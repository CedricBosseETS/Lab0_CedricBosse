# ADR 002 – Utilisation d’un API Gateway (NGINX) pour exposer les services

## Statut  
Accepté

## Séparation des services
La logique métier (gestion du panier, des ventes, du stock, etc.) a été séparée dans des services Python indépendants des vues Django.

## Contexte  
Chaque service expose sa propre API sur le port 5000. Il fallait un point d’entrée unique pour le frontend et les appels API.

## Conséquences  
- Simplifie l’accès via /api/... pour tous les services.
- Permet d’ajouter des headers, gestion CORS, auth à l’entrée.
- Load balancing possible à travers upstream.

## Conformité  
Cette décision respecte les standards d'API en microservices et permet le bon routing et la protection des requêtes.

## Notes  
Notes : Actuellement statique, mais pourra être rendu dynamique avec Kong ou KrakenD.
