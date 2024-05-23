
from base.models import Student, Book , Category
from rest_framework import serializers

class StudentContactDetail(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name','email','contact']
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    
    def validate(self, data):
        if any(char.isdigit() for char in data['name']):
            raise serializers.ValidationError({'error':'Name should not contain numbers'})
        
        return data
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'
class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    owner = StudentContactDetail()
    class Meta:
        model = Book 
        fields = '__all__'
        # depth = 1
