from auctionbid.models import AuctionBid
from rest_framework import serializers

class AuctionBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionBid
        fields = '__all__'