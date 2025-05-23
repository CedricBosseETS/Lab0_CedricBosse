from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base  # <-- même base partagée

class SaleItem(Base):
    __tablename__ = 'sale_items'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
