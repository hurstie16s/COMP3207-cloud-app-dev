var app = new Vue({
    el: '#set-new-password',
    //All data here
    data: {
      user: null,

      password1: '',
      password1Error: '',
      password2: '',
      password2Error: ''
      
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
            app.password1Error = '';
            app.password2Error = '';

            if (!this.password1) {app.password1Error = 'Password Required';}
            if (!this.password2) {app.password2Error = 'Password Required';}

            if (this.password1 !== this.password2) {
                app.password2Error = 'Passwords must match';
                return;
            }

            if (this.password1 && this.password2) {
                const response = handleSetNewPassoword(app.user, this.password1);
                if (response.result === true) {
                    alert("password has been changed");
                    window.location.href = '/explore';
                } else {
                    alert(response.msg);
                }
            }

        },

    },
    //FrontEnd methods here:
    computed: {
        
    },

    beforeMount() {
    this.user = getUserCookie();
    }
});

function handleSetNewPassoword(user, password) {
    return {result: true, msg: "OK"};
}