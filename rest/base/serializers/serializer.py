
from base.models import Student, Book , Category
from rest_framework import serializers
from django.contrib.auth.models import User

from drf_writable_nested import WritableNestedModelSerializer


class StudentContactDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'password', 'email']
class UserId(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
        
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def validate(self, data):
        if any(char.isdigit() for char in data['username']):
            raise serializers.ValidationError({'error':'Name should not contain numbers'})
        
        return data
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'
class CategoryId(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ['id']
        

class BookSerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    
#WritableNestedModelSerializer -> this needs to be added . as there is nesting of FK. create wont work directly.
# so we have to pip install this and add it here.

# ------------------ STACK OVERFLOW SOLUTION ---------------------------

# I had a similar problem but with the update() method ...

# The solution was simple thanks to this thread: https://github.com/beda-software/drf-writable-nested/issues/104...

# All I had to do was installing the library pip install drf-writable-nested and import it:

# from drf_writable_nested import WritableNestedModelSerializer 

# the code should look like this:

# (credit to: https://github.com/Leonardoperrella)

# --serializers.py--

# from drf_writable_nested import WritableNestedModelSerializer

# class ProductsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Products
#         fields = ('name', 'code', 'price')

# class VendorsSerializer(WritableNestedModelSerializer,
#                         serializers.ModelSerializer):
#     products = ProductsSerializer(source='vendor', many=True)
#     class Meta:
#         model = Vendors
#         fields = ('name', 'cnpj', 'city', 'products')


# -----------------------------------------------------------------------


    category = CategoryId()
    owner = UserId()
    class Meta:
        model = Book 
        fields = ['id', 'category', 'owner', 'title', 'description']
    
    def create(self, validated_data):
        print("context",self.context)
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class BookFullDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    owner = StudentContactDetail()
    class Meta:
        model = Book 
        fields = ['id', 'category', 'owner', 'title', 'description']
    
