from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Vente(Base):
    __tablename__ = "ventes"

    id = Column(Integer, primary_key=True)
    date_heure = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)

    produits = relationship("VenteProduit", back_populates="vente", cascade="all, delete-orphan")

