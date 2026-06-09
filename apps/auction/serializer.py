from auction.models import Auction
from rest_framework import serializers

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'