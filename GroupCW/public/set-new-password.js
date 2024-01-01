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
        this.getUserCookie();
    },
    //Js Methods here:
    methods: {
        logout() {
            document.cookie = 'user=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'; //date is the past so browser removes it
            this.user = null; //change to cookie
            window.location.href = '/';
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

        getUserCookie() {
            // Function to read the value of the 'user' cookie
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const [key, value] = cookie.trim().split('=');
                if (key === 'user') {
                    this.user = value; // Use 'this' to refer to the Vue instance
                    break;
                }
            }
        },

    },
    //FrontEnd methods here:
    computed: {
        
      }
});

function handleSetNewPassoword(user, password) {
    return {result: true, msg: "OK"};
}