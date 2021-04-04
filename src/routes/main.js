const express = require('express');
const mainCtrl = require('../controllers/main');

const router = express.Router();

router.post('/GameServer', mainCtrl.addGameServer);
router.get('/list', mainCtrl.listGameServer);
router.delete('/GameServer', mainCtrl.deleteGameServer);
router.put('/GameServer', mainCtrl.updateGameServer);
router.post('/alive', mainCtrl.aliveMainServer);

module.exports = router;
