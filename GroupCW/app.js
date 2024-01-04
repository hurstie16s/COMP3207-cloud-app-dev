/*
Vue BackEnd, if possible since we don't need person to person communication do everything on Vue
*/

'use strict';

//Set up express
const express = require('express');
const app = express();
const server = require('http').Server(app);
const cookieParser = require('cookie-parser');
app.use(cookieParser());

// URL of the backend API
const BACKEND_ENDPOINT = process.env.BACKEND || 'http://localhost:7071';
const options = {
  BACKEND_URL: BACKEND_ENDPOINT,
  PRODUCTION: process.env.PRODUCTION === 'true',
};

//Start the server
function startServer() {
    const PORT = process.env.PORT || 8080;
    server.listen(PORT, () => {
        console.log(`Server listening on port ${PORT}`);
    });
}

//Setup static page handling
app.set('view engine', 'ejs');
app.use('/static', express.static('public'));

//Handle client interface on /
app.get('/', (req, res) => {
  res.render('landing', options);
});

app.get('/sign-in', (req, res) => {
  res.render('sign-in', options);
});

app.get('/sign-up', (req, res) => {
  res.render('sign-up', options);
});

app.get('/reset-password', (req, res) => {
  res.render('reset-password', options);
});

app.get('/set-new-password', (req, res) => {
  res.render('set-new-password', options);
});

app.get('/explore', (req, res) => {
  res.render('explore', options);
});

app.get('/question/:id', (req, res) => {
  res.render('question', Object.assign({id: req.params['id']}, options));
});

app.get('/account/:user', (req, res) => {
  res.render('account', Object.assign({id: req.params['user']}, options));
});


//Start server
if (module === require.main) {
    startServer();
  }
  
module.exports = server;
  