from django.urls import path, include
from . import views
from auctionitem import views as auctionitem_views
from rest_framework import routers

app_name = 'auctionbid'

router = routers.SimpleRouter()
router.register('', views.AuctionBidViewSet, basename='Lances')

urlpatterns = [
    path('', views.list_bids, name='list_bids'),
    path('ver/<int:bid_id>/', views.view_bid, name='view_bid'),
    path('lances/', auctionitem_views.bids, name='bids'),
    path('lances/adicionar/<int:item_id>/', auctionitem_views.add_bid, name='add_bid'),
    path('lances/editar/<int:item_id>/', auctionitem_views.edit_bid, name='edit_bid'),
    path('lances/excluir/<int:item_id>/', auctionitem_views.delete_bid, name='delete_bid'),
    path('checkout/', auctionitem_views.checkout, name='checkout'),
    path('', include(router.urls) )
]
