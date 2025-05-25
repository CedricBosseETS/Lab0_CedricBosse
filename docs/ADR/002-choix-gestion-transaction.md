# ADR 004 – Gestion des transactions et cohérence des stocks

## Statut  
Accepté

## Transactions pour la gestion du stock  
Pour assurer la cohérence du stock lors d’une vente, on utilise des transactions SQL via SQLAlchemy.

## Contexte  
Lorsqu’une vente est enregistrée, il faut mettre à jour la quantité disponible des produits.  
Plusieurs utilisateurs peuvent utiliser la caisse simultanément, ce qui demande une gestion correcte des accès concurrents.

Plutôt que d’implémenter des verrous complexes, on utilise une transaction unique qui valide ou annule toutes les modifications selon le succès ou l’échec de l’opération.

## Conséquences  
- Le stock n’est modifié que si la vente est validée.  
- En cas d’erreur (stock insuffisant, produit non trouvé), la base n’est pas modifiée.  
- La logique est centralisée dans la fonction `creer_vente`.

## Conformité  
- On utilise `try/except` avec rollback pour gérer les erreurs.  
- Les tests vérifient que le stock reste cohérent après plusieurs ventes.  
- Les modifications du stock passent toujours par une transaction.

## Notes  
- Si le nombre d’utilisateurs augmente, on pourra envisager des verrous plus spécifiques.  
- Cette méthode est simple et fiable pour notre contexte actuel.
