from caisse.models import Magasin

def get_all_magasins():
    return Magasin.objects.all()
