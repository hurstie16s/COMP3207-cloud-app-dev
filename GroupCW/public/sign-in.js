var app = new Vue({
    el: '#login',
    data: {
      user: null,

      username: '',
      password: '',
      usernameError: '',
      passwordError: '',

      
    },
    methods: {
        async login() {
          app.usernameError = '';
          app.passwordError = '';

          //handles empty fields
          if (!this.username) {app.usernameError = 'Username Required';}
          if (!this.password) {app.passwordError = 'Password Required';}

          //only calls api if fields if both username and password have values
          if (this.username && this.password) {
            const data = {
              username: this.username,
              password: this.password 
            }
            postHelper(data, '/login')
            .then(response => {
              if (response.status === 200) {
                setSessionData(response.data.username, response.data.token);
                app.user = response.data.username;
                window.location.href = '/explore'
              } else if (response.status === 401) {
                handleError(response.data.msg);
              } else if (response.status === 300) {
                setSessionData(response.data.username, response.data.token);
                app.user = response.data.username;
                window.location.href = '/set-new-password';
              } else {
                addNotification(`An error occurred: ${res.status} ` + res.statusText);
              }
            })
            .catch(error => {
              console.log(error);
            })

          }
        },


    },
    computed: {
        
      }
});

function handleError(error) {
  if (error === 'User not found') {
    app.usernameError = error;
  } else if (error === 'Invalid Login') {
    app.passwordError = error;
  } else {
    addNotification(`An error occurred: ${error} `);
  }
}

