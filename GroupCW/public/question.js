var app = new Vue({
    el: '#question',
    //All data here
    data: {
      user: null,

    },
    //On Awake methods here:
    mounted: function() {
      this.getUserCookie();
    },
    //Js Methods here:
    methods: {
      logout() {
        document.cookie = 'user=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'; //date is the past so browser removes it
        this.user = null; //change to cookie
        window.location.href = '/sign-in';
      },

      getUserCookie() {
        // Function to read the value of the 'user' cookie
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
          const [key, value] = cookie.trim().split('=');
          if (key === 'user') {
            this.user = value; // Use 'this' to refer to the Vue instance
            break;
          }
        }
      },

    },
    //FrontEnd methods here:
    computed: {
        
      }
});


//any functions outside of vue here:



//---------------------------------------------------------
// Dummies
