from sqlalchemy import Column, Integer, String, Float
from src.database.mysql_client import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(100))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
