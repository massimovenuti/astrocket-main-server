const axios = require('axios');
const ipRegex = require('ip-regex');

var server_list = [];

function index_research(server_list,name)
{
    for (i = 0;i<server_list.length;i++)
        if (server_list[i].name == name)
            return i;

    return -1;
}

function port_research(server_list,port)
{
    for (i = 0;i<server_list.length;i++)
        if (server_list[i].port == port)
            return i;

    return -1;
}

console.log(server_list);

exports.addGameServer = (req, res) => {
    if (!req.body.port || !req.body.address) {
        res.status(404).json("Paramètre(s) manquant(s)");
    } else if (!ipRegex().test(req.body.address)) {
        res.status(405).json("Addresse invalide");
    } else if (typeof(req.body.port) != "number"){
        res.status(406).json("Port invalide");
    } else {
        axios.post('https://auth.aw.alexandre-vogel.fr/user/check', { token: req.headers.user_token })
        .then((res_user) => {
            if (res_user.data.role != 'A'){
                res.status(401).json("L'utilisateur n'a pas les droits");
            } else {
    
                if ((port_research(server_list,req.body.port) != -1)){
                    res.status(402).json("Port déjà utilisé");
                } else{
                    axios.post('https://auth.aw.alexandre-vogel.fr/server/add', { user_token: req.headers.user_token, name: req.body.name })
                    .then((res_server) => {
                        server_list.push({"name" : req.body.name, "address":req.body.address ,"port": req.body.port,"players": 0});
                        res.status(200).send(res_server.data.token);
                    })
                    .catch(err => {
                        if (err.response && (err.response.status == 400 || err.response.status == 401))
                            res.status(404).json("Paramètre(s) manquant(s)");
                        else
                            res.status(403).json("Nom du serveur déjà existant")
                    })
                }
            }
        })
        .catch(err => {
            if (err.response && (err.response.status == 400 || err.response.status == 401))
                res.status(404).json("Token manquant ou invalide");
            else
                res.status(500).json("Erreur interne au serveur");
        });
    }
}


exports.listGameServer = (req, res) => {
    axios.post('https://auth.aw.alexandre-vogel.fr/user/check', { token: req.headers.user_token })
    .then((res_auth) => {
        res.status(200).json(server_list);
    })
    .catch(err => {
        if (err.response && err.response.status == 400)
            res.status(400).json("Paramètre(s) manquant(s) ou invalide(s)");
        else if (err.response && err.response.status == 401)
            res.status(401).json("Token invalide");
        else
            res.status(500).json("Erreur interne au serveur");
    });
}


exports.deleteGameServer = (req, res) => {
    axios.post('https://auth.aw.alexandre-vogel.fr/server/remove', {name: req.body.name, token: req.headers.user_token})
    .then((res_auth) => {
        const idx = index_research(server_list,req.body.name);;
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
    if (req.body.name == undefined) {
        res.status(403).json("Nom manquant");
    } else if (req.body.playersNB == undefined) {
        res.status(404).json("Nombre de joueurs manquant");
    } else if (typeof(req.body.playersNB) != "number"){
        res.status(405).json("Nombre de joueurs invalide");
    } else {
        axios.post('https://auth.aw.alexandre-vogel.fr/server/check', {token: req.headers.token})
        .then((res_auth) => {
            const idx = index_research(server_list,req.body.name);
            if (idx == -1)
                res.status(402).json("Le serveur n'existe pas");
            else {
                server_list[idx].players = req.body.playersNB;
                res.status(200).json("Le nombre de joueurs a bien été modifié");
            }
        })
        .catch((err) => {
            if (err.response && err.response.status == 401)
                res.status(401).json("Token non valide");
            else 
                res.status(500).json("Erreur interne au serveur");
        });
    }
}

exports.aliveMainServer = (req, res) => {
    if(!req.body[0]){
        res.status(400).send('Paramètre(s) manquant(s) ou invalide(s)');
    } else {
        var length = req.body.length;
        var elem = req.body[Math.floor(Math.random() * (length-1))];
        axios.post('https://auth.aw.alexandre-vogel.fr/server/check', {token: elem.serverToken})
        .then((res_auth) => {
            const idx = index_research(server_list,res_auth.data.name);
            if(idx == -1)
                res.status(402).send('L\'un des ServerToken ne se trouve pas dans server_list');
            else
                res.status(200).send('Le Main Server est toujours opérationnel');
        })
        .catch((err) => {
            if (err.response && err.response.status == 401)
                res.status(401).send('L\'un des ServerToken est invalide');
            else
                res.status(500).json("Erreur interne au serveur");
        });
    }
}
