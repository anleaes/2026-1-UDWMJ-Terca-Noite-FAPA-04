from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'auctioneer'

router = routers.SimpleRouter()
router.register('', views.AuctioneerViewSet, basename='Leiloeiros')

urlpatterns = [
    path('login/', views.login_auctioneer, name='login'),
    path('listar/', views.list_auctioneers, name='list_auctioneers'),
    path('adicionar/', views.add_auctioneer, name='add_auctioneer'),
    path('editar/<int:id_auctioneer>/', views.edit_auctioneer, name='edit_auctioneer'),
    path('excluir/<int:id_auctioneer>/', views.delete_auctioneer, name='delete_auctioneer'),
    path('visualizar/<int:id_auctioneer>/', views.view_auctioneer, name='view_auctioneer'),
    path('', include(router.urls) )
]