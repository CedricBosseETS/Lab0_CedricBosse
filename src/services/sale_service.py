from src.database.mysql_client import SessionLocal
from src.models.product import Product
from src.models.sale import Sale
from datetime import datetime
import uuid
import json

def register_sale():
    session = SessionLocal()
    selected_products = []
    total = 0.0

    try:
        while True:
            product_id = input("Entrez l'ID du produit (ou 'fin' pour terminer): ")
            if product_id.lower() == "fin":
                break

            product = session.query(Product).filter_by(product_id=product_id).first()
            if not product:
                print("Produit introuvable.")
                continue

            quantity = int(input("Quantité: "))
            if product.stock < quantity:
                print("Stock insuffisant.")
                continue

            selected_products.append({
                "product_id": product.product_id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity
            })

            total += product.price * quantity
            product.stock -= quantity  # update stock

        if not selected_products:
            print("Aucun produit sélectionné.")
            return

        sale_id = str(uuid.uuid4())
        sale = Sale(
            sale_id=sale_id,
            products=json.dumps(selected_products),
            total=total,
            timestamp=datetime.now()
        )

        session.add(sale)
        session.commit()
        print(f"Vente enregistrée avec succès. Total: {total}$ (ID: {sale_id})")
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'enregistrement de la vente: {e}")
    finally:
        session.close()


def cancel_sale(sale_id):
    session = SessionLocal()
    try:
        sale = session.query(Sale).filter_by(sale_id=sale_id).first()
        if not sale:
            print("Vente introuvable.")
            return

        product_items = json.loads(sale.products)

        for item in product_items:
            product = session.query(Product).filter_by(product_id=item["product_id"]).first()
            if product:
                product.stock += item["quantity"]

        session.delete(sale)
        session.commit()
        print("Vente annulée et stock restauré.")
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'annulation de la vente: {e}")
    finally:
        session.close()
