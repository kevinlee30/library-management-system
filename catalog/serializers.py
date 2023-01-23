from rest_framework import serializers
from .models import *

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'pubYear', 'imgUrl']
        
class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        
class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            'password': {"write_only": True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
class BorrowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ['id', 'book', 'startDate', 'endDate', 'isReturned']
        
class BorrowingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"
    
    def validate(self, data):
        if data['startDate'] > data['endDate']:
            raise serializers.ValidationError("finish must occur after start")
        books = Borrowing.objects.filter(book=data['book']).values('startDate', 'endDate')
        for book in books:
            print(book)
            if (data['startDate'] >= book["startDate"] and data['startDate'] <= book["endDate"]) or (data['endDate'] >= book["startDate"] and data['endDate'] <= book["endDate"]):
               raise serializers.ValidationError("Book is not available at inputed dates") 
        return data

class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = "__all__"



class BorrowedBookSerializer(serializers.ModelSerializer):
    book = BookListSerializer(many=False, read_only=True)
    class Meta:
        model = Borrowing
        fields = ["id", "endDate", "book", "isReturned"]