const express = require('express');
const bodyParser = require('body-parser');
const mainRoutes = require('./routes/main');

const app = express();

app.use(bodyParser.json());
app.use('/main', mainRoutes);

module.exports = app;
