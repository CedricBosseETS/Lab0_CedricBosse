# Lab1_CedricBosse
## Description
Il s'agit d'une application console qui simule une caisse enregistreuse. Les caisses communiquent avec une base de données MySQL, 
et plusieurs caisses peuvent être utilisées en même temps.

## Installation des dépendances (À la racine du projet) 
Faire la commande suivante dans un environnement linux pour pouvoir utiliser l'application:
sudo apt install docker-compose

## Instructions de lancement de l'application :
1. docker-compose down -v --remove-orphans (pour fermer un conteneur déjà existant au cas où)
2. docker compose build --no-cache
3. docker compose run web

## Instructions de lancement des tests :
1. docker-compose down -v --remove-orphans (pour fermer un conteneur déjà existant au cas où)
2. docker compose build --no-cache
3. docker compose run web pytest

## Utilisation de l'application
L'application est très simple à utiliser. Une fois que les commandes de lancement sont effectuées, un menu s'affiche dans la console. Il suffit de suivre les instructions, soit en choisissant un numéro, soit en entrant un nom selon l'option choisie.

## Choix technologiques et justification

### MySQL comme base de données relationnelle  
MySQL a été choisi comme SGBD relationnel, car il est bien supporté dans Docker, largement utilisé, et fonctionne très bien avec SQLAlchemy. Il permet de gérer les relations entre les entités comme les produits, les ventes et les lignes de vente.

### Python + SQLAlchemy  
Python est un langage simple et rapide à prendre en main. SQLAlchemy permet d’interagir avec la base de données en utilisant des objets Python, ce qui rend le code plus lisible et plus facile à maintenir. Cela permet aussi de changer de SGBD plus tard si nécessaire.

### Docker & Docker Compose  
L'application tourne entièrement dans des conteneurs Docker. Cela évite les problèmes de configuration entre les machines. Docker Compose permet de démarrer la base de données et l’application en deux commandes rapide. Cela simplifie l’installation.

### Pytest pour les tests  
Pytest est utilisé pour écrire et lancer les tests automatisés. Les tests tournent aussi dans les conteneurs Docker, dans le même environnement que l’application principale. Cela permet de s’assurer que le code fonctionne partout de la même façon.

### Organisation modulaire du code  
Le code est séparé en plusieurs parties : les modèles, les services, et l’interface console. Cette structure rend le projet plus propre et plus facile à faire évoluer ou à tester.


