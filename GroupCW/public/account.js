var app = new Vue({
    el: '#account',
    //All data here
    data: {
      user: null,
      account: null,

      interviews: []
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
        if (!comment.thumbs_up.includes(this.user)) {
          const data = {
            comment_id: comment.id,
            username: this.user,
            rate_action: "like"
          }
          this.sendCommentRating(data);
        } 
      },

      dislike(comment) {
        if (!comment.thumbs_down.includes(this.user)) {
          const data = {
            comment_id: comment.id,
            username: this.user,
            rate_action: "dislike"
          }
          this.sendCommentRating(data);
        } 
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
        console.log(comment);
        return comment.thumbs_up.includes(this.user)
      },

      isDisliked(comment) {return comment.thumbs_down.includes(this.user)}

    },
    //FrontEnd methods here:
    computed: {
        
      },

    beforeMount() {
      this.user = getUserCookie();
      this.account = USER_ID; //Defined in account.ejs -- needs to be an api call to see if user exists (if user query returns empty redirect to 403)
      this.loadResponses();
    }
});

