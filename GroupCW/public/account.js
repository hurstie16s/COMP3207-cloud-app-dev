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
      this.loadResponses()
    },
    //Js Methods here:
    methods: {
      
      async loadResponses() {
        const data = {
          username: this.account,
          interviewQuestion: ""  
        }

        getHelper(data, 'interview/data/search')
        .then(response => {
          if (response.status === 200) {
            interviews = response.data;
          } else {
            //404
          }
        })
      },

    },
    //FrontEnd methods here:
    computed: {
        
      },

    beforeMount() {
      this.user = getUserCookie();
      this.account = USER_ID; //Defined in account.ejs -- needs to be an api call to see if user exists (if user query returns empty redirect to 403)
    }
});

