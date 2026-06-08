from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'user'

router = routers.SimpleRouter()
router.register('', views.UserViewSet, basename='Usuários')

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('listar/', views.list_users, name='list_users'),
    path('adicionar/', views.add_user, name='add_user'),
    path('editar/<int:id_user>/', views.edit_user, name='edit_user'),
    path('excluir/<int:id_user>/', views.delete_user, name='delete_user'),
    path('buscar/', views.search_users, name='search_users'),
    path('visualizar/<int:id_user>/', views.view_user, name='view_user'),
    path('', include(router.urls) )
]