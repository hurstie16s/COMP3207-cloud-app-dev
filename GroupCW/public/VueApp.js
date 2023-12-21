var app = new Vue({
    el: '#VueApp',
    //All data here
    data: {
      page: 'sign-in',
      user: null,

      username: '',
      password: '',
      usernameError: '',
      passwordError: ''
      
    },
    /*
    //On Awake methods here:
    mounted: function() {
       
    },
    */
    //Js Methods here:
    methods: {
        resets() {
          app.usernameError = '';
          app.passwordError = '';
        },

        nav(page) {
          app.page = page;
        },

        logout() {
          app.user = null;
          this.nav('sign-in');
        },

        login() {
          this.resets();

          //handles empty fields
          if (!this.username) {app.usernameError = 'Username Required';}
          if (!this.password) {app.passwordError = 'Password Required';}

          //only calls api if fields if both username and password have values
          if (this.username && this.password) {
            const response = handleLogin(this.username, this.password);
            if (response.result === true) {
              app.user = this.username;
              this.nav('explore');
            } else { //stupid long winded nested if for to classify errors into username and password
              if (response.msg.toLowerCase().includes("username")) {
                app.usernameError = response.msg;
              } else if (response.msg.toLowerCase().includes("password")) {
                app.passwordError = response.msg;
              } else { //error not standardised
                alert(response.msg);
              }
            }
          }
          
          app.username = '';
          app.password = '';
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


