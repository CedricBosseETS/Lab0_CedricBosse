from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.base import Base

class VenteProduit(Base):
    __tablename__ = "vente_produits"

    id = Column(Integer, primary_key=True)
    vente_id = Column(Integer, ForeignKey("ventes.id"), nullable=False)
    produit_id = Column(Integer, ForeignKey("produits.id"), nullable=False)
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)

    vente = relationship("Vente", back_populates="produits")
    produit = relationship("Produit")
