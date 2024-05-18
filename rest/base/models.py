# myapp/models.py

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(default=18)
    
    class Meta:
        db_table = 'Person'
        
    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name
    
class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title