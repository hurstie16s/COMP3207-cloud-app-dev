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
        login() {
          app.usernameError = '';
          app.passwordError = '';

          //handles empty fields
          if (!this.username) {app.usernameError = 'Username Required';}
          if (!this.password) {app.passwordError = 'Password Required';}

          //only calls api if fields if both username and password have values
          if (this.username && this.password) {
            const response = handleLogin(this.username, this.password);
            if (response.result === true) {
              app.user = this.username;
              setCookie(app.user);
              window.location.href = '/explore'
            } else { //long winded nested if for to classify errors into username and password
              if (response.msg.toLowerCase().includes("username")) {
                app.usernameError = response.msg;
              } else if (response.msg.toLowerCase().includes("password")) {
                app.passwordError = response.msg;
              } else { //error not standardised
                alert(response.msg);
              }
            }
          }
        },


    },
    //FrontEnd methods here:
    computed: {
        
      }
});

function setCookie(username) {
  // Set the 'user' cookie with an expiration time of 1 hour
  const expirationDate = new Date();
  expirationDate.setTime(expirationDate.getTime() + (1 * 60 * 60 * 1000)); // 1 hour
  document.cookie = `user=${username}; expires=${expirationDate.toUTCString()}; path=/`;
}

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

