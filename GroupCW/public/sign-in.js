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
            getHelper(data, '/login')
            .then(response => {
              if (response.result) {
                app.user = this.username;
                setCookie(app.user);
                window.location.href = '/explore'
              } else {
                app.passwordError = response.msg;
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

//---------------------------------------------------------
// Dummies
let userMap = new Map();
userMap.set('user1', 'password');
userMap.set('user2', 'password');
userMap.set('user3', 'password');

function handleLogin(username, password) { //call api here
  if (username === 'test') {
    return {result: false, msg: 'error message'}
  }
  if (userMap.has(username)) {
    if (password === userMap.get(username)) {
      return {result: true, msg: 'OK'};
    } else {
      return {result: false, msg: 'Password is incorrect'}
    }
  } else {
    return {result: false, msg: 'Username does not exist'};
  }
}

