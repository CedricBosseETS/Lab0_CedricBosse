# ADR-001 : Migration vers une architecture microservices

## Statut
Accepté

## Division du monolithe en plusieurs vrai services indépendants
Pour améliorer l'architecture et se défaire du monolithe, il as été séparé en plusieurs services.

## Contexte
L’application initiale était monolithique. Le couplage fort entre les modules posait des problèmes de maintenabilité et de scalabilité.
Il as donc été décider de tout séparer les services en conteneurs individuels pour réduire le couplage le plus possible.

## Conséquences
- Meilleure séparation des responsabilités.
- Complexité accrue en termes de communication inter-services.
- Besoin d'un orchestrateur (Docker Compose).
- Code actuel non fonctionnel

## Conformité
Cette décision aide à migré toujours plus vers une bonne architecture DDD

## Notes
Ce sont les premières étapes vers des microservices, mais la BD n'est pas encore partagée donc ce n'est pas un microservice complet.