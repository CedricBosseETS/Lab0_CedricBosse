from database.init_db import init_db

def main():
    print("Initialisation de la base de données...")
    init_db()
    print("Base de données initialisée.")

if __name__ == "__main__":
    main()
