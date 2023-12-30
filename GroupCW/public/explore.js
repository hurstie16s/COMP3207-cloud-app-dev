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
      
    },
    //Js Methods here:
    methods: {
      logout() {
        logout(); //utils.logout
      },

      async loadQuestions() {
        const res = await axios.get(`${BACKEND_URL}/interview/question/receive`);
        if (res.status !== 200) {
          alert('API returned non-200 status when loading questions: ${res.status}');
          return;
        }
      
        app.questions = res.data['questions'];
      },

      navToQuestion(questionId) {
        window.location.href = `/question/${questionId}`;
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
      this.user = getUserCookie();
      this.loadQuestions();
    }
});


//any functions outside of vue here:

//---------------------------------------------------------
// Dummies