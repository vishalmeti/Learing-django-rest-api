# myapp/models.py

from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(default=18)
    
    def __str__(self):
        return self.name
