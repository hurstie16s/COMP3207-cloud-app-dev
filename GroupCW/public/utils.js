async function getHelper(data, endpoint) {
  try {
    const response = await axios({
      method: 'GET',
      url: BACKEND_URL + endpoint,
      headers: {
        'Authorization': window.localStorage.getItem('token'),
        'Content-Type': 'application/json'
      },
      data: data
    })
    console.log('Response:', response);
    return response;
  } catch (error) {
    console.log('ERROR:', error);
    return error.response;
  }
}

async function postHelper(data, endpoint) {
  try {
    const response = await axios({
      method: 'POST',
      url: BACKEND_URL + endpoint,
      headers: {
        'Authorization': window.localStorage.getItem('token'),
        'Content-Type': 'application/json'
      },
      data: data
    })
    console.log('Response:', response);
    return response;
  } catch (error) {
    console.log('ERROR:', error);
    return error.response;
  }
}

async function putHelper(data, endpoint) {
  try {
    const response = await axios({
      method: 'PUT',
      url: BACKEND_URL + endpoint,
      headers: {
        'Authorization': window.localStorage.getItem('token'),
        'Content-Type': 'application/json'
      },
      data: data
    })
    console.log('Response:', response);
    return response;
  } catch (error) {
    console.log('ERROR:', error);
    return error.response;
  }
}

function setSessionData(username, token) {
  window.localStorage.setItem('user', username);
  window.localStorage.setItem('token', token);
}

function getLoggedInUsername() {
  return window.localStorage.getItem('user') || null;
}

function forceLoggedIn() {
  if (!window.localStorage.getItem('user') || !window.localStorage.getItem('token')) {
    window.location.href = '/sign-in';
  }
}

function logout() {
  window.localStorage.clear();
  window.location.href = '/';
}

function getAccount(user) {
  window.location.href = `/account/${user}`;
}

function getMyAccount() {
  window.location.href = `/account/${app.user}`;
}

function mapDifficultyToInt(difficulty) {
  // Map difficulty string to corresponding integer value
  switch (difficulty) {
      case 'Beginner':
          return 0;
      case 'Intermediate':
          return 1;
      case 'Advanced':
          return 2;
      default:
          return 0; // Default or error case
  }
}

function mapRegularityToInt(regularity) {
  // Map regularity string to corresponding integer value
  switch (regularity) {
      case 'Standard':
          return 0;
      case 'Infrequent':
          return 1;
      case 'Unusual':
          return 2;
      default:
          return 0; // Default or error case
  }
}