from database.init_db import SessionLocal
from models.produit import Produit

def afficher_produits():
    session = SessionLocal()
    try:
        produits = session.query(Produit).all()
        if not produits:
            print("Aucun produit trouvé.")
            return

        print("\n--- Liste des produits ---")
        for produit in produits:
            print(f"[{produit.id}] {produit.nom} - {produit.prix:.2f}$ (Stock: {produit.quantite_stock})")
    finally:
        session.close()
