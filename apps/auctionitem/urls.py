from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'auctionitem'

router = routers.SimpleRouter()
router.register('', views.AuctionItemViewSet, basename='ItensLeilão')

urlpatterns = [
    path('', views.list_auctionitems, name='list_auctionitems'),
    path('lances/', views.bids, name='bids'),
    path('lances/adicionar/<int:item_id>/', views.add_bid, name='add_bid'),
    path('lances/editar/<int:item_id>/', views.edit_bid, name='edit_bid'),
    path('lances/excluir/<int:item_id>/', views.delete_bid, name='delete_bid'),
    path('checkout/', views.checkout, name='checkout'),
    path('', include(router.urls) )
]