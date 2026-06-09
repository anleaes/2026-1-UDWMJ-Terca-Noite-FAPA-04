from django.apps import apps
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuctioneerForm
from .models import Auctioneer
from rest_framework import viewsets
from .serializer import AuctioneerSerializer

def login_auctioneer(request):
    template_name = 'auctioneer/auctioneer_login.html'
    error = ''

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        auctioneer = Auctioneer.objects.filter(email=email, password=password).first()
        if auctioneer:
            request.session['auth'] = {
                'role': 'auctioneer',
                'id': auctioneer.id,
                'name': f'{auctioneer.first_name} {auctioneer.last_name}',
                'email': auctioneer.email,
            }
            request.session.modified = True
            return redirect('auctioneer:view_auctioneer', auctioneer.id)

        error = 'Email ou senha inválidos.'

    return render(request, template_name, {'error': error})


def add_auctioneer(request):
    template_name = 'auctioneer/add_auctioneer.html'
    context = {}
    if request.method == 'POST':
        form = AuctioneerForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            return redirect('auctioneer:list_auctioneers')
    form = AuctioneerForm()
    context['form'] = form
    return render(request, template_name, context)

def list_auctioneers(request):
    template_name = 'auctioneer/list_auctioneers.html'
    auctioneers = Auctioneer.objects.filter()
    context = {
        'auctioneers': auctioneers,
    }
    return render(request, template_name, context)

def edit_auctioneer(request, id_auctioneer):
    template_name = 'auctioneer/add_auctioneer.html'
    context ={}
    auctioneer = get_object_or_404(Auctioneer, id=id_auctioneer)
    if request.method == 'POST':
        form = AuctioneerForm(request.POST, instance=auctioneer)
        if form.is_valid():
            form.save()
            return redirect('auctioneer:list_auctioneers')
    form = AuctioneerForm(instance=auctioneer)
    context['form'] = form
    return render(request, template_name, context)

def delete_auctioneer(request, id_auctioneer):
    auctioneer = Auctioneer.objects.get(id=id_auctioneer)
    auctioneer.delete()
    return redirect('auctioneer:list_auctioneers')


def view_auctioneer(request, id_auctioneer):
    template_name = 'auctioneer/view_auctioneer.html'
    auctioneer = get_object_or_404(Auctioneer, id=id_auctioneer)
    Auction = apps.get_model('auction', 'Auction')

    auctions = (
        Auction.objects
        .filter(auctioneer=auctioneer)
        .prefetch_related('auction_items', 'auction_items__item')
    )

    selected_auction = None
    auction_id = request.GET.get('auction_id')
    if auction_id:
        try:
            auction_id = int(auction_id)
        except (TypeError, ValueError):
            auction_id = None

    if auction_id is not None:
        selected_auction = (
            Auction.objects
            .filter(id=auction_id, auctioneer=auctioneer)
            .prefetch_related('auction_items', 'auction_items__item')
            .first()
        )

    context = {
        'auctioneer': auctioneer,
        'auctions': auctions,
        'selected_auction': selected_auction,
    }
    return render(request, template_name, context)


class AuctioneerViewSet(viewsets.ModelViewSet):
    queryset = Auctioneer.objects.all()
    serializer_class = AuctioneerSerializer
