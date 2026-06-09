from contactchannel.models import Contactchannel
from rest_framework import serializers

class ContactChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactchannel
        fields = '__all__'