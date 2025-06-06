# Lab1_CedricBosse

## Description

Il s'agit d'une application **web** de caisse enregistreuse développée avec **Django** et une base de données **MySQL**.  
L'application supporte plusieurs magasins (multi-sites) ainsi que des entités administratives comme la maison mère et le centre logistique.  
Plusieurs caisses peuvent être utilisées simultanément avec une gestion cohérente des stocks et des ventes.  

L’application permet :
- La consultation et la recherche de produits par magasin
- La gestion d’un panier (ajout, retrait, affichage)
- La finalisation des ventes à partir du panier
- La gestion administrative (maison mère, centre logistique, rapports, approvisionnement)
- Le réapprovisionnement entre entités via le centre logistique

L'interface est construite en Django avec des vues modulaires, et la logique métier est bien séparée dans des services Python.


## Installation des dépendances (À la racine du projet) 

Sur un système Linux, installer Docker et Docker Compose si ce n’est pas déjà fait :  
sudo apt install docker docker-compose


## Instructions de lancement de l'application :
0. Pour utiliser l'application et avoir accès au site web, soit : http://10.194.32.173:8000/ , il est important d'être sur le même réseau que celui de l'école (ou d'utiliser le vpn)
1. docker compose down (pour fermer un conteneur déjà existant au cas où et -v pour détruite les volumes si nécéssaire)
2. docker compose build --no-cache
3. docker compose up

## Instructions de lancement des tests :
1. docker compose build --no-cache
2. docker compose up -d 
3. docker compose exec app pytest 

## Utilisation de l'application
La page d'accueil propose le choix entre ouvrir une caisse (choisir un magasin) ou accéder à l'administration.
Dans la caisse, il est possible de rechercher des produits, ajouter ou retirer des articles dans un panier, puis finaliser une vente.
Le panier est géré en session utilisateur, et la finalisation met à jour les stocks de façon atomique.
L’administration permet la gestion des entités (maison mère, centres logistiques), la modification des produits, le suivi des ventes et la gestion des approvisionnements entre magasins.

## Choix technologiques et justification

### Django + Python
Le passage à Django a permis de construire une interface web de manière relativement simple, facilitant la maintenance, les tests et l’évolution des fonctionnalités.
Python reste le langage principal purement par simplicité.

### MySQL comme base de données relationnelle  
MySQL est utilisé pour sa robustesse et sa compatibilité avec Django ORM. 
La gestion relationnelle permet de modéliser aisément les magasins, produits, ventes, et stocks.

### Docker & Docker Compose  
L'application tourne entièrement dans des conteneurs Docker. Cela évite les problèmes de configuration entre les machines. Docker Compose permet de démarrer la base de données et l’application en deux commandes rapide. Cela simplifie l’installation et garantit un environnement reproductible.

### Pytest pour les tests  
Pytest est utilisé pour écrire et lancer les tests automatisés. Les tests tournent aussi dans les conteneurs Docker, dans le même environnement que l’application principale. Cela permet de s’assurer que le code fonctionne partout de la même façon.

### Organisation modulaire du code  
Le projet est organisé en plusieurs dossiers sous src/caisse/ :

models/ : les modèles Django

services/ : logique métier regroupée en services spécialisés (stock, vente, magasin, produit)

views/ : vues Django regroupées par fonctionnalité (caisse, panier, administration, accueil)

templates/ : fichiers HTML pour les interfaces utilisateur

Cette organisation facilite la maintenance, la réutilisation et les évolutions futures.