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