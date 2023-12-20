var app = new Vue({
    el: '#VueApp',
    //All data here
    data: {
      page: 'sign-in',
      user: null
    },
    /*
    //On Awake methods here:
    mounted: function() {
       
    },
    */
    //Js Methods here:
    methods: {
        nav(page) {
          app.page = page;
        },

        logout() {
          app.user = null;
          this.nav('sign-in');
        }
    },
    //FrontEnd methods here:
    computed: {
        
      }
});

//any functions outside of vue here: