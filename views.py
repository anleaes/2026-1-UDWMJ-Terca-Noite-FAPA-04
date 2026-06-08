from django.shortcuts import render, redirect, get_object_or_404
from core.auth import get_auth, user_required
from user.models import User
from .models import PaymentMethod
from .forms import PaymentMethodForm

