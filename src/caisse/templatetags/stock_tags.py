"""
Filtres personnalisés liés à l'affichage du stock local dans les templates Django.
"""

from django import template

register = template.Library()

@register.filter
def stock_local(stock_local_dict, produit_id):
    """
    Retourne la quantité en stock local pour un produit donné.

    Args:
        stock_local_dict (dict): Un dictionnaire avec les identifiants de produit comme clés.
        produit_id (int): L'identifiant du produit recherché.

    Returns:
        int: La quantité en stock local pour ce produit, ou 0 si non trouvée.
    """
    return stock_local_dict.get(produit_id, 0)
