var app = new Vue({
  el: '#account',
  //All data here
  data: {
    user: null,
    account: null,

    responses: [],
  },
  //On Awake methods here:
  mounted: function () {

  },
  //Js Methods here:
  methods: {

    async loadResponses() {
      const data = {
        username: this.account,
        interviewQuestion: ""
      }

      postHelper(data, '/interview/data/search')
        .then(response => {
          this.responses = response.data;
          if (this.responses.length > 0) {
            const firstResponse = this.responses[0];
            this.$set(firstResponse, 'showTranscript', true);
            this.$set(firstResponse, 'showComments', true);
            this.$set(firstResponse, 'showGPT', true);
          }
        })
        .catch(error => {
          console.log(error);
        })
    },

    formatDate(timestamp) {
      if (!timestamp) return "";
      const date = new Date(timestamp);
      return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()} at ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
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

    async deleteResponse(questionId, responseId) {
      const res = await axios.delete(`${BACKEND_URL}/interview/${questionId}/responses/${responseId}`);
      if (res.status !== 200) {
        alert(`API returned non-200 status when deleting response: ${res.status}`);
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

  },
  //FrontEnd methods here:
  computed: {
    averageRatings() {
      const res = {};
      this.responses.forEach(response => {
        if (!response.ratings) {
          res[response.id] = 0.0;
          return;
        }

        res[response.id] = response.ratings.map(rating => rating.rating).reduce((a, b) => a + b, 0) / response.ratings.length;
      });
      return res;
    },

    overallRating() {
      let res = 0.0;

      this.responses.forEach(response => {
        if (!response.ratings) {
          return;
        }
        res += response.ratings.map(rating => rating.rating).reduce((a, b) => a + b, 0) / response.ratings.length;
      });
      return res / this.responses.length;
    },

    uniqueQs() {
      const uniques = new Set(this.responses.map(obj => obj.questionId));
      return uniques.size;
    }
  },

  beforeMount() {
    forceLoggedIn();
    this.user = getLoggedInUsername();
    this.account = USER_ID; //Defined in account.ejs -- needs to be an api call to see if user exists (if user query returns empty redirect to 403)
    this.loadResponses();
  }
});



