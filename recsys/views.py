from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from catalog.models import Book, Borrowing
from recsys.serializers import BookListSerializer

from random import sample
        
@api_view(['GET'])
def SimilarBooksView(request):
    if request.method == 'GET':
        input_books = request.GET.getlist('id', '')
        
        if input_books == "":
            books = Book.objects.filter(borrowed__gte = 100).order_by('?')[:6]
            serializer = BookListSerializer(books, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        else:
            input = ""
            
            books = Book.objects.filter(borrowed__gte = 100)
            
            common_books = pd.DataFrame(list(Book.objects.all().values('id', 'title', 'author', 'publisher', 'category', 'pubYear', 'imgUrl')))
            target_cols = ['title','author','publisher','category']
            common_books['combined_features'] = [' '.join(common_books[target_cols].iloc[i,].values) for i in range(common_books[target_cols].shape[0])]
            
            for id in input_books:
                input += Book.objects.filter(id = id).values('title')[0]['title'] + " "
                input += Book.objects.filter(id = id).values('author')[0]['author'] + " "
                input += Book.objects.filter(id = id).values('publisher')[0]['publisher'] + " "
                input += Book.objects.filter(id = id).values('category')[0]['category'] + " "
                common_books = common_books[common_books.id != id]    
            
            new_row = common_books.iloc[-1]
            common_books = common_books.append(new_row,ignore_index=True)
            common_books.iloc[-1, common_books.columns.get_loc('combined_features')] = input
                    
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(common_books['combined_features'])
            cosine_sim = cosine_similarity(count_matrix)
            
            sim_books = list(enumerate(cosine_sim[-1]))
            sorted_sim_books = sorted(sim_books,key=lambda x:x[1],
                                        reverse=True)[1:10]
            sorted_sim_books = sample(sorted_sim_books, 6)
            books = common_books.loc[[sorted_sim_books[0][0]]]
            
            for i in range(1, len(sorted_sim_books)):
                books = pd.concat([books, common_books.loc[[sorted_sim_books[i][0]]]])
            
            return Response(books.to_dict('record'), status = status.HTTP_200_OK)
            
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def RecommendedBooksView(request, username):
    if request.method == 'GET':
        borrowed_books = Borrowing.objects.filter(user__username = username).values('book_id')
    
        if len(borrowed_books) == 0:
            books = Book.objects.filter(borrowed__gte = 100).order_by('?')[:6]
            serializer = BookListSerializer(books, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        else:
            input_books = []
            for book in borrowed_books:
                input_books.append(book["book_id"])
            
            input = ""
            
            books = Book.objects.filter(borrowed__gte = 100)
            
            common_books = pd.DataFrame(list(Book.objects.all().values('id', 'title', 'author', 'publisher', 'category', 'pubYear', 'imgUrl')))
            target_cols = ['title','author','publisher','category']
            common_books['combined_features'] = [' '.join(common_books[target_cols].iloc[i,].values) for i in range(common_books[target_cols].shape[0])]
            
            for id in input_books:
                input += Book.objects.filter(id = id).values('title')[0]['title'] + " "
                input += Book.objects.filter(id = id).values('author')[0]['author'] + " "
                input += Book.objects.filter(id = id).values('publisher')[0]['publisher'] + " "
                input += Book.objects.filter(id = id).values('category')[0]['category'] + " "
                common_books = common_books[common_books.id != id]    
            
            new_row = common_books.iloc[-1]
            common_books = common_books.append(new_row,ignore_index=True)
            common_books.iloc[-1, common_books.columns.get_loc('combined_features')] = input
                    
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(common_books['combined_features'])
            cosine_sim = cosine_similarity(count_matrix)
            
            sim_books = list(enumerate(cosine_sim[-1]))
            sorted_sim_books = sorted(sim_books,key=lambda x:x[1],
                                        reverse=True)[1:10]
            sorted_sim_books = sample(sorted_sim_books, 6)
            books = common_books.loc[[sorted_sim_books[0][0]]]
            
            for i in range(1, len(sorted_sim_books)):
                books = pd.concat([books, common_books.loc[[sorted_sim_books[i][0]]]])
            
            return Response(books.to_dict('record'), status = status.HTTP_200_OK)
        