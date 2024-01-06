let stream;
let recorder = null;
let chunks = [];

window.AudioRecorder = {
    start: async function () {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        recorder.start();

        chunks = [];
        recorder.ondataavailable = e => chunks.push(e.data);
      } catch (e) {
        console.error(e);
        addNotification('An error occured while capturing audio');
      }
    },

    stop: async function () {
      if (recorder === null) return;
      recorder.stop();

      if (stream !== null) {
        stream.getTracks().forEach(track => track.stop());
      }

      return new Promise(resolve => {
        recorder.onstop = e => {
          const blob = new Blob(chunks, { type: chunks[0]?.type || "audio/webm" });
          resolve(blob);
        };
      });
    }
}