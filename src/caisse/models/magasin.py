"""Représente un magasin physique"""
from django.db import models

class Magasin(models.Model):
    """Représente un magasin"""
    nom = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.nom
