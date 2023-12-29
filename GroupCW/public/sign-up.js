var app = new Vue({
    el: '#register',
    //All data here
    data: {
      user: null,

      username: '',
      password: '',
      email: '',
      name: '',
      usernameError: '',
      passwordError: '',
      emailError: '',
      nameError: ''
      
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
          app.nameError = '';
          app.emailError = '';
          //handles empty fields
          if (!this.username) {app.usernameError = 'Username Required';}
          if (!this.password) {app.passwordError = 'Password Required';}
          if (!this.email) {app.emailError = 'Email Required';}
          if (!this.name) {app.nameError = 'Name Required';}

          //only calls api if fields if both username and password have values
          if (this.username && this.password && this.email) {
            const response = handleRegister(this.username, this.password);
            if (response.result === true) { // successful register logs you in straight away
              app.user = this.username;
              setCookie(app.user);
              window.location.href = '/explore'
            } else { //long winded nested if for to classify errors into username and password
              if (response.msg.toLowerCase().includes("username")) {
                app.usernameError = response.msg;
              } else if (response.msg.toLowerCase().includes("password")) {
                app.passwordError = response.msg;
              } else if (response.msg.toLowerCase().includes("password")){ 
                app.emailError = response.msg;
              } else { //error not standardised or name error!
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
function handleRegister() {
  //call api
  return {result: true, msg: 'OK'}
}




function getHelper(data, endpoint) {

}

function postHelper(data, endpoint) {

}

function putHelper(data, endpoint) {

}
