var app = new Vue({
    el: '#reset-password',
    //All data here
    data: {
      user: null,

      email: '',
      emailError: ''
      
    },
    //On Awake methods here:
    mounted: function() {

    },
    //Js Methods here:
    methods: {
        logout() {
          document.cookie = 'user=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'; //date is the past so browser removes it
          app.user = null; //change to cookie
          window.location.href = '/sign-in';
        },

        resetPassword() {
          app.emailError = '';

          if (app.email) {
            const response = handlePasswordReset();
            if (response.result === true) {
              //TODO:
              //feedback that password has been reset
            } else {
              app.emailError = response.msg;
            }
          } else {app.emailError = 'Email Required';}
        }

    },
    //FrontEnd methods here:
    computed: {
        
      }
});



//---------------------------------------------------------
// Dummies
function handlePasswordReset() {
  //call api
  return {result: false, msg: 'Email does not exist'}
}

function getHelper(data, endpoint) {

}

function postHelper(data, endpoint) {

}

function putHelper(data, endpoint) {

}
