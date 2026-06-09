from django import forms
from .models import Auctioneer

class AuctioneerForm(forms.ModelForm):

    class Meta:
        model = Auctioneer
        exclude = ()