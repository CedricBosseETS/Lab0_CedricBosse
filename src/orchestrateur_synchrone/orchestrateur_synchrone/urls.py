from django.contrib import admin
from django.urls import path
from orchestrateurS.api_views import (
    bla,
)

urlpatterns = [
    path('admin/', admin.site.urls),
]
