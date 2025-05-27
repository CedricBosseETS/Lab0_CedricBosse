"""Représente un magasin physique"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

# pylint: disable=too-few-public-methods
class Magasin(Base):
    """Représente un magasin"""
    __tablename__ = "magasins"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    quartier = Column(String(100), nullable=False)
    type = Column(String(50))

    stocks = relationship("Stock", back_populates="magasin", cascade="all, delete-orphan")
    ventes = relationship("Vente", back_populates="magasin", cascade="all, delete-orphan")
