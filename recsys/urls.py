from django.urls import path, include
from .views import *

urlpatterns = [
    path('', SimilarBooksView, name="sim-books"),
    path('<str:username>/', RecommendedBooksView, name="rec-books"),
]