"""Ce module s'occupe de gérer les accès à la DB pour tout ce qui touche aux ventes"""
from models.produit import Produit
from models.vente import Vente
from models.vente_produit import VenteProduit
from database.init_db import SessionLocal

def faire_vente():
    """Affiche le menu de vente pour l'utilisateur et 
    lance la requête à la DB avec ce qu'il a choisis"""
    session = SessionLocal()
    panier = []
    quantites_temp = {}

    try:
        while True:
            produits = session.query(Produit).all()
            print("\n--- Produits disponibles ---")
            for p in produits:
                deja_reserve = quantites_temp.get(p.id, 0)
                stock_dispo = p.quantite_stock - deja_reserve
                print(f"{p.id}: {p.nom} - {p.prix:.2f} $ ({stock_dispo} en stock)")

            choix = input("ID du produit à ajouter (ou 'f' pour finaliser) : ").strip()
            if choix.lower() == "f":
                break

            try:
                produit_id = int(choix)
            except ValueError:
                print("Entrée invalide.")
                continue

            produit = session.query(Produit).filter_by(id=produit_id).first()
            if not produit:
                print("Produit invalide.")
                continue

            deja_reserve = quantites_temp.get(produit.id, 0)
            stock_dispo = produit.quantite_stock - deja_reserve

            quantite = int(input(f"Quantité de {produit.nom} : "))
            if quantite > stock_dispo:
                print("Stock insuffisant.")
                continue

            panier.append((produit, quantite))
            quantites_temp[produit.id] = deja_reserve + quantite
            print(f"{quantite} x {produit.nom} ajouté(s) au panier.")

        if not panier:
            print("Aucun produit sélectionné.")
            return

        total = creer_vente(panier, session)
        print(f"Vente enregistrée. Total: {total:.2f} $")

    except Exception as e:
        session.rollback()
        print(f"Erreur: {e}")
    finally:
        session.close()


def creer_vente(panier, session):
    """Fait la requête à la DB et mets à jour les items disponibles et leurs quantités"""
    try:
        total = sum(p.prix * q for p, q in panier)

        vente = Vente(total=total)
        session.add(vente)
        session.flush()

        for produit, quantite in panier:
            ligne = VenteProduit(
                vente_id=vente.id,
                produit_id=produit.id,
                quantite=quantite,
                prix_unitaire=produit.prix,
            )
            session.add(ligne)
            produit.quantite_stock -= quantite

        session.commit()
        return total
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def annuler_vente():
    """Annule une vente et mets à jour les quantités disponibles"""
    session = SessionLocal()

    try:
        ventes = session.query(Vente).order_by(Vente.date_heure.desc()).all()
        if not ventes:
            print("Aucune vente enregistrée.")
            return

        print("\n--- Dernières ventes ---")
        for vente in ventes:
            print(f"ID: {vente.id} | Total: {vente.total:.2f} $ | Date: {vente.date_heure}")

        vente_id = input("ID de la vente à annuler : ").strip()
        vente = session.query(Vente).filter_by(id=int(vente_id)).first()
        if not vente:
            print("Vente introuvable.")
            return

        confirmation = input(f"Confirmer l’annulation de la vente {vente.id} (o/N) ? ").lower()
        if confirmation != 'o':
            print("Annulation abandonnée.")
            return

        for ligne in vente.produits:
            produit = session.query(Produit).filter_by(id=ligne.produit_id).first()
            if produit:
                produit.quantite_stock += ligne.quantite

        session.delete(vente)
        session.commit()
        print("Vente annulée et stock restauré.")

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l’annulation : {e}")
    finally:
        session.close()
