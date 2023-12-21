var app = new Vue({
    el: '#VueApp',
    //All data here
    data: {
      page: 'sign-in',
      user: null,

      username: '',
      password: '',
      email: '',
      usernameError: '',
      passwordError: '',
      emailError: ''
      
    },
    /*
    //On Awake methods here:
    mounted: function() {
       
    },
    */
    //Js Methods here:
    methods: {
        resetErrors() {
          app.usernameError = '';
          app.passwordError = '';
          app.emailError = '';
        },

        resetFields() {
          app.username = '';
          app.password = '';
          app.email = '';
        },

        nav(page) {
          this.resetErrors();
          this.resetFields();
          app.page = page;
        },

        logout() {
          app.user = null;
          this.nav('sign-in');
        },

        login() {
          this.resetErrors();

          //handles empty fields
          if (!this.username) {app.usernameError = 'Username Required';}
          if (!this.password) {app.passwordError = 'Password Required';}

          //only calls api if fields if both username and password have values
          if (this.username && this.password) {
            const response = handleLogin(this.username, this.password);
            if (response.result === true) {
              app.user = this.username;
              this.nav('explore');
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
          
          this.resetFields();
        },

        register() {
          this.resetErrors();

          //handles empty fields
          if (!this.username) {app.usernameError = 'Username Required';}
          if (!this.password) {app.passwordError = 'Password Required';}
          if (!this.email) {app.emailError = 'Email Required';}

          //only calls api if fields if both username and password have values
          if (this.username && this.password && this.email) {
            const response = handleRegister(this.username, this.password);
            if (response.result === true) { // successful register logs you in straight away
              app.user = this.username;
              this.nav('explore');
            } else { //long winded nested if for to classify errors into username and password
              if (response.msg.toLowerCase().includes("username")) {
                app.usernameError = response.msg;
              } else if (response.msg.toLowerCase().includes("password")) {
                app.passwordError = response.msg;
              } else if (response.msg.toLowerCase().includes("password")){ 
                app.emailError = response.msg;
              } else { //error not standardised
                alert(response.msg);
              }
            }
          }
          
          this.resetFields();
        },

        resetPassword() {
          this.resetErrors();
          if (app.email) {
            const response = handlePasswordReset();
            if (response.result === true) { // successful register logs you in straight away
              app.user = this.username;
              this.nav('explore');
            } else {
              app.emailError = response.msg;
            }
          } else {app.emailError = 'Email Required';}
          this.resetFields();
        }

    },
    //FrontEnd methods here:
    computed: {
        
      }
});


//any functions outside of vue here:
function getHelper(data, endpoint) {

}

function postHelper(data, endpoint) {

}

function putHelper(data, endpoint) {

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

function handleRegister() {
  //call api
  return {result: true, msg: 'OK'}
}

function handlePasswordReset() {
  //call api
  return {result: false, msg: 'Email does not exist'}
}


