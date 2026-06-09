from django.urls import path, include
from payment import views
from rest_framework import routers

app_name = 'payment'

router = routers.SimpleRouter()
router.register('', views.PaymentViewSet, basename='Pagamentos')

urlpatterns = [
    path('', views.list_payments, name='list_payments'),
    path('add/', views.add_payment, name='add_payment'),
    path('edit/<int:id_payment>/', views.edit_payment, name='edit_payment'),
    path('delete/<int:id_payment>/', views.delete_payment, name='delete_payment'),
    path('', include(router.urls) )
]
