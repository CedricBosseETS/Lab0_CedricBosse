"""Ce module s'occupe de gérer les accès à la DB pour tout ce qui touche aux produits"""
from database.init_db import SessionLocal
from models.produit import Produit

def afficher_produits():
    """Affiche tout les produits, leurs prix unitaire et la quantité disponible"""
    session = SessionLocal()
    try:
        produits = session.query(Produit).all()
        if not produits:
            print("Aucun produit trouvé.")
            return

        print("\n--- Liste des produits ---")
        for produit in produits:
            print(
                f"[{produit.id}] {produit.nom} - {produit.prix:.2f}$ "
                f"(Stock: {produit.quantite_stock})"
            )
    finally:
        session.close()

def rechercher_produit():
    """Affiche les produits qui correspondent à ce que le user a entrer comme paramètre"""
    session = SessionLocal()

    try:
        terme = input("Entrez l'identifiant ou le nom du produit à rechercher : ").strip()

        if terme.isdigit():
            produit = session.query(Produit).filter_by(id=int(terme)).first()
            if produit:
                print(
                    f"[{produit.id}] {produit.nom} - {produit.prix:.2f}$ "
                    f"(Stock: {produit.quantite_stock})"
                )
            else:
                print("Aucun produit trouvé avec cet identifiant.")
        else:
            resultats = session.query(Produit).filter(Produit.nom.ilike(f"%{terme}%")).all()
            if resultats:
                print("\n--- Résultats ---")
                for p in resultats:
                    print(f"[{p.id}] {p.nom} - {p.prix:.2f}$ (Stock: {p.quantite_stock})")
            else:
                print("Aucun produit ne correspond à ce nom.")

    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
    finally:
        session.close()

def ajouter_produit():
    """Demande à l'utilisateur d'entrer un nouveau produit et l'ajoute en base."""
    session = SessionLocal()
    try:
        nom = input("Nom du produit : ").strip()
        if not nom:
            print("Nom invalide.")
            return

        try:
            prix = float(input("Prix du produit (ex: 12.50) : "))
            if prix < 0:
                print("Le prix doit être positif.")
                return
        except ValueError:
            print("Prix invalide.")
            return

        try:
            quantite = int(input("Quantité en stock : "))
            if quantite < 0:
                print("La quantité doit être positive ou nulle.")
                return
        except ValueError:
            print("Quantité invalide.")
            return

        nouveau_produit = Produit(nom=nom, prix=prix, quantite_stock=quantite)
        session.add(nouveau_produit)
        session.commit()
        print(f"Produit '{nom}' ajouté avec succès.")

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'ajout du produit : {e}")

    finally:
        session.close()
        