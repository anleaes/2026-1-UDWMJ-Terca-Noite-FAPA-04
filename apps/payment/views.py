from django.shortcuts import render, redirect, get_object_or_404
from core.auth import get_auth, user_required
from user.models import User
from .models import PaymentMethod
from .forms import PaymentMethodForm


@user_required
def add_payment(request):
    template_name = 'payment/add_payment.html'
    auth = get_auth(request)
    user = get_object_or_404(User, id=auth['id'])

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.user = user
            payment_method.save()
            return redirect('payment:list_payments')

    form = PaymentMethodForm()
    context = {
        'form': form
    }

    return render(request, template_name, context)


@user_required
def list_payments(request):
    template_name = 'payment/list_payments.html'
    auth = get_auth(request)
    user = get_object_or_404(User, id=auth['id'])
    payments = PaymentMethod.objects.filter(user=user)
    context = {
        'payments': payments
    }
    return render(request, template_name, context)


@user_required
def edit_payment(request, id_payment):
    template_name = 'payment/add_payment.html'
    auth = get_auth(request)
    user = get_object_or_404(User, id=auth['id'])
    payment = get_object_or_404(
        PaymentMethod,
        id=id_payment,
        user=user
    )

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment:list_payments')

    form = PaymentMethodForm(instance=payment)
    context = {
        'form': form
    }

    return render(request, template_name, context)


@user_required
def delete_payment(request, id_payment):
    auth = get_auth(request)
    user = get_object_or_404(User, id=auth['id'])
    payment = get_object_or_404(
        PaymentMethod,
        id=id_payment,
        user=user
    )
    payment.delete()
    return redirect('payment:list_payments')
