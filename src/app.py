from database.init_db import init_db

def afficher_menu():
    print("\n=== MENU PRINCIPAL DE LA CAISSE ===")
    print("1. Afficher les produits")
    print("2. Ajouter un produit")
    print("3. Faire une vente")
    print("4. Voir l’historique des ventes")
    print("5. Quitter")

def main():
    init_db()  # Initialisation au lancement

    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            print(">> TODO: afficher les produits")
        elif choix == "2":
            print(">> TODO: ajouter un produit")
        elif choix == "3":
            print(">> TODO: faire une vente")
        elif choix == "4":
            print(">> TODO: afficher l’historique des ventes")
        elif choix == "5":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    print("Initialisation de la base de données...")
    main()
