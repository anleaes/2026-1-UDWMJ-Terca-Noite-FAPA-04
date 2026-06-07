from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('listar/', views.list_items, name='list_items'),
    path('adicionar/', views.add_item, name='add_item'),
    path('editar/<int:id_item>/', views.edit_item, name='edit_item'),
    path('excluir/<int:id_item>/', views.delete_item, name='delete_item'),
]