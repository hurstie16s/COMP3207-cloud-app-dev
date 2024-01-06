var app = new Vue({
  el: '#question',
  //All data here
  data: {
    user: null,
    question: {},
    responses: [],
    isRecording: false,
    awaitingSubmission: false,
    industries: ['Computer Science', 'Engineering', 'Finance', 'Law', 'Retail'],
    industry: 'Computer Science',
    communityIndustryFilter: 'All Industries',
    userIndustryFilter: 'All Industries',
    userSortBy: 'Newest First',
    communitySortBy: 'Top Rated',
  },
  //On Awake methods here:
  mounted: function () {

  },
  //Js Methods here:
  methods: {

    async loadQuestion(questionId) {
      const res = await axios.get(`${BACKEND_URL}/interview/question/receive`);
      if (res.status !== 200) {
        addNotification(`An error occured: ${res.status} `)
        return;
      }
      return res.data.questions.find(question => question.id === questionId);
    },

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
        location.href = '/404';
        return;
      } else if (res.status !== 200) {
        addNotification(`An error occured: ${res.status} `)
        return;
      }
      console.log(res);
      return res.data.question;
    },

    async loadResponses(questionId) {
      const res = await axios.get(`${BACKEND_URL}/interview/${questionId}/responses`);
      if (res.status !== 200) {
        addNotification(`An error occured: ${res.status} `)
        return;
      }

      this.responses = res.data;
      if (this.responses.length > 0) {
        this.calculateAverages();
      }
    },

    async updatePrivacy(questionId, responseId, isPrivate) {
      const data = { private: isPrivate };
      const res = await axios.patch(`${BACKEND_URL}/interview/${questionId}/responses/${responseId}`, data);
      if (res.status !== 200) {
        addNotification(`An error occured: ${res.status} `)
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
        addNotification(`An error occurred: ${res.status} ` + (res.data ? ` ${res.data.msg}` : ''));
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
        addNotification(`An error occurred: ${res.status} ` + (res.data ? ` ${res.data.msg}` : ''));
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
        addNotification(`An error occurred: ${res.status} ` + (res.data ? ` ${res.data.msg}` : ''));
        return;
      }
      console.log(res.data);
      const response = this.responses.find(response => response.id === responseId);
      response.ratings = res.data.ratings;
      response.average = this.calculateAverage(response);
    },

    async deleteResponse(questionId, responseId) {
      const res = await axios.delete(`${BACKEND_URL}/interview/${questionId}/responses/${responseId}`);
      if (res.status !== 200) {

        return;
      }

      const idx = this.responses.findIndex(response => response.id === responseId);
      this.responses.splice(idx, 1);
      addNotification('Response deleted');
    },

    async playAudio(response) {
      if (!response.audio) {
        const res = await axios.get(`${BACKEND_URL}/interview/${response.questionId}/responses/${response.id}/audio`, { responseType: 'blob' });
        if (res.status !== 200) {
          addNotification(`An error occured: ${res.status} `)
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
      app.awaitingSubmission = false;
      AudioRecorder.start();
    },

    async stopRecording() {
      app.isRecording = false;
      app.awaitingSubmission = true;
      this.blob = await AudioRecorder.stop();
    },

    async deleteRecording() {
      app.awaitingSubmission = false;
    },

    async submitRecording() {
      document.getElementById('response-submission-spinner').classList.toggle('hidden');
      const formData = new FormData();
      formData.append('username', this.user);
      formData.append('industry', this.industry);
      formData.append('interviewTitle', this.question.question);
      formData.append('private', false); // TODO: Private?
      formData.append('webmFile', this.blob);

      const res = await axios({
        method: 'post',
        url: `${BACKEND_URL}/interview/${this.question.id}/responses`,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" }
      });

      if (res.status !== 200) {
        addNotification(`An error occured: ${res.status} `);
        document.getElementById('response-submission-spinner').classList.toggle('hidden');
        return;
      }

      if (res.data.result !== true) {
        addNotification(`An error occured: ${res.data.msg} `);
        document.getElementById('response-submission-spinner').classList.toggle('hidden');
        return;
      }
      addNotification('Response Uploaded');
      document.getElementById('response-submission-spinner').classList.toggle('hidden');
      app.awaitingSubmission = false;

        await this.loadResponses(QUESTION_ID);

    },

    calculateAverages() {
      this.responses.forEach(response => {
        this.$set(response, 'average', this.calculateAverage(response));
      });
    },

    calculateAverage(response) {
      if (!response.ratings || response.ratings.length === 0) {
        return 0.0;
      }
      return response.ratings.map(rating => rating.rating).reduce((a, b) => a + b, 0) / response.ratings.length;
    },

    goToAccount(user) {
      getAccount(user);
    }

  },


  //FrontEnd methods here:
  computed: {
    userResponses() {
      const responses = this.responses
        .filter(response => response.username === this.user)
        .filter(response => this.userIndustryFilter === 'All Industries' || response.industry === this.userIndustryFilter);

      if (this.userSortBy === 'Newest First') {
        responses.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
      } else if (this.userSortBy === 'Oldest First') {
        responses.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
      } else if (this.userSortBy === 'Top Rated') {
        responses.sort((a, b) => b.average - a.average);
      } else if (this.userSortBy === 'Lowest Rated') {
        responses.sort((a, b) => a.average - b.average);
      }
      if (responses.length > 0) {
        responses.forEach(response => {
          this.$set(response, 'showTranscript', false);
          this.$set(response, 'showComments', false);
          this.$set(response, 'showGPT', false);
          this.$set(response, 'language', "English");
        });
        const firstResponse = responses[0];
        this.$set(firstResponse, 'showTranscript', true);
        this.$set(firstResponse, 'showComments', true);
        this.$set(firstResponse, 'showGPT', true);
      }
      return responses;
    },
    communityResponses() {
      const responses = this.responses
        .filter(response => response.username !== this.user)
        .filter(response => this.communityIndustryFilter === 'All Industries' || response.industry === this.communityIndustryFilter);
      if (this.communitySortBy === 'Newest First') {
        responses.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
      } else if (this.communitySortBy === 'Oldest First') {
        responses.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
      } else if (this.communitySortBy === 'Top Rated') {
        responses.sort((a, b) => b.average - a.average);
      } else if (this.communitySortBy === 'Lowest Rated') {
        responses.sort((a, b) => a.average - b.average);
      }
      if (responses.length > 0) {
        responses.forEach(response => {
          this.$set(response, 'showTranscript', false);
          this.$set(response, 'showComments', false);
          this.$set(response, 'showGPT', false);
          this.$set(response, 'language', "English");
        });
      }

      return responses;
    },
    userRatings() {
      const res = {};
      this.responses.filter(r => r.ratings).forEach(response => {
        const rating = response.ratings.find(rating => rating.username === this.user);
        if (rating !== undefined) res[response.id] = rating.rating;
      });
      return res;
    },
  },
  async beforeMount() {
    forceLoggedIn();
    this.user = getLoggedInUsername();
    this.question = await this.loadQuestion(QUESTION_ID); // QUESTION_ID is defined via EJS in question.ejs
    this.loadResponses(QUESTION_ID);
  }
});


//any functions outside of vue here:



//---------------------------------------------------------
// Dummies
