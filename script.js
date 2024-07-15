const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
const transcription = document.getElementById('transcription');

let recognition;

if ('webkitSpeechRecognition' in window) {
  recognition = new webkitSpeechRecognition();
} else if ('SpeechRecognition' in window) {
  recognition = new SpeechRecognition();
} else {
  alert('Your browser does not support Speech Recognition');
}

if (recognition) {
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = 'en-US';

  recognition.onstart = () => {
    startButton.disabled = true;
    stopButton.disabled = false;
    transcription.innerHTML = 'Listening...';
  };

  recognition.onresult = (event) => {
    let interimTranscript = '';
    let finalTranscript = '';

    for (let i = 0; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript += transcript;
      } else {
        interimTranscript += transcript;
      }
    }

    transcription.innerHTML = finalTranscript + '<i style="color: #777;">' + interimTranscript + '</i>';
  };

  recognition.onerror = (event) => {
    console.error(event.error);
    alert('Error occurred in speech recognition: ' + event.error);
  };

  recognition.onend = () => {
    startButton.disabled = false;
    stopButton.disabled = true;
    transcription.innerHTML += '<p><i>Stopped listening</i></p>';
  };

  startButton.addEventListener('click', () => {
    recognition.start();
  });

  stopButton.addEventListener('click', () => {
    recognition.stop();
  });
}
