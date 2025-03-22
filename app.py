from flask import Flask, render_template, request, jsonify
import subprocess
import os

try:
    from backend.speech_to_text import tamil_speech_to_text
except ModuleNotFoundError as e:
    print(f"Error importing speech_to_text: {e}")
    tamil_speech_to_text = None

try:
    from backend.text_to_english import tamil_to_english
except ModuleNotFoundError as e:
    print(f"Error importing text_to_english: {e}")
    tamil_to_english = None

try:
    from backend.database import init_db, save_to_history, save_to_saved, get_history, get_saved
except ModuleNotFoundError as e:
    print(f"Error importing database: {e}")
    init_db, save_to_history, save_to_saved, get_history, get_saved = None, None, None, None, None

app = Flask(__name__)

# Initialize database
if init_db:
    init_db()
else:
    print("Database initialization failed. Please check backend.database module.")

def generate_sign_animation(english_text):
    blender_path = r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"  # Update this path
    script_path = os.path.join(os.getcwd(), "backend", "text_to_sign.py")

    try:
        result = subprocess.run(
            [blender_path, "-b", "-P", script_path, "--", english_text],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return "/static/animations/output.mp4"
        else:
            print(f"Blender error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error running Blender: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/language')
def language():
    return render_template('language.html')

@app.route('/mode')
def mode():
    return render_template('mode.html')

@app.route('/speech')
def speech():
    return render_template('speech.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/saved')
def saved():
    return render_template('saved.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if not (tamil_speech_to_text and tamil_to_english):
        return jsonify({'error': 'Required backend modules are not available'}), 500

    audio_file = request.files['audio']
    audio_path = 'temp_audio.wav'
    audio_file.save(audio_path)

    # Step 1: Speech to Tamil text
    tamil_text = tamil_speech_to_text(audio_path)
    if not tamil_text:
        return jsonify({'error': 'Speech recognition failed'}), 500

    # Step 2: Tamil to English
    english_text = tamil_to_english(tamil_text)
    if not english_text:
        return jsonify({'error': 'Translation failed'}), 500

    # Step 3: English to Sign Animation
    animation_path = generate_sign_animation(english_text)
    if not animation_path:
        return jsonify({'error': 'Animation generation failed'}), 500

    return jsonify({
        'tamil_text': tamil_text,
        'english_text': english_text,
        'animation': animation_path
    })

@app.route('/save_history', methods=['POST'])
def save_history():
    if not save_to_history:
        return jsonify({'error': 'Database module not available'}), 500
    data = request.json
    save_to_history(data['text'])
    return jsonify({'status': 'success'})

@app.route('/save_to_saved', methods=['POST'])
def save_to_saved_route():
    if not save_to_saved:
        return jsonify({'error': 'Database module not available'}), 500
    data = request.json
    save_to_saved(data['text'])
    return jsonify({'status': 'success'})

@app.route('/get_history')
def get_history_route():
    if not get_history:
        return jsonify({'error': 'Database module not available'}), 500
    return jsonify(get_history())

@app.route('/get_saved')
def get_saved_route():
    if not get_saved:
        return jsonify({'error': 'Database module not available'}), 500
    return jsonify(get_saved())

if __name__ == '__main__':
    app.run(debug=True)