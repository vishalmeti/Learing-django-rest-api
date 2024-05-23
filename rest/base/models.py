# myapp/models.py

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(default=18)
    contact = models.CharField(max_length=10, default=0, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=True , unique=True)
    
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
    owner = models.ForeignKey(Student, on_delete=models.CASCADE , default = 5, null=False , blank=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title