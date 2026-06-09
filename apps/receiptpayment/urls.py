from django.urls import path
from . import views

app_name = 'ReceiptPayment'

urlpatterns = [
    path('<int:receipt_id>/', views.view_receipt, name='view_receipt'),
] 