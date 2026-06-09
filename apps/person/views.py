from django.shortcuts import render
from .serializer import PersonSerializer
from rest_framework import viewsets
from person.models import Person

# Create your views here.
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

