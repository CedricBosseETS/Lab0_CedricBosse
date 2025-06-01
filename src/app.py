"""Fichier principal de l'application. 
Gère la sélection de l'entité (magasin, logistique, maison mère), le menu principal et les appels aux services."""

from src.caisse.init_db import init_db, SessionLocal
from services.produit_service import afficher_produits, rechercher_produit, ajouter_produit, mettre_a_jour_produit
from services.vente_service import faire_vente, annuler_vente
from models.magasin import Magasin

def choisir_entite():
    """Permet à l'utilisateur de choisir une entité parmi les magasins, centre logistique et maison mère."""
    session = SessionLocal()
    try:
        entites = session.query(Magasin).all()
        print("\n=== Sélectionnez une entité ===")
        for entite in entites:
            print(f"{entite.id}. {entite.nom} ({entite.type})")
        choix = input("ID de l'entité : ")
        entite = session.query(Magasin).filter_by(id=int(choix)).first()
        if entite is None:
            print("Entité invalide.")
            return None
        return entite
    finally:
        session.close()

def menu_magasin():
    """Affiche le menu pour les magasins."""
    print("\n=== MENU MAGASIN ===")
    print("1. Afficher les produits")
    print("2. Enregistrer une vente")
    print("3. Annuler une vente")
    print("4. Rechercher un produit (par identifiant ou nom)")
    print("5. Ajouter un produit dans le magasin")
    print("6. Quitter")

def menu_logistique():
    """Affiche le menu pour le centre logistique."""
    print("\n=== MENU CENTRE LOGISTIQUE ===")
    print("1. Consulter stock central (à implémenter)")
    print("2. Gérer réapprovisionnement (à implémenter)")
    print("3. Quitter")

def menu_admin():
    """Affiche le menu pour la maison mère."""
    print("\n=== MENU MAISON MÈRE ===")
    print("1. Générer rapport consolidé (à implémenter)")
    print("2. Visualiser performances (à implémenter)")
    print("3. Mettre à jour les produits")
    print("4. Quitter")

def pause():
    """Pause pour laisser l'utilisateur voir les résultats."""
    input("\nAppuyez sur Entrée pour revenir au menu...")

def main():
    """Fonction principale du programme."""
    init_db()

    entite = choisir_entite()
    if entite is None:
        print("Fin du programme.")
        return

    while True:
        if entite.type == "magasin":
            menu_magasin()
            choix = input("Choisissez une option (1-6) : ").strip()

            if choix == "1":
                afficher_produits(entite.id)
                pause()
            elif choix == "2":
                faire_vente(entite.id)
                pause()
            elif choix == "3":
                annuler_vente(entite.id)
                pause()
            elif choix == "4":
                rechercher_produit(entite.id)
                pause()
            elif choix == "5":
                ajouter_produit(entite.id)
                pause()
            elif choix == "6":
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

        elif entite.type == "logistique":
            menu_logistique()
            choix = input("Choisissez une option (1-3) : ").strip()

            if choix == "1":
                print("Consultation du stock central - fonctionnalité à implémenter.")
                pause()
            elif choix == "2":
                print("Gestion du réapprovisionnement - fonctionnalité à implémenter.")
                pause()
            elif choix == "3":
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

        elif entite.type == "admin":
            menu_admin()
            choix = input("Choisissez une option (1-4) : ").strip()

            if choix == "1":
                print("Génération rapport consolidé - fonctionnalité à implémenter.")
                pause()
            elif choix == "2":
                print("Visualisation des performances - fonctionnalité à implémenter.")
                pause()
            elif choix == "3":
                mettre_a_jour_produit()
                pause()
            elif choix == "4":
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

        else:
            print("Type d'entité non reconnu.")
            break

if __name__ == "__main__":
    main()
