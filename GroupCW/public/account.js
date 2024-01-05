var app = new Vue({
  el: '#account',
  //All data here
  data: {
    user: null,
    account: null,

      responses: [],
      sortBy: 'Oldest First',
      industries: ['Computer Science','Engineering', 'Finance', 'Law', 'Retail'],
      industryFilter: 'All Industries'
    },
    //On Awake methods here:
    mounted: function() {
      
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
            this.calculateAverages();
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
        addNotification(`An error occured: ${res.status} `)
        return;
      }

        const response = this.responses.find(response => response.id === responseId);
        response.private = isPrivate;
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

    async deleteResponse(questionId, responseId) {
      const res = await axios.delete(`${BACKEND_URL}/interview/${questionId}/responses/${responseId}`);
      if (res.status !== 200) {
        addNotification(`An error occured: ${res.status} `)
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
      
      goToAccount(user){
        getAccount(user);
      }

    },
    //FrontEnd methods here:
    computed: {
      overallRating() {
        let res = 0.0;
        if (this.responses.length === 0) {
          return 0;
        }

        this.responses.forEach(response => {
         res += response.average;
        });
        return res/this.responses.length;
      },

      uniqueQs() {
        const uniques = new Set(this.responses.map(obj => obj.questionId));
        return uniques.size;
      },

      userResponses() {
        const responses = this.responses
          .filter(response => this.industryFilter === 'All Industries' || response.industry === this.industryFilter);
        
        if (this.sortBy === 'Newest First') {
          responses.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        } else if (this.sortBy === 'Oldest First') {
          responses.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
        } else if (this.sortBy === 'Top Rated') {
          responses.sort((a, b) => b.average - a.average);
        } else if (this.sortBy === 'Lowest Rated') {
          responses.sort((a, b) => a.average - b.average);
        }
        if (responses.length > 0) {
          responses.forEach(response => {
            this.$set(response, 'showTranscript', false);
            this.$set(response, 'showComments', false);
            this.$set(response, 'showGPT', false);
          });
          const firstResponse = responses[0];
          this.$set(firstResponse, 'showTranscript', true);
          this.$set(firstResponse, 'showComments', true);
          this.$set(firstResponse, 'showGPT', true);
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

  beforeMount() {
    forceLoggedIn();
    this.user = getLoggedInUsername();
    this.account = USER_ID; //Defined in account.ejs -- needs to be an api call to see if user exists (if user query returns empty redirect to 403)
    this.loadResponses();
  }
});



