var app = new Vue({
    el: '#reset-password',
    //All data here
    data: {
      user: null,

      email: '',
      emailError: ''
      
    },
    //On Awake methods here:
    mounted: function() {

    },
    //Js Methods here:
    methods: {
        async resetPassword() {
          app.emailError = '';

          if (app.email) {
            const res = await axios.put(`${BACKEND_URL}/password/reset`, {email: this.email});
            if (res.status > 299) {
              alert(`API returned non-200 status when submitting comment: ${res.status}` + (res.data ? `: ${res.data.msg}` : ''));
              return;
            }
          } else {this.emailError = 'Email Required';}
        }

    },
    //FrontEnd methods here:
    computed: {
        
      }
});
