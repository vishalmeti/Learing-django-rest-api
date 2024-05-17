from django.shortcuts import render
from base.models import Person
from base.serializers import serializer

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET','POST'])
def hello_world(request):
    if request.method == 'GET':
        # to get the params from the url, we need to name the param into get function as a string
        paramData = request.GET.get('name')
        allPerson = Person.objects.all()
        data=serializer.PersonSerializer(allPerson, many=True).data
        
        
        print("---------")
        print('Param :',paramData)
        print("---------")
        return Response({"message": "You hit GET method: Hello, world!", "data": data})
    elif request.method == 'POST':
        payload = request.data
        serial = serializer.PersonSerializer(data=payload)
        if not serial.is_valid():
            return Response({"message":"Something went wrong", "error": serial.errors})
        
        serial.save()
        print("-----------")
        print('Request Data :',payload)
        print("-----------")
        return Response({"message": "You hit POST method: Hello, world!",
                         "data":payload})