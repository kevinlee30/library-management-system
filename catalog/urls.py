from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home.as_view(), name="api-root"),
    path('highlight/', HighlightView, name="highlight-books"),
    path('recent-release/', RecentReleaseBooksView, name="recent-release-books"),
    path('book/', BookListView, name="book-list"),
    path('book/<uuid:id>', BookDetailView, name="book-detail"),
    path('user/', UserListView, name="user-list"),
    path('user/<str:username>', UserDetailView, name="user-detail"),
    path('borrowing/', BorrowingListView, name="borrowing-list"),
    path('borrowing/<uuid:id>', BorrowingDetailView, name="borrowing-detail"),
]
