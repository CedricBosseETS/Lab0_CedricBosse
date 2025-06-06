# ADR 002 – Séparation de la logique métier dans des services Python

## Statut  
Accepté

## Séparation des services
La logique métier (gestion du panier, des ventes, du stock, etc.) a été séparée dans des services Python indépendants des vues Django.

## Contexte  
Dans un souci de clarté, testabilité et réutilisabilité, il était nécessaire de sortir la logique métier des vues Django pour éviter des views énormes et respecter le principe de séparation des responsabilités.

## Conséquences  
- Création de modules `magasin_service.py`, `vente_service.py`, `produit_service.py`, `stock_service.py`.
- Les vues appellent des fonctions de services pour exécuter les traitements métiers.
- Les tests unitaires peuvent cibler ces services sans passer par l’interface HTTP.

## Conformité  
Cette décision respecte les bonnes pratiques Django, les principes SOLID et facilite l’ajout futur d’une API ou d’un frontend alternatif.

## Notes  
Des validations supplémentaires sont intégrées côté services pour assurer la robustesse métier indépendamment des vues.
