from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics

from .models import *
from .serializers import *



class WrittenPostView(generics.ListAPIView):
    def get_queryset(self):
        concernBoard
        return super().get_queryset()
    
