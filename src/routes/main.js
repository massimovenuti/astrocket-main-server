const express = require('express');
const mainCtrl = require('../controllers/main');

const router = express.Router();

router.post('/addGameServer', mainCtrl.addGameServer);
router.get('/', mainCtrl.listGameServer);
// router.delete('/', mainCtrl.deleteGameServer);

module.exports = router;
