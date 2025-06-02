from django.shortcuts import render, redirect
from caisse.models import Vente
from services import vente_service

def liste_ventes(request, magasin_id):
    ventes = Vente.objects.filter(magasin_id=magasin_id).order_by('-date_heure')
    return render(request, 'caisse/vente.html', {'ventes': ventes, 'magasin_id': magasin_id})

def annuler_vente(request, magasin_id, vente_id):
    if request.method == "POST":
        vente_service.annuler_vente(magasin_id, vente_id)
    return redirect('liste_ventes', magasin_id=magasin_id)
