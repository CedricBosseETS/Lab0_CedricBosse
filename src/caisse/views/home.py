"""Vue pour la page d'accueil."""

from django.shortcuts import render

def home_view(request):
    """Affiche la page d'accueil."""
    return render(request, 'home.html')
