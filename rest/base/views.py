from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET','POST'])
def hello_world(request):
    if request.method == 'GET':
        return Response({"message": "You hit GET method: Hello, world!"})
    elif request.method == 'POST':
        data = request.data
        print("-----------")
        print(data)
        print("-----------")
        return Response({"message": "You hit POST method: Hello, world!",
                         "data":data})