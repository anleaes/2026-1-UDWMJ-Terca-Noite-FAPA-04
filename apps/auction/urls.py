from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'auction'

router = routers.SimpleRouter()
router.register('', views.AuctionViewSet, basename='Leilões')


urlpatterns = [
    path('adicionar/', views.add_auction, name='add_auction'),
    path('listar/', views.list_auctions, name='list_auctions'),
    path('itens/<int:auction_id>/', views.view_auction, name='view_auctions'),
    path('cancelar/<int:auction_id>/cancel/', views.cancel_auction, name='cancel_auction'),
    path('deletar/<int:auction_id>/delete/', views.delete_auction, name='delete_auction'),
    path('', include(router.urls) )

]
