from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    publisher = models.CharField(max_length=200)
    pubYear = models.PositiveSmallIntegerField()
    imgUrl = models.CharField('image URL', max_length=200)
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-pubYear']
        
    def __str__(self):
        return f'{self.title} ({self.author.name})'
        
class Author(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
    
class Category(models.Model):
    category = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['category']

    def __str__(self):
        return f'{self.category}'
    
