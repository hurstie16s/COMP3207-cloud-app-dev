var app = new Vue({
    el: '#set-new-password',
    data: {
      user: null,

      oldPassword: '',
      oldPasswordError: '',
      newPassword1: '',
      newPassword1Error: '',
      newPassword2: '',
      newPassword2Error: ''
      
    },
    methods: {
        logout() {
            logout(); //utils.logout
        },

        async setNewPassword() {
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
                const response = await axios.put(`${BACKEND_URL}/password/change`, data);
                if (response.status ===200) {
                    addNotification('Succesfully changed password');
                    setTimeout(function() {window.location.href = '/explore'}, 1000);
                } else if (response.status === 403) {
                    this.newPassword2Error = response.data.msg.replace(/:/g, ':\n \u2022 ').replace(/;/g, '\n \u2022 ');
                } else {
                    addNotification(`An error occurred: ${response.status} ` + response.statusText);
                }
            }

        },

    },
    computed: {
        
    },
    beforeMount() {
        forceLoggedIn();
        this.user = getLoggedInUsername();
    }
});