var app = new Vue({
    el: '#account',
    //All data here
    data: {
      user: null,
      account: null

    },
    //On Awake methods here:
    mounted: function() {
      
    },
    //Js Methods here:
    methods: {
      logout() {
        logout(); //utils.logout
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

