async function getHelper(data, endpoint) {
  try {
    const response = await axios({
      method: 'GET',
      url: BACKEND_URL + endpoint,
      headers: {
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

function setCookie(username) {
  // Set the 'user' cookie with an expiration time of 1 hour
  const expirationDate = new Date();
  expirationDate.setTime(expirationDate.getTime() + (1 * 60 * 60 * 1000)); // 1 hour
  document.cookie = `user=${username}; expires=${expirationDate.toUTCString()}; path=/`;
}

function getUserCookie() {
  // Function to read the value of the 'user' cookie
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === 'user') {
      return value;
    } else { return null; }
  }
}

function logout() {
  document.cookie = 'user=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'; //date is the past so browser removes it
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