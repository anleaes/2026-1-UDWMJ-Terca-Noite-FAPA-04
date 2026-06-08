from django.shortcuts import render, redirect, get_object_or_404

from auctionitem.models import AuctionItem
from auction.models import Auction
from item.models import Item
from user.models import User
from auctioneer.models import Auctioneer
from payment.models import Payment
from core.auth import user_required, get_auth
from auctionbid.models import AuctionBid

from receiptpayment.views import (
    create_receipt_for_auction
)


@user_required
def bids(request):

    template_name = (
        'auctionitem/bid.html'
    )

    bid = request.session.get(
        'bid',
        {}
    )

    total = sum(
        float(item['subtotal'])
        for item in bid.values()
    )

    context = {
        'bid': bid,
        'cart': bid,
        'total': total
    }

    return render(
        request,
        template_name,
        context
    )


@user_required
def add_bid(request, item_id):

    auction_item = get_object_or_404(
        AuctionItem,
        id=item_id
    )

    auction = auction_item.auction

    # impede lances em leilão encerrado
    if auction.status == 'Finalizado':

        return redirect(
            'auction:view_auction',
            auction_id=auction.id
        )

    bid = request.session.get(
        'bid',
        {}
    )

    pid = str(
        auction_item.id
    )

    if pid in bid:

        bid[pid]['quantity'] += 1

    else:

        bid[pid] = {
            'name': (
                auction_item.item.name
            ),
            'price': float(
                auction_item.value
            ),
            'quantity': 1,
            'subtotal': float(
                auction_item.value
            ),
            'auction_id': (
                auction.id
            )
        }

    quantity = (
        bid[pid]['quantity']
    )

    price = float(
        bid[pid]['price']
    )

    bid[pid]['subtotal'] = (
        quantity * price
    )

    request.session['bid'] = bid
    request.session.modified = True

    return redirect(
        'auctionitem:bids'
    )


@user_required
def edit_bid(
    request,
    item_id
):

    if request.method == 'POST':

        quantity = int(
            request.POST.get(
                'quantity',
                1
            )
        )

        bid = request.session.get(
            'bid',
            {}
        )

        pid = str(item_id)

        if pid in bid:

            if quantity <= 0:

                del bid[pid]

            else:

                price = float(
                    bid[pid]['price']
                )

                bid[pid][
                    'quantity'
                ] = quantity

                bid[pid][
                    'subtotal'
                ] = (
                    quantity *
                    price
                )

        request.session['bid'] = bid
        request.session.modified = True

    return redirect(
        'auctionitem:bids'
    )


@user_required
def delete_bid(
    request,
    item_id
):

    bid = request.session.get(
        'bid',
        {}
    )

    pid = str(item_id)

    if pid in bid:

        del bid[pid]

    request.session['bid'] = bid
    request.session.modified = True

    return redirect(
        'auctionitem:bids'
    )


@user_required
def checkout(request):

    template_name = (
        'auctionitem/checkout.html'
    )

    bid = request.session.get(
        'bid',
        {}
    )

    total = sum(
        float(item['subtotal'])
        for item in bid.values()
    )

    auth = get_auth(request)
    user = get_object_or_404(User, id=auth['id'])

    auctioneers = (
        Auctioneer.objects.all()
    )

    if request.method == 'POST':

        if not bid:

            return redirect(
                'auctionitem:bids'
            )

        payment_method = request.POST.get(
            'payment_method'
        )

        auctioneer_id = request.POST.get(
            'auctioneer'
        )

        first_item_id = next(
            iter(bid)
        )

        auction_item = (
            get_object_or_404(
                AuctionItem,
                id=first_item_id
            )
        )

        auction = (
            auction_item.auction
        )

        if (
            auction.status
            == 'Finalizado'
        ):
            return redirect(
                'auction:view_auctions',
                auction_id=auction.id
            )

        if auctioneer_id:

            auction.auctioneer = (
                get_object_or_404(
                    Auctioneer,
                    id=auctioneer_id
                )
            )

        auction.status = (
            'Finalizado'
        )

        auction.save()

        payment = (
            Payment.objects
            .filter(
                auction=auction
            )
            .first()
        )

        if payment:

            payment.total = total

            if hasattr(
                payment,
                'payment_method'
            ):
                payment.payment_method = (
                    payment_method
                )

            if hasattr(
                payment,
                'user'
            ):
                payment.user = user

            payment.save()

        else:

            payment_data = {
                'auction': auction,
                'total': total
            }

            if hasattr(
                Payment,
                'payment_method'
            ):
                payment_data[
                    'payment_method'
                ] = payment_method

            if hasattr(
                Payment,
                'user'
            ):
                payment_data[
                    'user'
                ] = user

            payment = (
                Payment.objects
                .create(
                    **payment_data
                )
            )

        for (
            item_id,
            item
        ) in bid.items():

            auction_item = (
                get_object_or_404(
                    AuctionItem,
                    id=item_id
                )
            )

            auction_item.quantity = (
                int(
                    item[
                        'quantity'
                    ]
                )
            )

            auction_item.sub_total = (
                float(
                    item[
                        'subtotal'
                    ]
                )
            )

            auction_item.save()

            AuctionBid.objects.create(
                auction=auction,
                auctionitem=auction_item,
                user=user,
                value=item['subtotal'],
                status='A'
            )

        create_receipt_for_auction(
            payment
        )

        request.session[
            'bid'
        ] = {}

        request.session.modified = (
            True
        )

        return redirect(
            'auction:view_auctions',
            auction_id=auction.id
        )

    context = {
        'bid': bid,
        'total': total,
        'current_user': user,
        'auctioneers': (
            auctioneers
        ),
        'payment_methods': (
            Payment._meta
            .get_field(
                'payment_method'
            )
            .choices
        )
    }

    return render(
        request,
        template_name,
        context
    )


def list_auctionitems(
    request
):

    template_name = (
        'auctionitem/'
        'list_auctionitems.html'
    )

    auctionitems = (
        AuctionItem.objects
        .select_related(
            'auction',
            'item'
        )
        .all()
    )

    context = {
        'auctionitems':
        auctionitems
    }

    return render(
        request,
        template_name,
        context
    )


def view_auctionitem(
    request,
    id_auctionitem
):

    template_name = (
        'auctionitem/'
        'view_auctionitem.html'
    )

    auctionitem = (
        get_object_or_404(
            AuctionItem,
            id=id_auctionitem
        )
    )

    context = {
        'auctionitem':
        auctionitem
    }

    return render(
        request,
        template_name,
        context
    )


def add_auctionitem(
    request
):

    template_name = (
        'auctionitem/'
        'add_auctionitem.html'
    )

    auctions = (
        Auction.objects.all()
    )

    items = (
        Item.objects.all()
    )

    if request.method == 'POST':

        auction_id = (
            request.POST.get(
                'auction'
            )
        )

        item_id = (
            request.POST.get(
                'item'
            )
        )

        quantity = int(
            request.POST.get(
                'quantity'
            )
        )

        auction = (
            get_object_or_404(
                Auction,
                id=auction_id
            )
        )

        item = (
            get_object_or_404(
                Item,
                id=item_id
            )
        )

        value = float(
            item.price
        )

        sub_total = (
            value *
            quantity
        )

        AuctionItem.objects.create(
            auction=auction,
            item=item,
            quantity=quantity,
            value=value,
            sub_total=sub_total
        )

        return redirect(
            'auctionitem:list_auctionitems'
        )

    context = {
        'auctions':
        auctions,
        'items':
        items
    }

    return render(
        request,
        template_name,
        context
    )


def edit_auctionitem(
    request,
    id_auctionitem
):

    template_name = (
        'auctionitem/'
        'edit_auctionitem.html'
    )

    auctionitem = (
        get_object_or_404(
            AuctionItem,
            id=id_auctionitem
        )
    )

    auctions = (
        Auction.objects.all()
    )

    items = (
        Item.objects.all()
    )

    if request.method == 'POST':

        quantity = int(
            request.POST.get(
                'quantity'
            )
        )

        auction_id = (
            request.POST.get(
                'auction'
            )
        )

        item_id = (
            request.POST.get(
                'item'
            )
        )

        auctionitem.auction = (
            get_object_or_404(
                Auction,
                id=auction_id
            )
        )

        auctionitem.item = (
            get_object_or_404(
                Item,
                id=item_id
            )
        )

        auctionitem.quantity = (
            quantity
        )

        auctionitem.value = (
            float(
                auctionitem
                .item
                .price
            )
        )

        auctionitem.sub_total = (
            auctionitem.value *
            quantity
        )

        auctionitem.save()

        return redirect(
            'auctionitem:list_auctionitems'
        )

    context = {
        'auctionitem':
        auctionitem,
        'auctions':
        auctions,
        'items':
        items
    }

    return render(
        request,
        template_name,
        context
    )


def delete_auctionitem(
    request,
    id_auctionitem
):

    auctionitem = (
        get_object_or_404(
            AuctionItem,
            id=id_auctionitem
        )
    )

    auctionitem.delete()

    return redirect(
        'auctionitem:list_auctionitems'
    )
