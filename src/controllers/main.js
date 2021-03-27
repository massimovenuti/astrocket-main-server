const  http  = require('http');
const {all} = require('../app');
const axios = require('axios');
const  dotenv  = require('dotenv');
const ipRegex = require('ip-regex');
dotenv.config()

var server_list = [{"name" : "Orion", "address" : "local", "port" : 4040, "players" : 10}];



exports.addGameServer = (req, res) => {
    axios.post('http://localhost:8080/user/check', { token: req.headers.user_token })
    .then((res_user) => {
        if (res_user.role != 'A'){
            res.status(401).json("L'utilisateur n'a pas les droits")
        } else {
            const exists = 0;
            server_list.foreach(elem => {
                if (elem['port'] == req.body.port)
                    exists = 1;
            })
            if (!ipRegex.test(req.body.address))
                res.status(404).json("Paramètre(s) manquant(s) ou invalide(s)");

            const num_regex = new RegExp('\\[0-9]{4}');
            if (!req.body.port.match(num_regex))
                res.status(404).json("Paramètre(s) manquant(s) ou invalide(s)");

            if (exists){
                res.status(402).json("Port déjà utilisé");
            } else{
                axios.post('http://localhost:8080/server/add', { token: req.headers.user_token, name: req.body.name })
                .then((res_server) => {
                    server_list.push({"name" : req.body.name, "address":req.body.address ,"port": req.body.port,"players": 0});
                    res.status(200).json("Un nouveau serveur a bien été créé");
                })
                .catch(err => {
                    if (err.response && (err.response.status == 400 || err.response.status == 401))
                        res.status(404).json("Paramètre(s) manquant(s) ou invalide(s)");
                    else
                        res.status(403).json("Nom du serveur déjà existant")
                })
            }
        }
    })
    .catch(err => {
        if (err.response && err.response.status == 400)
            res.status(404).json("Paramètre(s) manquant(s) ou invalide(s)");
        else
            res.status(500).json("Erreur interne au serveur");
    });
}


exports.listGameServer = (req, res) => {
    axios.post('http://localhost:8080/user/check', { token: req.headers.userToken })
    .then((res_auth) => {
        res.status(200).json(server_list);
    })
    .catch(err => {
        if (err.response && err.response.status == 401)
            res.status(401).json("Token invalide");
        else
            res.status(500).json("Erreur interne au serveur");
    });
}


exports.deleteGameServer = (req, res) => {
    axios.post('http://localhost:8080/server/remove', {name: req.body.name, token: req.headers.userToken})
    .then((res_auth) => {
        const idx = server_list.indexOf(req.body.name);
        server_list.splice(idx);
        res.status(200).json("Le serveur a bien été supprimé");
    })
    .catch((err) => {
        if (err.response && err.response.status == 400)
            res.status(400).json("Paramètre(s) manquant(s) ou invalide(s)");
        else if (err.response && err.response.status == 401)
            res.status(401).json("Token non valide");
        else if (err.response && err.response.status == 402)
            res.status(402).json("L'utilisateur n'a pas les droits");
        else if (err.response && err.response.status == 403)
            res.status(403).json("Le serveur n'existe pas");
        else 
            res.status(500).json("Erreur interne au serveur");
    })
}

exports.updateGameServer = (req, res) => {
    axios.post('http://localhost:8080/server/check', {token: req.headers.servToken})
    .then((res_auth) => {
        const idx = server_list.indexOf({name: req.body.name});
        if (idx == -1)
            res.status(402).json("Le serveur n'existe pas");
        else {
            server_list[idx][players] = req.body.playersNB;
            res.status(200).json("Le nombre de joueurs a bien été modifié");
        }
    })
    .catch((err) => {
        if (err.response && err.response.status == 400)
            res.status(400).json("Paramètre(s) manquant(s)");
        else if (err.response && err.response.status == 401)
            res.status(401).json("Token non valide");
        else 
            res.status(500).json("Erreur interne au serveur");
    })
}

exports.aliveMainServer = (req, res) => {
    if(!req.body){
        res.status(400).send('Paramètre(s) manquant(s) ou invalide(s)');
    } else {
        var length = req.body.length;
        var elem = req.body[getRandom(length)];
        knex('servers').select('serverName').where({ serverToken: elem })
            .then((res) => {
                if(res[0]) {
                    const exists = 0;
                    server_list.foreach(elem => {
                        if (elem['name'] == res[0].serverName)
                            exists = 1;
                    })
                    if(exists){
                        res.status(200).send('Le Main Server est toujours opérationnel');
                    } else {
                        res.status(402).send('L\'un des ServerToken ne se trouve pas dans server_list');
                    }
                } else {
                    res.status(401).send('L\'un des ServerToken est invalide');
                }
            })
            .catch((err) => {
                res.status(500).json("Erreur interne au serveur");
            });    
    }
}
