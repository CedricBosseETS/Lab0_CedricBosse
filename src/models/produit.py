"""Représente les produits dans la DB"""
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from models.base import Base

# pylint: disable=too-few-public-methods
class Produit(Base):
    """Représente un produit"""
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prix = Column(Float, nullable=False)

    stocks = relationship("Stock", back_populates="produit", cascade="all, delete-orphan")
