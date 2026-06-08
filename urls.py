from django.urls import path
from . import views

app_name = 'auctioneer'

urlpatterns = [
    path('login/', views.login_auctioneer, name='login'),
    path('listar/', views.list_auctioneers, name='list_auctioneers'),
    path('adicionar/', views.add_auctioneer, name='add_auctioneer'),
    path('editar/<int:id_auctioneer>/', views.edit_auctioneer, name='edit_auctioneer'),
    path('excluir/<int:id_auctioneer>/', views.delete_auctioneer, name='delete_auctioneer'),
]