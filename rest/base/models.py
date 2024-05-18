# myapp/models.py

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(default=18)
    
    class Meta:
        db_table = 'Person'
        
    def __str__(self):
        return self.name
