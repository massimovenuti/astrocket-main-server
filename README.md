# Main server

## Description

Pour permettre aux joueurs de jouer en réseau, nous avons utilisés deux types de serveurs: les *Game Servers* et les *Main Servers*.
Les *Main Servers* se divisent en deux catégories. Premièrement, le *big Main* est semblable à une API. Il tient à jour une liste des serveurs de jeu disponibles, permet l'ajout et la suppression de ces derniers dans la liste. De ce fait, il permet aux joueurs d'avoir une liste des serveurs dispoibles au moment où le client souhaite jouer. Deuxièment, les *main* sont des programmes permettant de créer des sessions de jeu. Leur rôle va être de vérifier le bon fonctionnement de ces sessions (Pas de crash, etc...). De plus, ils servent d'intermédiaire entre les sessions et le *big Main*.

Aussi, le *big Main* est unique, alors que l'on peut utiliser plusieurs *main*, par exemple si l'on utilise plusieurs ordinateurs pour héberger nos sessions de jeu.

## Déploiement

### Big Main
Pour déployer votre big Main, dnas le répertoire du projet,
entrez en ligne de commande :
```
cd bigMain/src
node server.js
```

### Main
Pour déployer votre main server, dans le répertoire du projet,
entrez en ligne de commande :

```
cd main/
python3 server.py
```
