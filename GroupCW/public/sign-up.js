var app = new Vue({
    el: '#register',
    //All data here
    data: {
      user: null,

      username: '',
      password: '',
      email: '',
      usernameError: '',
      passwordError: '',
      emailError: '',
      
    },
    //On Awake methods here:
    mounted: function() {
      if (document.cookie.split(';').includes('user')) {
        document.cookie = 'user=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'; //date is the past so browser removes it
        app.user = null; //change to cookie
      }
    },
    //Js Methods here:
    methods: {
        register() {
          app.usernameError = '';
          app.passwordError = '';
          app.emailError = '';
          //handles empty fields
          if (!this.username) {app.usernameError = 'Username Required';}
          if (!this.password) {app.passwordError = 'Password Required';}
          if (!this.email) {app.emailError = 'Email Required';}

          //only calls api if fields if both username and password have values
          if (this.username && this.password && this.password) {
            const data = {
              username: this.username,
              password: this.password,
              email: this.email 
            }
            postHelper(data, '/register')
            .then(response => {
              if (response.status === 201) {
              app.user = this.username;
              setCookie(app.user);
              window.location.href = '/explore'
              } else {
                handleError(response.data);
              }
            })
            .catch(error => {
              console.log(error);
            })
          }
        },

    },
    //FrontEnd methods here:
    computed: {
        
      }
});


function handleError(error) {
  if (error.toLowerCase().includes('email')) {
    app.emailError = error;
  } else if (error.toLowerCase().includes('username')) {
    app.usernameError = error;
  } else {
    app.passwordError = error.replace(/:/g, ':\n \u2022 ').replace(/;/g, '\n \u2022 ');
  }
}
