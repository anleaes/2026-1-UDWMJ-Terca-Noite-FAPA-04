from receiptpayment.models import Receipt
from rest_framework import serializers

class ReceiptPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'