var app = new Vue({
    el: '#VueApp',
    //All data here
    data: {
      page: 'sign-in',
      user: null,

      username: '',
      password: ''
    },
    /*
    //On Awake methods here:
    mounted: function() {
       
    },
    */
    //Js Methods here:
    methods: {
        nav(page) {
          app.page = page;
        },

        logout() {
          app.user = null;
          this.nav('sign-in');
        },

        login() {
          if (this.username === "") { //empty username
            //username error
          } else if (this.password === "") { //empty password
            //password error
          } else {
            const response = handleSignIn(this.username, this.password);
            if (response.status === 'OK') {
              app.user = this.username;
              this.nav('explore');
            } else {
              //reponse.msg error
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


//---------------------------------------------------------
// Dummies
let userMap = new Map();
userMap.set('user1', 'password');
userMap.set('user2', 'password');
userMap.set('user3', 'password');

function handleSignIn(username, password) {
  if (userMap.has(username)) {
    if (password === userMap.get(username));
    return {status: 'OK', msg: ''};
  } else {
    return {status: 'error', msg: 'error msg'};
  }
}


