from django.shortcuts import render, get_object_or_404
from receiptpayment.models import Receipt
from .serializer import ReceiptPaymentSerializer
from rest_framework import viewsets

def create_receipt_for_auction(auction, payment=None):
    receipt = (
        Receipt.objects
        .filter(
            auction=auction
        )
        .first()
    )

    if receipt:
        if payment and receipt.payment_id != payment.id:
            receipt.payment = payment
            receipt.save(
                update_fields=[
                    'payment'
                ]
            )
        return receipt

    receipt_number = f'Recibo-{auction.id:06d}'

    return Receipt.objects.create(
        auction=auction,
        number=receipt_number,
        payment=payment
    )

def view_receipt(request, receipt_id):
    template_name = 'receiptpayment/view_receiptpayment.html'
    receipt = get_object_or_404(Receipt, id=receipt_id)
    items = receipt.auction.auction_items.all()
    total = sum(
        auction_item.sub_total or auction_item.value * auction_item.quantity
        for auction_item in items
    )

    context = {
        'receipt': receipt,
        'auction': receipt.auction,
        'items': items,
        'total': total
    }
    return render(request, template_name, context)


class ReceiptPaymentViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptPaymentSerializer
