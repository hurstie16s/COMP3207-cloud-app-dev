let recorder = null;
let chunks = [];

export default {
    start: async function () {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        recorder.start();

        chunks = [];
        recorder.ondataavailable = e => chunks.push(e.data);
      } catch (e) {
        console.error(e);
        alert('Error capturing audio, check the console for more details');
      }
    },

    stop: async function () {
      if (recorder === null) return;
      recorder.stop();

      return new Promise(resolve => {
        recorder.onstop = e => {
          const blob = new Blob(chunks, { type: chunks[0]?.type || "audio/webm" });
          resolve(blob);
        };
      });
    }
}