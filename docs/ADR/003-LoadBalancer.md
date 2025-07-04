# ADR 003 – Mise en place d'un Load Balancer avec Docker

## Statut
Accepté

Utilisation d'un Load Balancer

L'application Django est maintenant déployée derrière un Load Balancer (NGINX) avec plusieurs instances de l'application via Docker Compose.

## Contexte
Afin d'améliorer la résilience, la disponibilité et la scalabilité de l'application, il a été nécessaire d'introduire un système de load balancing pour répartir la charge entre plusieurs conteneurs Django.

## Conséquences
- Le fichier docker-compose.yml a été modifié pour inclure plusieurs instances de l'application.
- Un service NGINX a été ajouté pour servir de point d'entrée avec une stratégie de round-robin.
- L'application est plus résiliente à l'échec d'une instance.
- Des ajustements ont été faits pour s'assurer de la compatibilité avec les sessions et la base de données partagée.

## Conformité
Cette décision est alignée avec les objectifs de performance, de disponibilité et d'évolutivité de l'application.

# Notes
Cette évolution prépare l'application à une mise en production plus robuste et à des tests de charge plus réalistes.