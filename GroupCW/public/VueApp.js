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
        }
    },
    //FrontEnd methods here:
    computed: {
        
      }
});

//any functions outside of vue here: