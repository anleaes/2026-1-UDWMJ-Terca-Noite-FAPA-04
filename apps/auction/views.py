from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from auction.models import Auction
from auctionitem.models import AuctionItem
from item.models import Item
from auctioneer.models import Auctioneer
from core.auth import auctioneer_required
from receiptpayment.models import Receipt
from rest_framework import viewsets
from .serializer import AuctionSerializer

@auctioneer_required
def add_auction(request):
    template_name = 'auction/add_auction.html'
    current_auctioneer = get_object_or_404(
        Auctioneer,
        id=request.session['auth']['id']
    )
    items = Item.objects.all()
    

    if request.method == 'POST':
        selected_items = request.POST.getlist('items')

        if not selected_items:
            item_id = request.POST.get('item')
            selected_items = [item_id] if item_id else []

        if not selected_items:
            messages.warning(
                request,
                'Selecione pelo menos um item para criar o leilão.'
            )
            return render(request, template_name, {
                'current_auctioneer': current_auctioneer,
                'items': items
            })

        with transaction.atomic():
            auction = Auction.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                date_begin=request.POST.get('date_begin'),
                date_end=request.POST.get('date_end'),
                initial_value=request.POST.get('initial_value', 0.0),
                auctioneer=current_auctioneer,
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
        'current_auctioneer': current_auctioneer,
        'items': items
    }

    return render(request, template_name, context)


def list_auctions(request):
    template_name = 'auction/list_auctions.html'

    auctions = Auction.objects.select_related(
        'auctioneer'
    ).prefetch_related(
        'auction_items',
        'auction_items__item'
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

    if auction.status != 'Cancelado':

        auction.status = (
            'Cancelado'
        )

        auction.save()

    return redirect(
        'auction:list_auctions'
    )

@auctioneer_required
def delete_auction(request, auction_id):
    auction = get_object_or_404(
        Auction,
        id=auction_id
    )

    auction.delete()

    return redirect('auction:list_auctions')


def view_auction(request, auction_id):

    template_name = (
        'auction/view_auctions.html'
    )


    auction = get_object_or_404(
        Auction,
        id=auction_id
    )

    auction_items = (
        AuctionItem.objects
        .select_related(
            'item',
            'item__category'
        )
        .filter(
            auction=auction
        )
    )

    bids = (
        auction.bids
        .select_related(
            'user',
            'auctionitem__item'
        )
        .order_by('-id')
    )

    accepted_bid = (
        bids
        .filter(
            status='A'
        )
        .first()
    )

    receipt = (
        Receipt.objects
        .select_related(
            'payment'
        )
        .filter(
            auction=auction
        )
        .first()
    )

    auth = request.session.get('auth')
    can_bid = (
        bool(auth)
        and auth.get('role') == 'user'
        and auction.status == 'Em andamento'
    )

    context = {
        'auction': auction,
        'auction_items': auction_items,
        'bids': bids,
        'can_bid': can_bid,
        'accepted_bid': accepted_bid,
        'winner_user': accepted_bid.user if accepted_bid else None,
        'receipt': receipt,
        'selected_payment': receipt.payment if receipt else None,
    }

    return render(
        request,
        template_name,
        context
    )

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
