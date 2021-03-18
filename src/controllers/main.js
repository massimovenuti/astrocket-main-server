const  http  = require('http');
const {all} = require('../app');
const axios = require('axios');
const  dotenv  = require('dotenv')
dotenv.config()

var server_list = [{"name" : "Orion", "address" : "local", "port" : 4040, "players" : 10}];



exports.addGameServer = (req, res) => {

    axios.post('http://localhost:8080/user/check', { token: req.headers.user_token })
    .then((res_user) => {
        if (res_user.role != 'A'){
            res.status(401).json("L'utilisateur n'a pas les droits")
        } else {
            axios.post('http://localhost:8080/server/add', { token: req.headers.user_token, name: req.body.name })
            .then((res_server) => {
                const exists = 0;
                server_list.foreach(elem => {
                    if (elem['port'] == req.body.port)
                        exists = 1;
                    })

                if (exists){
                    res.status(402).json("Port déjà utilisé");
                } else{
                    server_list.push({"name" : req.body.name, "address":req.body.address ,"port": req.body.port,"players": 0});
                    res.status(200).json("Un nouveau serveur a bien été créé");
                }
            })
            .catch(err => {
                if (err.response && (err.response.status == 400 || err.response.status == 401))
                    res.status(404).json("Paramètre(s) manquant(s) ou invalide(s)");
                else
                    res.status(403).json("Nom du serveur déjà existant")
            })
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
    axios.post('http://localhost:8080/user/check', { token: req.headers.user_token })
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

/*
exports.deleteGameServer = (req, res) => {

}
*/
