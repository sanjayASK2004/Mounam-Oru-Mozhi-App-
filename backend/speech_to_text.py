import speech_recognition as sr

def tamil_speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            # Using Google Speech Recognition API (requires internet)
            text = recognizer.recognize_google(audio, language='ta-IN')  # 'ta-IN' for Tamil
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

if __name__ == "__main__":
    # Test the function with a sample audio file
    test_audio = "path_to_test_audio.wav"
    result = tamil_speech_to_text(test_audio)
    print(f"Recognized Tamil text: {result}")