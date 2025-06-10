from django.core.management.base import BaseCommand
import MySQLdb
import os

class Command(BaseCommand):
    help = "Donne les droits à l'utilisateur 'caisse_user' sur la base de test MySQL."

    def handle(self, *args, **kwargs):
        db_host = os.getenv("DB_HOST", "db")
        root_user = os.getenv("MYSQL_ROOT_USER", "root")
        root_pass = os.getenv("MYSQL_ROOT_PASSWORD", "root")

        self.stdout.write("Connexion à MySQL pour donner les droits sur la base de test...")

        try:
            conn = MySQLdb.connect(
                host=db_host,
                user=root_user,
                passwd=root_pass
            )
            cursor = conn.cursor()

            # Modifier ici selon le nom exact de ta base de test
            cursor.execute("GRANT ALL PRIVILEGES ON `test_%`.* TO 'caisse_user'@'%';")
            cursor.execute("FLUSH PRIVILEGES;")
            conn.commit()
            cursor.close()
            conn.close()

            self.stdout.write(self.style.SUCCESS("✅ Droits accordés à 'caisse_user' sur les bases test_%"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Échec de l’attribution des droits : {e}"))
