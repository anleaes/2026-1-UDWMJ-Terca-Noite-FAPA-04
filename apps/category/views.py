from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm
from .models import Category
from .serializer import CategorySerializer
from rest_framework import viewsets

# Create your views here.

def add_category(request):
    template_name = 'category/add_category.html'
    context = {}
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            return redirect('category:list_categories')
    form = CategoryForm()
    context['form'] = form
    return render(request, template_name, context)

def list_categories(request):
    template_name = 'category/list_categories.html'
    categories = Category.objects.filter()
    context = {
        'categories': categories
    }
    return render(request, template_name, context)

def edit_category(request, id_category):
    template_name = 'category/add_category.html'
    context ={}
    category = get_object_or_404(Category, id=id_category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category:list_categories')
    form = CategoryForm(instance=category)
    context['form'] = form
    return render(request, template_name, context)

def delete_category(request, id_category):
    category = Category.objects.get(id=id_category)
    category.delete()
    return redirect('category:list_categories')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
