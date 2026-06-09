from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'ReceiptPayment'

router = routers.SimpleRouter()
router.register('', views.ReceiptPaymentViewSet, basename='RecibosPagamentos')

urlpatterns = [
    path('<int:receipt_id>/', views.view_receipt, name='view_receipt'),
    path('', include(router.urls) )
]