from src.database.mysql_client import SessionLocal
from src.models.product import Product
from sqlalchemy import or_

def search_product(keyword):
    session = SessionLocal()
    try:
        results = session.query(Product).filter(
            or_(
                Product.product_id == keyword,
                Product.name.ilike(f"%{keyword}%"),
                Product.category.ilike(f"%{keyword}%")
            )
        ).all()

        if not results:
            print("Aucun produit trouvé.")
        else:
            for p in results:
                print(f"{p.name} ({p.product_id}) - Stock: {p.stock}, Prix: {p.price}$")
    finally:
        session.close()


def view_stock():
    session = SessionLocal()
    try:
        products = session.query(Product).all()
        print("\n=== Stock actuel ===")
        for p in products:
            print(f"{p.name} ({p.product_id}) - Stock: {p.stock}, Prix: {p.price}$")
    finally:
        session.close()
