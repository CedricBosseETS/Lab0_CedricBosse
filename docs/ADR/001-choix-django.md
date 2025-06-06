# ADR 001 – Passage d’une application console à une application web Django

## Statut  
Accepté

## Utilisation de Django  
L’application de caisse est passée d'une interface console à une interface web utilisant Django, tout en conservant la logique métier en Python.

## Contexte  
L’ancienne version était une application console utilisant SQLAlchemy pour la persistance. Elle devenait difficile à étendre, à tester dans un contexte multi-utilisateur, et à rendre conviviale.  
Le besoin d’une interface graphique, d’une meilleure organisation du code, et de fonctionnalités multi-sites plus complexes a justifié l’adoption de Django.

## Conséquences  
- Le projet utilise désormais le framework Django pour la structure MVC (Modèles, Vues, Templates).
- Le code a été réorganisé en services, vues modulaires et modèles Django.
- La réorganisation du code a pris énormément de temps et de travail à cause du mauvais état du code avant.
- La logique console a été supprimée au profit d’interactions HTTP avec gestion de session.
- Le déploiement est facilité grâce à la compatibilité de Django avec Docker.

## Conformité  
Cette décision respecte les objectifs de maintenabilité, de modularité et de facilité d'évolution du projet.

## Notes  
Cette transition ouvre la porte à l'intégration d'une API REST et d'une interface mobile.
