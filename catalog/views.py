from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from django.db.models import Q

from .models import *
from .serializers import *
from .copywrite.email import newUserEmail, newBorrowingEmail

class home(APIView):
    def get(self, request):
        return Response({
            "Highlight Books": reverse_lazy("highlight-books", request=request),
            "Recent Release Books": reverse_lazy("recent-release-books", request=request),
            "Book List": reverse_lazy("book-list", request=request),
            "User List": reverse_lazy("user-list", request=request),
            "Borrowing List": reverse_lazy("borrowing-list", request=request),
        })



@api_view(['GET'])
def RecentReleaseBooksView(request):
    if request.method == 'GET':
        paramsDict = request.GET
        
        numLim = None
        if "num" in paramsDict:
            numLim = int(paramsDict.get("num"))
            
        books = Book.objects.all().order_by('-pubYear').values()[:numLim]
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
def BookListView(request):
    if request.method == 'GET':
        paramsDict = request.GET
        
        numLim = None
        if "num" in paramsDict:
            numLim = int(paramsDict.get("num"))
        
        if "search" in paramsDict:
            books = Book.objects.filter(Q(title__icontains=paramsDict.get("search")) | Q(author__icontains=paramsDict.get("search")) | Q(isbn=paramsDict.get("search"))).order_by("-pubYear")[:numLim]
        elif "cat" in paramsDict:
            books = Book.objects.filter(
                category = paramsDict.get("cat")
            )[:numLim]
        else:
            books = Book.objects.all()[:numLim]
            
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])   
def BookDetailView(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookDetailSerializer(book)
        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def UserListView(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = AuthUserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            copywrite = newUserEmail(serializer.data["username"])
            subject = copywrite.subject
            message = copywrite.message
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [serializer.data["email"], ]
            send_mail( subject, message, email_from, recipient_list )
            return Response(serializer.data, status=status.HTTP_201_CREATED)     
        else:
            return Response("400 INVALID REQUEST", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def UserDetailView(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def BorrowingListView(request):
    if request.method == 'GET':
        paramsDict = request.GET
        if "user" in paramsDict:
            borrowings = Borrowing.objects.filter(user__username=paramsDict.get("user"))
            serializer = BorrowedBookSerializer(borrowings, many=True)
        elif "book" in paramsDict:
            borrowings = Borrowing.objects.filter(book__id=paramsDict.get("book"))
            serializer = BorrowingListSerializer(borrowings, many=True)
        else:
            borrowings = Borrowing.objects.all()
            serializer = BorrowingListSerializer(borrowings, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = BorrowingDetailSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            book = Book.objects.get(id=serializer.data['book'])
            book.borrowed += 1
            book.save(update_fields=['borrowed'])
            user = User.objects.get(username=serializer.data["user"])
            copywrite = newBorrowingEmail(serializer.data["user"], serializer.data["id"], book.title, serializer.data["startDate"], serializer.data["endDate"])
            subject = copywrite.subject
            message = copywrite.message
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response("400 INVALID REQUEST", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])   
def BorrowingDetailView(request, id):
    try:
        borrowing = Borrowing.objects.get(id=id)
    except Borrowing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BorrowingDetailSerializer(borrowing)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = BorrowingDetailSerializer(borrowing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        borrowing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def HighlightView(request):
    if request.method == 'GET':
        highlight = Highlight.objects.all()
        serializer = HighlightSerializer(highlight, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
