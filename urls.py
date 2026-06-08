from django.urls import path
from . import views

app_name = 'contactchannel'

urlpatterns = [
    path('listar/', views.list_contactchannels, name='list_contactchannels'),
    path('adicionar/', views.add_contactchannel, name='add_contactchannel'),
    path('editar/<int:id_contactchannel>/', views.edit_contactchannel, name='edit_contactchannel'),
    path('excluir/<int:id_contactchannel>/', views.delete_contactchannel, name='delete_contactchannel'),
]