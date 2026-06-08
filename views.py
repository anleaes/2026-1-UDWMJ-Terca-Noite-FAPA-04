from django.shortcuts import render, get_object_or_404, redirect
from auction.models import Auction
from auctionitem.models import AuctionItem
from item.models import Item
from auctioneer.models import Auctioneer
from core.auth import auctioneer_required


@auctioneer_required
def add_auction(request):
    template_name = 'auction/add_auction.html'
    auctioneers = Auctioneer.objects.all()
    items = Item.objects.all()
    

    if request.method == 'POST':
        auctioneer_id = request.POST.get('auctioneer')
        selected_items = request.POST.getlist('items')

        auction = Auction.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            date_begin=request.POST.get('date_begin'),
            date_end=request.POST.get('date_end'),
            initial_value=request.POST.get('initial_value', 0.0),
            auctioneer_id=auctioneer_id,
            status='Em andamento'
        )

        for item_id in selected_items:
            item = get_object_or_404(Item, id=item_id)
            AuctionItem.objects.create(
                auction=auction,
                item=item,
                quantity=1,
                value=item.price,
                sub_total=item.price
            )

        return redirect('auction:list_auctions')

    context = {
        'auctioneers': auctioneers,
        'items': items
    }

    return render(request, template_name, context)


@auctioneer_required
def list_auctions(request):
    template_name = 'auction/list_auctions.html'

    auctions = Auction.objects.select_related(
        'auctioneer'
    ).all()

    context = {
        'auctions': auctions
    }

    return render(request, template_name, context)


@auctioneer_required
def cancel_auction(
    request,
    auction_id
):

    auction = get_object_or_404(
        Auction,
        id=auction_id
    )

    if auction.status != 'CANCELADO':

        auction.status = (
            'CANCELADO'
        )

        auction.save()

    return redirect(
        'auction:list_auctions'
    )


@auctioneer_required
def view_auction(request, auction_id):

    template_name = (
        'auction/view_auctions.html'
    )

    auction = get_object_or_404(
        Auction,
        id=auction_id
    )

    items = auction.auction_items.select_related('item').all()
    bids = auction.bids.select_related('user', 'auctionitem__item').order_by('-id')

    context = {
        'auction': auction,
        'items': items,
        'bids': bids,
    }

    return render(
        request,
        template_name,
        context
    )