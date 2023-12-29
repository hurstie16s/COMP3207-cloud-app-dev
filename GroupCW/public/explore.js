var app = new Vue({
    el: '#explore',
    //All data here
    data: {
      user: null,

    },
    //On Awake methods here:
    mounted: function() {
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
