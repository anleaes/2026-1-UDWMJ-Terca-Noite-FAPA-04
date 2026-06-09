from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from auctionitem.models import AuctionItem
from auction.models import Auction
from user.models import User
from payment.models import Payment
from core.auth import user_required, get_auth
from auctionbid.models import AuctionBid
from .serializer import AuctionItemSerializer
from rest_framework import viewsets
from receiptpayment.views import (
    create_receipt_for_auction
)


def _money(value):
    try:
        return Decimal(str(value)).quantize(Decimal('0.01'))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal('0.00')


def _cart_total(cart):
    return sum(
        _money(item.get('subtotal', 0))
        for item in cart.values()
    )


def _cart_item(auction_item, auction_bid, quantity):
    price = _money(auction_item.value)
    subtotal = price * quantity

    return {
        'name': auction_item.item.name,
        'price': str(price),
        'quantity': quantity,
        'subtotal': str(subtotal),
        'auction_id': auction_item.auction_id,
        'bid_id': auction_bid.id
    }


def _delete_pending_bid(cart_item, user):
    bid_id = cart_item.get('bid_id')

    if not bid_id:
        return

    AuctionBid.objects.filter(
        id=bid_id,
        user=user,
        status='P'
    ).delete()


def _save_pending_bid(user, auction_item, value):
    auction_bid = (
        AuctionBid.objects
        .filter(
            user=user,
            auction=auction_item.auction,
            auctionitem=auction_item,
            status='P'
        )
        .order_by('-id')
        .first()
    )

    if auction_bid:
        auction_bid.value = value
        auction_bid.save(
            update_fields=[
                'value'
            ]
        )
        return auction_bid

    return AuctionBid.objects.create(
        user=user,
        auction=auction_item.auction,
        auctionitem=auction_item,
        value=value,
        status='P'
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

    total = _cart_total(bid)

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
    auth = get_auth(request)
    user = get_object_or_404(User, id=auth['id'])

    if auction.status != 'Em andamento':

        return redirect(
            'auction:view_auctions',
            auction_id=auction.id
        )

    bid = request.session.get(
        'bid',
        {}
    )

    pid = str(
        auction_item.id
    )

    if bid:
        current_auction_id = next(iter(bid.values())).get('auction_id')
        if str(current_auction_id) != str(auction.id):
            messages.warning(
                request,
                'Finalize ou esvazie os lances do leilão atual antes de adicionar itens de outro leilão.'
            )
            return redirect(
                'auctionitem:bids'
            )

    if pid in bid:

        quantity = int(
            bid[pid].get(
                'quantity',
                1
            )
        ) + 1

    else:

        quantity = 1

    if auction_item.quantity and quantity > auction_item.quantity:
        messages.warning(
            request,
            'A quantidade solicitada é maior que a disponível para este item.'
        )
        return redirect(
            'auctionitem:bids'
        )

    value = _money(auction_item.value) * quantity

    auction_bid = _save_pending_bid(
        user=user,
        auction_item=auction_item,
        value=value
    )

    bid[pid] = _cart_item(
        auction_item,
        auction_bid,
        quantity
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

        try:
            quantity = int(
                request.POST.get(
                    'quantity',
                    1
                )
            )
        except (TypeError, ValueError):
            quantity = 1

        bid = request.session.get(
            'bid',
            {}
        )

        pid = str(item_id)
        auth = get_auth(request)
        user = get_object_or_404(User, id=auth['id'])

        if pid in bid:

            if quantity <= 0:

                _delete_pending_bid(
                    bid[pid],
                    user
                )
                del bid[pid]

            else:

                auction_item = get_object_or_404(
                    AuctionItem,
                    id=item_id
                )

                if auction_item.quantity and quantity > auction_item.quantity:
                    messages.warning(
                        request,
                        'A quantidade solicitada é maior que a disponível para este item.'
                    )
                    return redirect(
                        'auctionitem:bids'
                    )

                value = _money(
                    auction_item.value
                ) * quantity

                auction_bid = _save_pending_bid(
                    user=user,
                    auction_item=auction_item,
                    value=value
                )

                bid[pid] = _cart_item(
                    auction_item,
                    auction_bid,
                    quantity
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
    auth = get_auth(request)
    user = get_object_or_404(User, id=auth['id'])

    if pid in bid:

        _delete_pending_bid(
            bid[pid],
            user
        )
        del bid[pid]

    request.session['bid'] = bid
    request.session.modified = True

    return redirect(
        'auctionitem:bids'
    )


@user_required
def checkout(request):

    template_name = 'auctionitem/checkout.html'

    bid = request.session.get(
        'bid',
        {}
    )

    total = _cart_total(bid)

    auth = get_auth(request)
    user = get_object_or_404(
        User,
        id=auth['id']
    )

    payments = user.payment.all()
    
    if request.method == 'POST':

        if not bid:
            return redirect(
                'auctionitem:bids'
            )

        payment_id = request.POST.get(
            'payment_id'
        )

        if not payment_id:
            messages.warning(
                request,
                'Selecione uma forma de pagamento.'
            )
            return redirect(
                'auctionitem:checkout'
            )

        selected_payment = get_object_or_404(
            Payment,
            id=payment_id,
            is_active=True
        )

        has_payment = user.payment.through.objects.filter(
            user=user,
            payment=selected_payment
        ).exists()

        if not has_payment:
            messages.warning(
                request,
                'Forma de pagamento inválida.'
            )
            return redirect(
                'auctionitem:checkout'
            )

        first_item_id = next(iter(bid))

        auction_item = get_object_or_404(
            AuctionItem,
            id=first_item_id
        )

        auction = auction_item.auction

        if auction.status != 'Em andamento':
            return redirect(
                'auction:view_auctions',
                auction_id=auction.id
            )

        cart_auction_ids = {
            str(item.get('auction_id'))
            for item in bid.values()
        }

        if cart_auction_ids != {str(auction.id)}:
            messages.warning(
                request,
                'O carrinho deve conter itens de apenas um leilão.'
            )
            return redirect(
                'auctionitem:bids'
            )

        for item_id, item in bid.items():

            auction_item = get_object_or_404(
                AuctionItem,
                id=item_id,
                auction=auction
            )

            quantity = int(
                item['quantity']
            )

            if (
                auction_item.quantity
                and quantity > auction_item.quantity
            ):
                messages.warning(
                    request,
                    'A quantidade solicitada é maior que a disponível para este item.'
                )
                return redirect(
                    'auctionitem:bids'
                )

        with transaction.atomic():

            auction.status = 'Finalizado'
            auction.save()

            accepted_bid_ids = []

            for item_id, item in bid.items():

                auction_item = get_object_or_404(
                    AuctionItem,
                    id=item_id,
                    auction=auction
                )

                subtotal = _money(
                    item['subtotal']
                )

                auction_item.sub_total = float(
                    subtotal
                )

                auction_item.save(
                    update_fields=[
                        'sub_total'
                    ]
                )

                bid_id = item.get(
                    'bid_id'
                )

                if bid_id:

                    auction_bid = get_object_or_404(
                        AuctionBid,
                        id=bid_id,
                        user=user,
                        auction=auction,
                        auctionitem=auction_item
                    )

                    auction_bid.value = subtotal
                    auction_bid.status = 'A'

                    auction_bid.save(
                        update_fields=[
                            'value',
                            'status'
                        ]
                    )

                    accepted_bid_ids.append(
                        auction_bid.id
                    )

                else:

                    auction_bid = AuctionBid.objects.create(
                        auction=auction,
                        auctionitem=auction_item,
                        user=user,
                        value=subtotal,
                        status='A'
                    )

                    accepted_bid_ids.append(
                        auction_bid.id
                    )

            for pending_bid in AuctionBid.objects.filter(
                auction=auction,
                status='P'
            ).only(
                'id',
                'status'
            ):
                if pending_bid.id in accepted_bid_ids:
                    continue

                pending_bid.status = 'R'
                pending_bid.save(
                    update_fields=[
                        'status'
                    ]
                )

            create_receipt_for_auction(
                auction,
                selected_payment
            )

        request.session['bid'] = {}
        request.session.modified = True

        return redirect(
            'auction:view_auctions',
            auction_id=auction.id
        )

    context = {
        'bid': bid,
        'total': total,
        'current_user': user,
        'payments': payments,
        'auction': (
            Auction.objects
            .filter(
                id=next(
                    iter(
                        bid.values()
                    )
                ).get(
                    'auction_id'
                )
            )
            .select_related(
                'auctioneer'
            )
            .first()
            if bid
            else None
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
        .filter(
            auction__status='Em andamento'
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

class AuctionItemViewSet(viewsets.ModelViewSet):
    queryset = AuctionItem.objects.all()
    serializer_class = AuctionItemSerializer
