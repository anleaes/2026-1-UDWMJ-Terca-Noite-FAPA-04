from django.urls import path

app_name = 'payment'

urlpatterns = [
    path('', views.list_payments, name='list_payments'),
    path('add/', views.add_payment, name='add_payment'),
    path('edit/<int:id_payment>/', views.edit_payment, name='edit_payment'),
    path('delete/<int:id_payment>/', views.delete_payment, name='delete_payment'),
]
