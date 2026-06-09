from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm
from .models import User, Contactchannel
from .serializer import UserSerializer
from rest_framework import viewsets

def add_user(request):
    template_name = 'user/add_user.html'
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            return redirect('user:list_users')
    form = UserForm()
    context['form'] = form
    return render(request, template_name, context)

def list_users(request):
    template_name = 'user/list_users.html'
    users = User.objects.prefetch_related('contactchannel')
    context = {
        'users': users,
    }
    return render(request, template_name, context)

def edit_user(request, id_user):
    template_name = 'user/add_user.html'
    context ={}
    user = get_object_or_404(User, id=id_user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user:view_user', user.id)
    form = UserForm(instance=user)
    context['form'] = form
    return render(request, template_name, context)

def delete_user(request, id_user):
    user = User.objects.get(id=id_user)
    user.delete()
    return redirect('user:list_users')


def login_user(request):
    template_name = 'user/user_login.html'
    error = ''

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email, password=password).first()
        if user:
            request.session['auth'] = {
                'role': 'user',
                'id': user.id,
                'name': f'{user.first_name} {user.last_name}',
                'email': user.email,
            }
            request.session.modified = True
            return redirect('user:view_user', id_user=user.id)

        error = 'Email ou senha inválidos.'

    return render(request, template_name, {'error': error})


def logout_user(request):
    request.session.pop('auth', None)
    request.session.modified = True
    return redirect('core:home')


def search_users(request):
    template_name = 'user/list_users.html'
    query = request.GET.get('query')
    contactchannels = Contactchannel.objects.filter()
    users = User.objects.filter(last_name__icontains=query)
    context = {
        'users': users,
        'contactchannels': contactchannels,
    }
    return render(request,template_name, context)

def view_user(request, id_user):
    template_name = 'user/view_user.html'
    user = get_object_or_404(User, id=id_user)

    from django.apps import apps
    Auction = apps.get_model('auction', 'Auction')

    auctions = (
    Auction.objects
    .filter(status='Em andamento')
    .prefetch_related('auction_items', 'auction_items__item')
    )

    selected_auction = None

    auction_id = request.GET.get('auction_id')

    if auction_id:
        selected_auction = (
        Auction.objects
        .filter(id=auction_id)
        .prefetch_related('auction_items', 'auction_items__item')
        .first()
    )

    bids = user.auction_bids.select_related(
        'auctionitem__item',
        'auction'
    ).order_by('-id')

    context = {
        'user': user,
        'auctions': auctions,
        'selected_auction': selected_auction,
        'bids': bids,
    }
    return render(request, template_name, context)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

