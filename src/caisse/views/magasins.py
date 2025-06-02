from django.shortcuts import render
from services import magasin_service

def page_magasins(request):
    print("page_magasins appelée")
    magasins = magasin_service.get_only_magasins()
    print(f"Magasins récupérés : {magasins}")
    return render(request, "magasins.html", {"magasins": magasins})
