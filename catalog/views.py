from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.decorators import api_view

from .models import *
from .serializers import *

from rest_framework import viewsets

class home(APIView):
    def get(self, request):
        return Response({
            "Most Popular Books": reverse_lazy("most-popular-books", request=request),
            "Recent Release Books": reverse_lazy("recent-release-books", request=request),
        })

# from rest_framework import generics
# class MostPopularBooks(viewsets.ModelViewSet):
#     queryset = Book.objects.all()
#     serializer_class = MostPopularBookSerializer

@api_view(['GET'])
def MostPopularBooks(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def RecentReleaseBooks(request):
    if request.method == 'GET':
        books = Book.objects.all().order_by('-pubYear').values()[:10]
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)