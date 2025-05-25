# ADR 001 – Choix du SGBD relationnel : MySQL

## Statut  
Accepté

## MySQL comme base de données  
Le choix pour la base de données de l’application est MySQL.

## Contexte  
L’application de caisse doit gérer des entités relationnelles comme les produits, les ventes, et leurs relations.  
Plusieurs options ont été étudiées : MySQL, PostgreSQL, SQLite, MongoDB.

MySQL a été retenu parce que :  
- Il est bien supporté dans Docker.  
- Il est largement utilisé et bien documenté.  
- Il offre une bonne compatibilité avec SQLAlchemy, l’ORM utilisé.  
- Il est simple à mettre en place pour un projet de cette taille.

SQLite a été envisagé, mais la gestion de la concurrence pose problème. PostgreSQL est robuste, mais plus complexe. MySQL est un bon compromis pour ce projet.

## Conséquences  
- Le modèle de données suit une structure relationnelle stricte.  
- Les requêtes doivent respecter la syntaxe MySQL.  
- Les tests et le pipeline CI utilisent un conteneur MySQL.

## Conformité  
- Docker Compose initialise un conteneur MySQL configuré correctement.  
- Toutes les transactions passent par SQLAlchemy (`SessionLocal`) et respectent le modèle.  
- La migration reste possible grâce à l’abstraction de SQLAlchemy.

## Notes  
- Une migration vers PostgreSQL pourra être envisagée si les besoins évoluent.  
- Ce choix convient bien pour un projet local ou une petite structure, ce qui correspond à notre usage.
