# ADR 005 – Ajout de l'observabilité via Prometheus et Grafana

## Statut
Accepté

## Utilisation de Prometheus et Grafana
L'application a été instrumentée pour collecter des métriques via Prometheus et les visualiser avec Grafana, afin de suivre les "Golden Signals" : latence, trafic, erreurs et saturation.

## Contexte
Dans un contexte de tests de charge et d'exploitation multi-utilisateurs, il est devenu essentiel de disposer d'outils d'observabilité pour détecter les goulets d'étranglement, surveiller la santé du système et identifier les points à optimiser.

## Conséquences
- Prometheus et Grafana ont été ajoutés dans l'environnement Docker Compose.
- L'application Django expose des métriques via un endpoint compatible Prometheus (grâce à django-prometheus).
- Des tableaux de bord ont été créés pour visualiser la latence, les erreurs, le trafic et les requêtes lentes.
- Les tests de charge sont corrélés aux métriques collectées pour guider les optimisations futures.

## Conformité
Cette décision respecte les objectifs de qualité de service (QoS), de résilience et d'amélioration continue.

## Notes
Ces outils permettront à terme d'automatiser certaines alertes et de préparer l'application à un déploiement en environnement de production.