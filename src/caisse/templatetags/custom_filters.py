"""
Filtres personnalisés pour les templates Django de l'application caisse.
"""

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Récupère la valeur associée à une clé dans un dictionnaire.

    Args:
        dictionary (dict): Le dictionnaire à interroger.
        key (str): La clé à rechercher.

    Returns:
        La valeur associée à la clé, ou None si la clé est absente.
    """
    return dictionary.get(key)
