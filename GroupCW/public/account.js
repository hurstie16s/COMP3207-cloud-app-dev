var app = new Vue({
    el: '#account',
    //All data here
    data: {
      user: null,
      account: null,

      interviews: [],
      visibleElements: {}
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
          this.interviews = response.data;
          if (Object.keys(this.visibleElements).length === 0) {this.loadElements();}
        })
        .catch(error => {
          console.log(error);
        })
      },

      async submitComment(response) {
        const data = {
          comment: response.commentText,
          id: response.id,
          username: this.user
        }
        
        response.commentText = "";
        try {
          const response = await axios.put(`${BACKEND_URL}/send/comments`, data);
            console.log('Comment submitted successfully:', response.data);
            this.loadResponses();
        } catch (error) {
          console.error('Error submitting comment:', error);
        }
      },

      like(comment) {
        const data = {
          comment_id: comment.id,
          username: this.user,
          rate_action: "like"
        }
        this.sendCommentRating(data);
      },

      dislike(comment) {
        const data = {
          comment_id: comment.id,
          username: this.user,
          rate_action: "dislike"
        }
        this.sendCommentRating(data);
      },

      async sendCommentRating(data) {
        try {
          const response = await axios.put(`${BACKEND_URL}/rate/comments`, data);
            console.log('Comment submitted successfully:', response.data);
            this.loadResponses();
        } catch (error) {
          console.error('Error submitting comment:', error);
        }
      },

      isLiked(comment) {
        return comment.thumbs_up.includes(this.user)
      },

      isDisliked(comment) {
        return comment.thumbs_down.includes(this.user)
      },

      toggleVisibility(id) {
        this.$set(this.visibleElements, id, !this.visibleElements[id]);
      },

      loadElements() {
        this.interviews.forEach((response, index) => {
          this.$set(this.visibleElements, `response-transcript-${index}`, (index === 0 ? false : true));
          this.$set(this.visibleElements, `response-comments-${index}`, (index === 0 ? false : true));
        });
      }

    },
    //FrontEnd methods here:
    computed: {
        
      },

    beforeMount() {
      forceLoggedIn();
      this.user = getLoggedInUsername();
      this.account = USER_ID; //Defined in account.ejs -- needs to be an api call to see if user exists (if user query returns empty redirect to 403)
      this.loadResponses();
    }
});



