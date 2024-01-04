var app = new Vue({
  el: '#question',
  //All data here
  data: {
    user: null,
    question: null,
    responses: [],
    isRecording: false,
  },
  //On Awake methods here:
  mounted: function () {

  },
  //Js Methods here:
  methods: {

    async loadQuestion(questionId) {
      const res = await axios.get(`${BACKEND_URL}/interview/question/receive`);
      if (res.status !== 200) {
        alert(`API returned non-200 status when loading questions: ${res.status}`);
        return;
      }

      return res.data.questions.find(question => question.id === questionId);
    },
<<<<<<< HEAD

    startRecording() {
      app.isRecording = true
      AudioRecorder.start();
    },

    formatDate(timestamp) {
      if (!timestamp) return "";
      const date = new Date(timestamp);
      return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()} at ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
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
=======
    //FrontEnd methods here:
    computed: {
      userResponses() {
        return this.responses.filter(response => response.username === this.user);
      },
      communityResponses() {
        return this.responses.filter(response => response.username !== this.user);
      },
      userRatings() {
        const res = {};
        this.responses.filter(r => r.ratings).forEach(response => {
          const rating = response.ratings.find(rating => rating.username === this.user);
          if (rating !== undefined) res[response.id] = rating.rating;
        });
        return res;
      },
      averageRatings() {
        const res = {};
        this.responses.forEach(response => {
          if (!response.ratings || response.ratings.length === 0) {
            res[response.id] = 0.0;
            return;
          }
          
          res[response.id] = response.ratings.map(rating => rating.rating).reduce((a, b) => a + b, 0) / response.ratings.length;
        });
        return res;
>>>>>>> origin/main
      }

      return res.data.question;
    },

    async loadResponses(questionId) {
      const res = await axios.get(`${BACKEND_URL}/interview/${questionId}/responses`);
      if (res.status !== 200) {
        alert(`API returned non-200 status when loading responses: ${res.status}`);
        return;
      }

      return res.data;
    },

    async updatePrivacy(questionId, responseId, isPrivate) {
      const data = { private: isPrivate };
      const res = await axios.patch(`${BACKEND_URL}/interview/${questionId}/responses/${responseId}`, data);
      if (res.status !== 200) {
        alert(`API returned non-200 status when updating privacy: ${res.status}`);
        return;
      }

      const response = this.responses.find(response => response.id === responseId);
      response.private = isPrivate;
    },

    async submitComment(questionId, responseId, comment) {
      const data = {
        id: responseId,
        username: this.user,
        comment: comment
      };

      const res = await axios.put(`${BACKEND_URL}/send/comments`, data);
      if (res.status > 299) {
        alert(`API returned non-200 status when submitting comment: ${res.status}` + (res.data ? `: ${res.data.msg}` : ''));
        return;
      }

      const response = this.responses.find(response => response.id === responseId);
      response.comments.push(res.data.data);

      response.pending_comment = '';
    },

    async rateComment(responseId, commentId, action) {
      const data = {
        comment_id: commentId,
        username: this.user,
        rate_action: action
      };

      const res = await axios.put(`${BACKEND_URL}/rate/comments`, data);
      if (res.status > 299) {
        alert(`API returned non-200 status when submitting rating: ${res.status}` + (res.data ? `: ${res.data.msg}` : ''));
        return;
      }

      const response = this.responses.find(response => response.id === responseId);
      const idx = response.comments.findIndex(comment => comment.id === commentId);
      response.comments[idx] = res.data.comment;
      response.comments = [...response.comments]; // Force Vue to re-render - doesn't detect change without this
    },

    async rateInterview(responseId, rating) {
      const data = {
        id: responseId,
        username: this.user,
        rating: rating
      };

      const res = await axios.put(`${BACKEND_URL}/rate/interview`, data);
      if (res.status > 299) {
        alert(`API returned non-200 status when submitting rating: ${res.status}` + (res.data ? `: ${res.data.msg}` : ''));
        return;
      }

      const response = this.responses.find(response => response.id === responseId);
      response.ratings = res.data.ratings;
    },

    async deleteResponse(questionId, responseId) {
      const res = await axios.delete(`${BACKEND_URL}/interview/${questionId}/responses/${responseId}`);
      if (res.status !== 200) {
        alert(`API returned non-200 status when deleting response: ${res.status}`);
        return;
      }

      const idx = this.responses.findIndex(response => response.id === responseId);
      this.responses.splice(idx, 1);
    },

    async playAudio(response) {
      if (!response.audio) {
        const res = await axios.get(`${BACKEND_URL}/interview/${response.questionId}/responses/${response.id}/audio`, { responseType: 'blob' });
        if (res.status !== 200) {
          alert(`API returned non-200 status when loading audio: ${res.status}`);
          return;
        }

        const blob = res.data;
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        audio.onended = () => { response.audioPaused = true };

        Vue.set(response, 'audio', audio); // Vue can't detect nested new properties without this
        Vue.set(response, 'audioPaused', true); // Vue can't detect nested new properties without this
      }

      response.audio.play();
      response.audioPaused = false;
    },

    async pauseAudio(response) {
      if (!response.audio) return;

      response.audio.pause();
      response.audioPaused = true;
    },

    async seekAudio(responseId, seconds) {
      const response = this.responses.find(response => response.id === responseId);
      if (!response) return;

      if (!response.audio) return;

      response.audio.currentTime += seconds;
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
      formData.append('private', false); // TODO: Private?
      formData.append('webmFile', blob);

      const res = await axios({
        method: 'post',
        url: `${BACKEND_URL}/interview/${this.question.id}/responses`,
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

      await this.loadResponses(QUESTION_ID);
      alert("upload success");
    }
  },
  //FrontEnd methods here:
  computed: {
    userResponses() {
      return this.responses.filter(response => response.username === this.user);
    },
    communityResponses() {
      return this.responses.filter(response => response.username !== this.user);
    },
    userRatings() {
      const res = {};
      this.responses.filter(r => r.ratings).forEach(response => {
        const rating = response.ratings.find(rating => rating.username === this.user);
        if (rating !== undefined) res[response.id] = rating.rating;
      });
      return res;
    },
    averageRatings() {
      const res = {};
      this.responses.forEach(response => {
        if (!response.ratings || response.ratings.length === 0) {
          res[response.id] = 0.0;
          return;
        }

        res[response.id] = response.ratings.map(rating => rating.rating).reduce((a, b) => a + b, 0) / response.ratings.length;
      });
      return res;
    }
  },
  async beforeMount() {
    this.user = getUserCookie();
    this.question = await this.loadQuestion(QUESTION_ID); // QUESTION_ID is defined via EJS in question.ejs
    this.responses = await this.loadResponses(QUESTION_ID);
  }
});


//any functions outside of vue here:



//---------------------------------------------------------
// Dummies
