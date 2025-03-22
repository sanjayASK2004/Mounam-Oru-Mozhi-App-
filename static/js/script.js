document.getElementById('record-btn').addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const chunks = [];

    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', blob, 'recording.wav');

        const response = await fetch('/process_audio', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        // Display Tamil text and animation
        document.getElementById('recognized-text').innerText = result.tamil_text;
        document.getElementById('sign-animation').src = result.animation;
        document.getElementById('sign-animation').play();

        // Save to history
        fetch('/save_history', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: result.tamil_text })
        });

        // Optionally save to "Saved" (e.g., if user clicks "சேமிப்பு" later)
    };

    mediaRecorder.start();
    setTimeout(() => mediaRecorder.stop(), 5000); // Record for 5 seconds
});