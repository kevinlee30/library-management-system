from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    pubYear = models.PositiveSmallIntegerField()
    imgUrl = models.CharField('image URL', max_length=200)
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    category = models.CharField(max_length=200)
    desc = models.TextField()
    borrowed = models.IntegerField(default=0, help_text='Number of times book is borrowed')
    
    class Meta:
        ordering = ['-pubYear']
        
    def __str__(self):
        return f'{self.title} ({self.author})'
    
class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['username']
            
    def __str__(self):
        return f'{self.username}'
        
class Borrowing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', to_field='id', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('User', to_field='username', on_delete=models.SET_NULL, null=True)
    startDate = models.DateField()
    endDate = models.DateField()
    isReturned = models.BooleanField(default=False)
    class Meta:
        ordering = ['endDate']
            
    def __str__(self):
        return f'{self.book.title} ({self.user.username})'
    
class Highlight(models.Model):
    title = models.CharField('Highlight Title', max_length=200)
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    imgUrl = imgUrl = models.CharField('Image URL', max_length=200)
    
    def __str__(self):
        return f'{self.book.title}: {self.title}'
    