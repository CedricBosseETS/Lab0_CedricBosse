"""Représente le stock de chaque produit dans chaque magasin"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

# pylint: disable=too-few-public-methods
class Stock(Base):
    """Représente le stock d’un produit dans un magasin"""
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey("produits.id"), nullable=False)
    magasin_id = Column(Integer, ForeignKey("magasins.id"), nullable=False)
    quantite = Column(Integer, nullable=False)

    produit = relationship("Produit", back_populates="stocks")
    magasin = relationship("Magasin", back_populates="stocks")
