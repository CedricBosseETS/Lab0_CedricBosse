#!/bin/sh

echo "⏳ Attente que la base de données MySQL soit prête..."

# Boucle jusqu'à ce que la DB soit disponible (port ouvert et responsive)
until mysqladmin ping -h db -u root -p"$MYSQL_ROOT_PASSWORD" --silent; do
  echo "   ➤ Base non prête, nouvelle tentative dans 2 secondes..."
  sleep 2
done

echo "✅ Base de données disponible."

echo "🛠 Appliquer les migrations..."
python manage.py migrate

echo "📦 Initialiser les données de stock"
python manage.py init_db

echo "🚀 Démarrage du serveur Django"
python manage.py runserver 0.0.0.0:5000
