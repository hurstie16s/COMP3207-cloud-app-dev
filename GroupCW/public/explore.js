var app = new Vue({
    el: '#explore',
    //All data here
    data: {
      user: null,
      search: '',
      filterRegularity: -1, // -1 = all,
      filterDifficulty: -1, // -1 = all,
      questions: [],
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

      async loadQuestions() {
        const res = await axios.get(`${BACKEND_URL}/interview/question/receive`);
        if (res.status !== 200) {
          alert('API returned non-200 status when loading questions: ${res.status}');
          return;
        }
      
        app.questions = res.data['questions'];
      }
    },
    //FrontEnd methods here:
    computed: {
      filteredQuestions() {
        const questions = this.questions
          .filter(question => this.filterRegularity === -1 || question.regularity === this.filterRegularity)
          .filter(question => this.filterDifficulty === -1 || question.difficulty === this.filterDifficulty);

        return questions.filter(question => {
          return question.question.toLowerCase().includes(this.search.toLowerCase());
        });
      }
    },
    beforeMount() {
      this.loadQuestions();
    }
});


//any functions outside of vue here:

//---------------------------------------------------------
// Dummies