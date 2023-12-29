var app = new Vue({
    el: '#question',
    //All data here
    data: {
      user: null,

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
    }
});

