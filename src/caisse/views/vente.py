"""Vues liées à la gestion des ventes dans l'application caisse."""

from django.shortcuts import render, redirect
from vente_service.models import Vente
from vente_service.services import vente_service


def liste_ventes(request, magasin_id):
    """Affiche la liste des ventes pour un magasin donné."""
    ventes = Vente.objects.filter(magasin_id=magasin_id).order_by('-date_heure')
    return render(request, 'caisse/vente.html', {'ventes': ventes, 'magasin_id': magasin_id})


def annuler_vente(request, magasin_id, vente_id):
    """Annule une vente spécifique après une requête POST."""
    if request.method == "POST":
        vente_service.annuler_vente(magasin_id, vente_id)
    return redirect('liste_ventes', magasin_id=magasin_id)
