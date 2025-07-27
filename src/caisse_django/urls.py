"""
Module urls.py principal de la projet Django.

Il route les URL vers l'interface d'administration Django ainsi que vers les URLs de l'application 'caisse'.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('caisse.urls')),  
]
