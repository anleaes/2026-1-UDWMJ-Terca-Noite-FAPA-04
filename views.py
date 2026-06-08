from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from auctionbid.models import AuctionBid


def list_bids(request):
    bids = AuctionBid.objects.select_related(
        'user', 'auction', 'auctionitem'
    ).all()
    
    context = {
        'bids': bids
    }
    
    return render(request, 'auctionbid/list_bids.html', context)


def view_bid(request, bid_id):
    bid = get_object_or_404(
        AuctionBid.objects.select_related(
            'user', 'auction', 'auctionitem'
        ),
        id=bid_id
    )
    
    context = {
        'bid': bid
    }
    
    return render(request, 'auctionbid/view_bid.html', context)
