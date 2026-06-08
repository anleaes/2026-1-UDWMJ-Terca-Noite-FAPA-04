from django.urls import path
from . import views

app_name = 'auction'

urlpatterns = [
    path('adicionar/', views.add_auction, name='add_auction'),
    path('listar/', views.list_auctions, name='list_auctions'),
    path('itens/<int:auction_id>/', views.view_auction, name='view_auctions'),
    path('itens/<int:auction_id>/cancelar/', views.cancel_auction, name='cancel_auction'),
]
