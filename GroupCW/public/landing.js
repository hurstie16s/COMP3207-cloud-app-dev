var app = new Vue({
    el: '#landing',
    data: {
      user: null,

    },
    methods: {

    },
    computed: {
        
    },
    beforeMount() {
      this.user = getLoggedInUsername();
    }
});

