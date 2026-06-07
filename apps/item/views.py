from django.shortcuts import render, get_object_or_404, redirect

from .forms import ItemForm
from .models import Item

def add_item(request):
    template_name = 'item/add_item.html'
    context = {}
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            return redirect('item:list_items')
    form = ItemForm()
    context['form'] = form
    return render(request, template_name, context)

def list_items(request):
    template_name = 'item/list_items.html'
    items = Item.objects.filter()
    context = {
        'items': items
    }
    return render(request, template_name, context) 

def edit_item(request, id_item):
    template_name = 'item/add_item.html'
    context ={}
    item = get_object_or_404(Item, id=id_item)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES,  instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:list_items')
    form = ItemForm(instance=item)
    context['form'] = form
    return render(request, template_name, context)

def delete_item(request, id_item):
    item = Item.objects.get(id=id_item)
    item.delete()
    return redirect('item:list_items')
