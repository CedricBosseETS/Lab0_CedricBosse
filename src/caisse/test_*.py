from unittest.mock import MagicMock
import pytest
from django.http import Http404
from caisse.models import Magasin, Produit, Stock
import caisse.services.produit_service as produit_service
import caisse.services.magasin_service as magasin_service
import caisse.services.stock_service as stock_service
import caisse.services.vente_service as vente_service
from django.db.models import Q

@pytest.fixture
def mock_magasins(mocker):
    # Mock d’un queryset retournant une liste simple de magasins
    magasins = [
        Magasin(nom="Magasin 1", quartier="Q1", type="magasin"),
        Magasin(nom="Magasin 2", quartier="Q2", type="magasin"),
        Magasin(nom="Centre Logistique", quartier="Q3", type="logistique"),
    ]
    mock_qs = mocker.MagicMock()
    mock_qs.all.return_value = magasins
    mock_qs.filter.return_value = [m for m in magasins if m.type == "magasin"]
    mock_qs.get.return_value = magasins[2]
    return magasins, mock_qs

def test_get_all_magasins(mocker, mock_magasins):
    magasins, mock_qs = mock_magasins
    mocker.patch('caisse.models.Magasin.objects.all', return_value=magasins)

    result = magasin_service.get_all_magasins()
    assert result == magasins

def test_get_only_magasins(mocker, mock_magasins):
    magasins, mock_qs = mock_magasins
    mocker.patch('caisse.models.Magasin.objects.filter', return_value=mock_qs.filter(type="magasin"))

    result = magasin_service.get_only_magasins()
    assert all(m.type == "magasin" for m in result)

def test_get_magasin_by_id_success(mocker, mock_magasins):
    magasins, mock_qs = mock_magasins
    # Mock get_object_or_404
    mocker.patch('caisse.services.magasin_service.get_object_or_404', return_value=magasins[0])

    result = magasin_service.get_magasin_by_id(1)
    assert result == magasins[0]

def test_get_magasin_by_id_raises_404(mocker):
    # Mock get_object_or_404 pour lever Http404
    def raise_404(*args, **kwargs):
        raise Http404()

    mocker.patch('caisse.services.magasin_service.get_object_or_404', side_effect=raise_404)

    with pytest.raises(Http404):
        magasin_service.get_magasin_by_id(999)

def test_get_centre_logistique(mocker, mock_magasins):
    magasins, mock_qs = mock_magasins
    mocker.patch('caisse.models.Magasin.objects.get', return_value=magasins[2])

    result = magasin_service.get_centre_logistique()
    assert result.type == "logistique"

def test_get_all_magasins(mocker, mock_magasins):
    magasins, mock_qs = mock_magasins
    mocker.patch('caisse.models.Magasin.objects.all', return_value=magasins)

    result = magasin_service.get_all_magasins()
    assert result == magasins

@pytest.fixture
def produit_mock(mocker):
    return mocker.patch('caisse.models.Produit')

@pytest.fixture
def stock_mock(mocker):
    return mocker.patch('caisse.models.Stock')

def test_get_produits_par_magasin(mocker):
    mock_stocks = [
        MagicMock(produit=MagicMock(id=1, nom="Prod1")),
        MagicMock(produit=MagicMock(id=2, nom="Prod2")),
    ]
    # Patch Stock.objects.filter().select_related() pour retourner mock_stocks
    mock_filter = mocker.patch('caisse.services.produit_service.Stock.objects.filter')
    mock_filter.return_value.select_related.return_value = mock_stocks

    result = produit_service.get_produits_par_magasin(1)

    mock_filter.assert_called_once_with(magasin_id=1)
    mock_filter.return_value.select_related.assert_called_once_with('produit')
    assert result == [stock.produit for stock in mock_stocks]

def test_rechercher_produits_par_nom_ou_id_with_id(mocker):
    mock_qs = MagicMock()
    patch_filter = mocker.patch('caisse.services.produit_service.Produit.objects.filter', return_value=mock_qs)

    result = produit_service.rechercher_produits_par_nom_ou_id("123")

    # Vérifie que filter a été appelé avec le bon Q
    patch_filter.assert_called_once_with(Q(id=123) | Q(nom__icontains="123"))
    assert result == mock_qs

def test_rechercher_produits_par_nom_ou_id_with_name(mocker):
    mock_qs = MagicMock()
    patch_filter = mocker.patch('caisse.services.produit_service.Produit.objects.filter', return_value=mock_qs)

    result = produit_service.rechercher_produits_par_nom_ou_id("abc")

    patch_filter.assert_called_once_with(nom__icontains="abc")
    assert result == mock_qs

def test_get_tous_les_produits(mocker):
    mock_qs = MagicMock()
    patch_all = mocker.patch('caisse.services.produit_service.Produit.objects.all', return_value=mock_qs)

    result = produit_service.get_tous_les_produits()

    patch_all.assert_called_once()
    assert result == mock_qs

def test_mettre_a_jour_produit(mocker):
    mock_produit = MagicMock()
    patch_get = mocker.patch('caisse.services.produit_service.Produit.objects.get', return_value=mock_produit)

    produit_service.mettre_a_jour_produit(produit_id=1, nom="Nouveau Nom", prix=99.99, description="Desc")

    patch_get.assert_called_once_with(id=1)
    assert mock_produit.nom == "Nouveau Nom"
    assert mock_produit.prix == 99.99
    assert mock_produit.description == "Desc"
    mock_produit.save.assert_called_once()

def test_get_stock_total_par_magasin(mocker):
    mock_manager = MagicMock()
    mock_values = MagicMock()
    mock_result = MagicMock()

    # On configure la chaîne d'appels : Stock.objects.values().annotate()
    mocker.patch('caisse.models.Stock.objects', mock_manager)
    mock_manager.values.return_value = mock_values
    mock_values.annotate.return_value = mock_result

    result = stock_service.get_stock_total_par_magasin()

    mock_manager.values.assert_called_once_with('magasin__id', 'magasin__nom')
    mock_values.annotate.assert_called_once()
    assert result == mock_result

    
def test_get_stock_par_magasin(mocker):
    mock_qs = MagicMock()
    patch = mocker.patch('caisse.models.Stock.objects.filter', return_value=mock_qs)
    mock_qs.select_related.return_value = mock_qs
    result = stock_service.get_stock_par_magasin(1)
    patch.assert_called_once_with(magasin_id=1)
    mock_qs.select_related.assert_called_once_with('produit')
    assert result == mock_qs

def test_get_stock_entry(mocker):
    mock_qs = MagicMock()
    mocker.patch('caisse.models.Stock.objects.filter', return_value=mock_qs)
    mock_qs.first.return_value = 'entry'
    result = stock_service.get_stock_entry(1, 2)
    assert result == 'entry'
    mock_qs.first.assert_called_once()

def test_get_stock_dict_for_magasin(mocker):
    mock_queryset = MagicMock()
    mock_stock1 = MagicMock()
    mock_stock1.produit.id = 1
    mock_stock2 = MagicMock()
    mock_stock2.produit.id = 2
    mock_stock_list = [mock_stock1, mock_stock2]

    mock_queryset.select_related.return_value = mock_stock_list

    mocker.patch('caisse.models.Stock.objects.filter', return_value=mock_queryset)

    from caisse.services import stock_service
    result = stock_service.get_stock_dict_for_magasin(1)

    assert result == {
        1: mock_stock1,
        2: mock_stock2,
    }
    mock_queryset.select_related.assert_called_once_with('produit')

def test_get_stock_indexed_by_produit(mocker):
    d1 = {1: "A"}
    d2 = {2: "B"}
    mocker.patch('caisse.services.stock_service.get_stock_dict_for_magasin', side_effect=[d1, d2])
    stock_centre, stock_local = stock_service.get_stock_indexed_by_produit(10, 20)
    assert stock_centre == d1
    assert stock_local == d2

def test_get_produits_disponibles(mocker):
    mock_queryset = MagicMock()
    
    stock1 = MagicMock()
    stock1.produit = "Produit A"
    stock2 = MagicMock()
    stock2.produit = "Produit B"
    stock_list = [stock1, stock2]

    mock_queryset.select_related.return_value = stock_list
    mocker.patch('caisse.models.Stock.objects.filter', return_value=mock_queryset)

    from caisse.services import stock_service
    result = stock_service.get_produits_disponibles(magasin_id=1)

    assert result == ["Produit A", "Produit B"]
    mock_queryset.select_related.assert_called_once_with('produit')

def test_get_ventes_par_magasin(mocker):
    mock_qs = MagicMock()
    mock_qs.values.return_value.annotate.return_value.order_by.return_value = "resultat"
    mocker.patch('caisse.models.Vente.objects', new=MagicMock(values=MagicMock(return_value=mock_qs.values())))
    
    result = vente_service.get_ventes_par_magasin()
    assert result == "resultat"

def test_get_produits_les_plus_vendus(mocker):
    mock_qs = MagicMock()
    mock_qs.values.return_value.annotate.return_value.order_by.return_value.__getitem__.return_value = ["top3"]
    mocker.patch('caisse.models.VenteProduit.objects', new=MagicMock(values=MagicMock(return_value=mock_qs.values())))
    
    result = vente_service.get_produits_les_plus_vendus()
    assert result == ["top3"]
  
def test_get_dashboard_stats(mocker):
    ventes_mock = MagicMock()
    ventes_mock.values.return_value.annotate.return_value.order_by.return_value = ["ventes_par_magasin"]
    mocker.patch('caisse.models.Vente.objects', new=MagicMock(
        values=MagicMock(return_value=ventes_mock.values())
    ))
    
    rupture_mock = MagicMock()
    rupture_mock.filter.return_value.select_related.return_value = ["rupture_stock"]
    mocker.patch('caisse.models.Stock.objects', new=MagicMock(
        filter=MagicMock(return_value=rupture_mock.filter())
    ))
    
    surstock_mock = MagicMock()
    surstock_mock.filter.return_value.select_related.return_value = ["surstock"]
    mocker.patch('caisse.models.Stock.objects', new=MagicMock(
        filter=MagicMock(return_value=surstock_mock.filter())
    ))
    
    ventes_hebdo_mock = MagicMock()
    ventes_hebdo_mock.values.return_value.annotate.return_value.order_by.return_value = ["ventes_hebdo"]
    mocker.patch('caisse.models.Vente.objects.filter', return_value=ventes_hebdo_mock)
    
    stats = vente_service.get_dashboard_stats()
    
    assert "ventes_par_magasin" in stats
    assert "rupture_stock" in stats
    assert "surstock" in stats
    assert "ventes_hebdo" in stats