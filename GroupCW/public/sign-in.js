var app = new Vue({
    el: '#login',
    //All data here
    data: {
      user: null,

      username: '',
      password: '',
      usernameError: '',
      passwordError: '',

      
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
                app.user = this.username;
                setCookie(app.user);
                window.location.href = '/explore'
              } else if (response.status === 401) {
                handleError(response.data.msg);
              } else if (response.status === 300) {
                app.user = this.username;
                setCookie(app.user);
                window.location.href = '/set-new-password'
              } else {
                alert(`${response.status}: ${response.statusText}`) //undefined error
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
  if (error === 'User not found') {
    app.usernameError = error;
  } else if (error === 'Invalid Login') {
    app.passwordError = error;
  } else {
    alert(error);
  }
}

