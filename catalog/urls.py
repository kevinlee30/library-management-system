from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home.as_view(), name="api-root"),
    path('most-popular-books/', MostPopularBooks, name="most-popular-books"),
    path('recent-release-books/', RecentReleaseBooks, name="recent-release-books"),
]
