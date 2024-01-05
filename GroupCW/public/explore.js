var app = new Vue({
    el: '#explore',
    //All data here
    data: {
      user: null,
      search: '',
      filterRegularity: -1, // -1 = all,
      filterDifficulty: -1, // -1 = all,
      questions: [],
      newQuestion: {text: "", difficulty: "Beginner", regularity: "Standard"}
    },
    //On Awake methods here:
    mounted: function() {
      
    },
    //Js Methods here:
    methods: {
      async loadQuestions() {
        console.log("retrieving Qs")
        const res = await axios.get(`${BACKEND_URL}/interview/question/receive`);
        if (res.status !== 200) {
          alert(`API returned non-200 status when loading questions: ${res.status}`);
          return;
        }
      
        app.questions = res.data['questions'];
        app.questions.sort((a, b) => {
          return b.numberOfResponses - a.numberOfResponses;
        })
      },

      navToQuestion(questionId) {
        window.location.href = `/question/${questionId}`;
      },

      async submitQuestion(newQuestion, regularity, difficulty) {
        const data = {
          question: newQuestion,
          difficulty: mapDifficultyToInt(difficulty),
          regularity: mapRegularityToInt(regularity)
        };
        document.getElementById('question-submission-spinner').classList.toggle('hidden');
        const res = await axios.post(`${BACKEND_URL}/interview/question/submit`, data);
        if (res.status > 299) {
          alert(`API returned non-200 status when submitting comment: ${res.status}` + (res.data ? `: ${res.data.msg}` : ''));
          return;
        }
        document.getElementById('question-submission-spinner').classList.toggle('hidden');
        addNotification('Question Submitted')
        this.newQuestion.text = '';
        this.loadQuestions();
      },
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
      },
      topQuestions() {
        return this.questions.slice(0, 3);
      }
    },
    beforeMount() {
      forceLoggedIn();
      this.user = getLoggedInUsername();
      this.loadQuestions();
    }
});
