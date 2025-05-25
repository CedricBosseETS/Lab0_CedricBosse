"""Fichier principal de l'application. 
Gère le menu principal et les appels."""
from database.init_db import init_db
from services.produit_service import afficher_produits
from services.vente_service import faire_vente
from services.vente_service import annuler_vente
from services.produit_service import rechercher_produit

def afficher_menu():
    """Affiche le menu de la caisse"""
    print("\n=== MENU PRINCIPAL DE LA CAISSE ===")
    print("1. Afficher les produits")
    print("2. Enregistrer une vente")
    print("3. Annuler une vente")
    print("4. Rechercher un produit (par identifiant ou nom")
    print("5. Quitter")

def pause():
    """Arrête le programme après chaque commande pour que l'utilisateur voit le résultat"""
    input("\nAppuyez sur Entrée pour revenir au menu...")

def main():
    """Fonction principale du programme qui écoute le clavier du user"""
    init_db()

    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            afficher_produits()
            pause()
        elif choix == "2":
            faire_vente()
            pause()
        elif choix == "3":
            annuler_vente()
            pause()
        elif choix == "4":
            rechercher_produit()
            pause()
        elif choix == "5":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    print("Initialisation de la base de données...")
    main()
