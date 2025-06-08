"""Vues liées à l'affichage des magasins."""
from django.shortcuts import render

def page_magasins(request):
    """Affiche la page magasins, la liste sera chargée par JS via l’API."""
    return render(request, "magasins.html")

