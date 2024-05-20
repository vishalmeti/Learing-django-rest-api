from django.shortcuts import render
from base.models import Student, Book
from base.serializers import serializer

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET','POST'])
def users(request):
    if request.method == 'GET':
        # to get the params from the url, we need to name the param into get function as a string
        paramData = request.GET.get('name')
        paramId = request.GET.get('id')
        data=''
        if paramData or paramId:
            try:
                # student = Student.objects.get(name = paramData)
                student = Student.objects.get(id = paramId)
                data = serializer.StudentSerializer(student).data
            except:
                return Response({"msg":"No Student found with id: "+str(paramId)})

        else:
            allStudent = Student.objects.all()
            data=serializer.StudentSerializer(allStudent, many=True).data
        
        
        print("---------")
        print('Param :',paramData)
        print("---------")
        return Response({"data": data})
    elif request.method == 'POST':
        payload = request.data
        serial = serializer.StudentSerializer(data=payload)
        if not serial.is_valid():
            return Response({"message":"Something went wrong", "error": serial.errors})
        
        serial.save()
        print("-----------")
        print('Request Data :',payload)
        print("-----------")
        return Response({"message": "Data added","data":payload})
    
@api_view(['PATCH','DELETE'])
def updateUser(request, id):
    print(request.data)
    try:
        student = Student.objects.get(id = id)
    except:
        return Response({"msg":"No Student found with id: "+str(id)})
     
    if request.method == 'PATCH':   
        ser = serializer.StudentSerializer(student, data = request.data, partial = True)
        if not ser.is_valid():
            return Response({"error":ser.errors})
        
        ser.save()
        return Response({"Student updated":ser.data})
    
    elif request.method == 'DELETE':
        student.delete()
        return Response({"msg":"Deleted"})   
    

@api_view(['GET'])
def getBooks(request):
    try:
        books = Book.objects.all()
        ser = serializer.BookSerializer(books, many=True)
        return Response({"books": ser.data}, status=200)
    except Exception as e:
        return Response({'msg': 'Failed to fetch books', "error": str(e)}, status=500)