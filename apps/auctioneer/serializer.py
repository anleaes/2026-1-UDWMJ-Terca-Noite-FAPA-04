from auctioneer.models import Auctioneer
from rest_framework import serializers

class AuctioneerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auctioneer
        fields = '__all__'