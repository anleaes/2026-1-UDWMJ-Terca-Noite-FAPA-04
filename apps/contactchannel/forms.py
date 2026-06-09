from django import forms
from .models import Contactchannel

class ContactchannelForm(forms.ModelForm):

    class Meta:
        model = Contactchannel
        exclude = ()