from django.shortcuts import render
from auction.models import Auction
from item.models import Item

def home(request):
    auctions = (
        Auction.objects
        .filter(status='Em andamento')
        .prefetch_related(
            'auction_items',
            'auction_items__item'
        )
        .all()
    )
    items = Item.objects.all()

    return render( 
        request,
        'core/home.html',
        {
            'auctions': auctions,
            'items': items
        }

    