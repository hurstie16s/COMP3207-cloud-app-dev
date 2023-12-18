/*
Vue BackEnd, if possible since we don't need person to person communication do everything on Vue
*/

'use strict';

//Set up express
const express = require('express');
const app = express();
const server = require('http').Server(app);

// URL of the backend API
const BACKEND_ENDPOINT = process.env.BACKEND || 'http://localhost:8181';

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
  res.render('root');
});



//Start server
if (module === require.main) {
    startServer();
  }
  
module.exports = server;
  