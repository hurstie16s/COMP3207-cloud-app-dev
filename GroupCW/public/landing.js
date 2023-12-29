var app = new Vue({
    el: '#landing',
    //All data here
    data: {
      user: null,

    },
    //On Awake methods here:
    mounted: function() {
      console.log(getUserCookie());
      this.user = getUserCookie();
    },
    //Js Methods here:
    methods: {
      logout() {
        logout(); //utils.logout
      },
      

    },
    //FrontEnd methods here:
    computed: {
        
      }
});

