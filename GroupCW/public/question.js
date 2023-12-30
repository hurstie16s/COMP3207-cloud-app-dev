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
      
    },
    //Js Methods here:
    methods: {
      logout() {
        logout(); //utils.logout
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
        const res = await axios.get(`${BACKEND_URL}/interview/question/receive?id=${questionId}`);
        if (res.status === 404) {
          alert("Question not found");
          location.href = '/explore';
          return;
        } else if (res.status !== 200) {
          alert(`API returned non-200 status when loading questions: ${res.status}`);
          return;
        }
      
        return res.data;
      },

      startRecording() {
        app.isRecording = true
        AudioRecorder.start();
      },

      async stopRecording() {
        app.isRecording = false;
        const blob = await AudioRecorder.stop();

        const formData = new FormData();
        formData.append('username', this.user);
        formData.append('industry', 'TODO'); // TODO: Industry?
        formData.append('interviewTitle', this.question.question);
        formData.append('interviewQuestion', this.question.question);
        formData.append('private', false); // TODO: Private?
        formData.append('webmFile', blob);

        const res = await axios({
          method: 'post',
          url: `${BACKEND_URL}/interview/data/send`,
          data: formData,
          headers: { "Content-Type": "multipart/form-data" }
        });

        if (res.status !== 200) {
          alert(`API returned non-200 status when sending audio: ${res.status}`);
          return;
        }

        if (res.data.result !== true) {
          alert(`API returned error when sending audio: ${res.data.msg}`);
          return;
        }

        alert("upload success");
      }
    },
    //FrontEnd methods here:
    computed: {
        
    },
    async beforeMount() {
      this.user = getUserCookie();
      this.question = await this.loadQuestion(QUESTION_ID); // QUESTION_ID is defined via EJS in question.ejs
    }
});


//any functions outside of vue here:



//---------------------------------------------------------
// Dummies
