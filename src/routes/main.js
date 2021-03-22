const express = require('express');
const mainCtrl = require('../controllers/main');

const router = express.Router();

router.post('/GameServer', mainCtrl.addGameServer);
router.get('/list', mainCtrl.listGameServer);
// router.delete('/GameServer', mainCtrl.deleteGameServer);

module.exports = router;
