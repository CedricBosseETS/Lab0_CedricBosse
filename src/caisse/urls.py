from django.urls import path
from .views import home, magasins, admin_page

urlpatterns = [
    path('', home.home_view, name='home'),
    path('magasins/', magasins.page_magasins, name='magasins'),
    path('admin_page/', admin_page.admin_view, name='admin_page'),
]
