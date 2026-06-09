from django.shortcuts import render, redirect, get_object_or_404
from core.auth import get_auth, user_required
from user.models import User
from .models import Payment
from .forms import PaymentForm
from .serializer import PaymentSerializer
from rest_framework import viewsets

@user_required
def add_payment(request):

    template_name = 'payment/add_payment.html'

    auth = get_auth(request)
    user = get_object_or_404(
        User,
        id=auth['id']
    )

    if request.method == 'POST':

        form = PaymentForm(request.POST)

        if form.is_valid():

            payment = form.save()

            user.payment.add(payment)

            return redirect(
                'payment:list_payments'
            )

    else:

        form = PaymentForm()

    return render(
        request,
        template_name,
        {
            'form': form
        }
    )

@user_required
def list_payments(request):

    template_name = 'payment/list_payments.html'

    auth = get_auth(request)

    user = get_object_or_404(
        User,
        id=auth['id']
    )

    payments = user.payment.all()

    context = {
        'payments': payments
    }

    return render(
        request,
        template_name,
        context
    )

@user_required
def edit_payment(request, id_payment):

    template_name = 'payment/add_payment.html'

    auth = get_auth(request)

    user = get_object_or_404(
        User,
        id=auth['id']
    )

    payment = get_object_or_404(
        user.payment.all(),
        id=id_payment
    )

    if request.method == 'POST':

        form = PaymentForm(
            request.POST,
            instance=payment
        )

        if form.is_valid():

            form.save()

            return redirect(
                'payment:list_payments'
            )

    else:

        form = PaymentForm(
            instance=payment
        )

    context = {
        'form': form
    }

    return render(
        request,
        template_name,
        context
    )

@user_required
def delete_payment(
    request,
    id_payment
):

    auth = get_auth(request)

    user = get_object_or_404(
        User,
        id=auth['id']
    )

    payment = get_object_or_404(
        user.payment.all(),
        id=id_payment
    )

    user.payment.remove(payment)

    payment.delete()

    return redirect(
        'payment:list_payments'
    )

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
