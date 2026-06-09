from django.shortcuts import render, get_object_or_404
from receiptpayment.models import Receipt

def create_receipt_for_auction(source):
    auction = source.auction if hasattr(source, 'auction') else source
    if hasattr(auction, 'receipt'):
        if hasattr(source, 'auction') and auction.receipt.payment_id != source.id:
            auction.receipt.payment = source
            auction.receipt.save(update_fields=['payment'])
        return auction.receipt

    receipt_number = f'Recibo-{auction.id:06d}'

    return Receipt.objects.create(
        auction=auction,
        number=receipt_number,
        payment=source if hasattr(source, 'auction') else None
    )

