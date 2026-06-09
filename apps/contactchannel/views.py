from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactchannelForm
from .models import Contactchannel
from .serializer import ContactChannelSerializer
from rest_framework import viewsets

def add_contactchannel(request):
    template_name = 'contactchannel/add_contactchannel.html'
    context = {}
    if request.method == 'POST':
        form = ContactchannelForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            return redirect('contactchannel:list_contactchannels')
    form = ContactchannelForm()
    context['form'] = form
    return render(request, template_name, context)

def list_contactchannels(request):
    template_name = 'contactchannel/list_contactchannels.html'
    contactchannels = Contactchannel.objects.filter()
    context = {
        'contactchannel': contactchannels
    }
    return render(request, template_name, context)

def edit_contactchannel(request, id_contactchannel):
    template_name = 'contactchannel/add_contactchannel.html'
    context ={}
    contactchannel = get_object_or_404(Contactchannel, id=id_contactchannel)
    if request.method == 'POST':
        form = ContactchannelForm(request.POST, instance=contactchannel)
        if form.is_valid():
            form.save()
            return redirect('contactchannel:list_contactchannels')
    form = ContactchannelForm(instance=contactchannel)
    context['form'] = form
    return render(request, template_name, context)

def delete_contactchannel(request, id_contactchannel):
    contactchannel = Contactchannel.objects.get(id=id_contactchannel)
    contactchannel.delete()
    return redirect('contactchannel:list_contactchannels')

class ContactChannelViewSet(viewsets.ModelViewSet):
    queryset = Contactchannel.objects.all()
    serializer_class = ContactChannelSerializer
