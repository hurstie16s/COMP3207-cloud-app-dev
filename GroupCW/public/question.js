import AudioRecorder from './audio.js';

var app = new Vue({
    el: '#question',
    //All data here
    data: {
      user: null,
      question: null,
      isRecording: false,
    },
    //On Awake methods here:
    mounted: function() {
      this.getUserCookie();
    },
    //Js Methods here:
    methods: {
      logout() {
        document.cookie = 'user=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'; //date is the past so browser removes it
        this.user = null; //change to cookie
        window.location.href = '/';
      },

      getUserCookie() {
        // Function to read the value of the 'user' cookie
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
          const [key, value] = cookie.trim().split('=');
          if (key === 'user') {
            this.user = value; // Use 'this' to refer to the Vue instance
            break;
          }
        }
      },

      async loadQuestion(questionId) {
        const res = await axios.get(`${BACKEND_URL}/interview/question/receive`);
        if (res.status !== 200) {
          alert(`API returned non-200 status when loading questions: ${res.status}`);
          return;
        }
      
        return res.data.questions.find(question => question.id === questionId);
      },

      startRecording() {
        app.isRecording = true
        AudioRecorder.start();
      },

      async stopRecording() {
        app.isRecording = false;
        const blob = await AudioRecorder.stop();
        const audioURL = window.URL.createObjectURL(blob);
      }
    },
    //FrontEnd methods here:
    computed: {
        
    },
    async beforeMount() {
      this.question = await this.loadQuestion(QUESTION_ID); // QUESTION_ID is defined via EJS in question.ejs
    }
});


//any functions outside of vue here:



//---------------------------------------------------------
// Dummies
