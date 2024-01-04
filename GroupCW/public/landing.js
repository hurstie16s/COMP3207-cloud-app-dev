var app = new Vue({
    el: '#landing',
    //All data here
    data: {
      user: null,

    },
    //On Awake methods here:
    mounted: function() {

    },
    //Js Methods here:
    methods: {

    },
    //FrontEnd methods here:
    computed: {
        
      },

    beforeMount() {
      this.user = getLoggedInUsername();
    }
});

