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

def view_receipt(request, receipt_id):
    template_name = 'receiptpayment/view_receiptpayment.html'
    receipt = get_object_or_404(Receipt, id=receipt_id)
    total = (
        receipt.payment.total
        if receipt.payment
        else sum(
            auction_item.value * auction_item.quantity
            for auction_item in receipt.auction.auction_items.all()
        )
    )

    context = {
        'receipt': receipt,
        'auction': receipt.auction,
        'items': receipt.auction.auction_items.all(),
        'total': total
    }
    return render(request, template_name, context)
