var app = new Vue({
  el: '#reset-password',
  //All data here
  data: {
    user: null,

    email: '',
    emailError: '',
    submitted: false,
    sending: false
  },
  //On Awake methods here:
  mounted: function () {

  },
  //Js Methods here:
  methods: {
    async resetPassword() {
      app.emailError = '';
      this.sending = true;
      if (app.email) {
        const res = await axios.put(`${BACKEND_URL}/password/reset`, { email: this.email });
        if (res.status > 299) {
          addNotification(`An error occurred: ${res.status} ` + (res.data ? ` ${res.data.msg}` : ''));
          this.sending = false;
          return;
        } else {
          this.submitted = true;
          this.sending = false;
        }
      } else {
        this.emailError = 'Email Required';
        this.sending = false;
      }
    }

  },
  //FrontEnd methods here:
  computed: {

  }
});
