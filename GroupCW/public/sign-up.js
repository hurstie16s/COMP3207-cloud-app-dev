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
                setSessionData(response.data.username, response.data.token);
                app.user = response.data.username;
                window.location.href = '/explore';
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
