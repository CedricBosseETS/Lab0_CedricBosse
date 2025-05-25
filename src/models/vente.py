"""Représente les ventes dans la DB"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from models.base import Base

# pylint: disable=too-few-public-methods
class Vente(Base):
    """Représente une vente"""
    __tablename__ = "ventes"

    id = Column(Integer, primary_key=True)
    date_heure = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)

    produits = relationship("VenteProduit", back_populates="vente", cascade="all, delete-orphan")
