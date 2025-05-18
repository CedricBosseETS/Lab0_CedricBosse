# Lab0_CedricBosse
## Description
Il s'agit d'un simple hello world qui est affiché dans la console.

## Architecture
Comme il s'agit d'un simple hello world, l'architecture est très simple et rudimentaire. Le fichier de helloworld.py est à la racine et le fichier de tests ainsi que les fichiers nécessaires au fonctionnement de docker. Avec un projet plus gros j'aurais séparé les fichiers de tests et les fichiers principaux dans des dossiers séparés. Comme ça, seuls les fichiers de docker et le ReadMe seraient à la racine.

## Instructions de clonage : 
1. Créer un dossier qui va contenir le projet.
2. Ouvrir un CMD
3. Faire : CD "path jusqu'au dossier créé"
4. Faire la commande git clone "url du projet git". Puis, faire cd Lab0_CedricBosse
De cette manière, vous devriez être placé à la racine du projet.

## Installation des dépendances (toujours à la racine du projet) 
Faire les commandes suivantes dans un environnement linux :
sudo apt install python3-pip
sudo apt install python3-pytest
sudo apt install docker-compose
sudo apt install pylint

## Instructions de lancement du conteneur local :
1. docker compose build
2. docker compose down (pour fermer un conteneur déjà existant au cas où)
3. docker compose up
Ça m'a suffi pour une exécution locale du conteneur.

# Fonctionnement du pipeline CI/CD : après chaque push et chaque merge, le pipeline va automatiquement s'éxécuter et va éxucuter trois étapes. Il commence par vérifier la syntaxe du code, puis il fait les tests unitaires.
Enfin, il finit avec le build et le push de l'image  sur Docker Hub.  

# Voici une image d'une exécution réussie du pipeline :
![alt text](image.png)