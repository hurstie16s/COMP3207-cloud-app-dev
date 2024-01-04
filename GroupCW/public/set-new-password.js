var app = new Vue({
    el: '#set-new-password',
    //All data here
    data: {
      user: null,

      oldPassword: '',
      oldPasswordError: '',
      newPassword1: '',
      newPassword1Error: '',
      newPassword2: '',
      newPassword2Error: ''
      
    },
    //On Awake methods here:
    mounted: function() {

    },
    //Js Methods here:
    methods: {
        logout() {
            logout(); //utils.logout
        },

        setNewPassword() {
            app.oldPasswordError = '';
            app.newPassword1Error = '';
            app.newPassword2Error = '';

            if (!this.oldPassword) {app.oldPasswordError = 'Password Required';}
            if (!this.newPassword1) {app.newPassword1Error = 'Password Required';}
            if (!this.newPassword2) {app.newPassword2Error = 'Password Required';}


            if (this.oldPassword && this.newPassword1 && this.newPassword2) {
                const data = {
                    username: app.user,
                    currentPassword: this.oldPassword,
                    newPassword: this.newPassword1,
                    newPasswordConfirm: this.newPassword2
                }
                putHelper(data, '/password/change')
                .then(response => {
                    if (response.status === 200) {
                        window.location.href = '/explore'
                        alert('Password Change Success')
                    } else if (response.status === 403) {
                        response.data.msg === 'AuthFail' ? app.oldPasswordError = 'Does not match old password' : app.newPassword2Error = 'Password does not match confirmation';
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
        
    },
    beforeMount() {
        forceLoggedIn();
        this.user = getLoggedInUsername();
    }
});