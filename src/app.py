from src.services import product_service, sale_service

def main_menu():
    while True:
        print("\n=== SYSTÈME DE CAISSE (MySQL) ===")
        print("1. Rechercher un produit")
        print("2. Enregistrer une vente")
        print("3. Annuler une vente")
        print("4. Consulter le stock")
        print("5. Quitter")

        choice = input("Votre choix: ")

        if choice == "1":
            keyword = input("Entrez le nom ou ID du produit: ")
            product_service.search_product(keyword)

        elif choice == "2":
            sale_service.register_sale()

        elif choice == "3":
            sale_id = input("ID de la vente à annuler: ")
            sale_service.cancel_sale(sale_id)

        elif choice == "4":
            product_service.view_stock()

        elif choice == "5":
            print("À bientôt !")
            break

        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main_menu()
