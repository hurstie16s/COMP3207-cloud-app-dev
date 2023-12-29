function getHelper(data, endpoint) {

}

function postHelper(data, endpoint) {

}

function putHelper(data, endpoint) {

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
      } else {return null;}
    }
}

function logout() {
    document.cookie = 'user=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'; //date is the past so browser removes it
    window.location.href = '/';
  }