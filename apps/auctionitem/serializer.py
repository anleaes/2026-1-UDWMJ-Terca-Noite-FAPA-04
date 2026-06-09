from auctionitem.models import AuctionItem
from rest_framework import serializers

class AuctionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionItem
        fields = '__all__'