# ADR 004 – Ajout d'un système de cache Redis pour les stocks

## Statut
Accepté

## Utilisation de Redis pour la cache
Un cache Redis a été introduit pour améliorer les performances de l'accès aux données de stock dans l'application Django.

## Contexte
Certaines opérations telles que la consultation du stock étaient très fréquentes, en particulier pendant les tests de charge. Ces accès répétés à la base de données MySQL entraînaient des ralentissements notables.

## Conséquences
- Un service Redis a été ajouté au fichier docker-compose.yml.
- Les fonctions de lecture des stocks utilisent maintenant django.core.cache.
- Un système d'invalidation du cache est mis en place lors des opérations critiques (vente, réapprovisionnement).
- Les performances lors de la consultation du stock ont significativement augmenté.

## Conformité
Cette amélioration respecte les objectifs de performance et de scalabilité de l'application.

## Notes
L'utilisation future d'un cache pour d'autres types de données est maintenant possible grâce à cette architecture.