from django.shortcuts import render
from base.models import Student, Book , Category
from base.serializers import serializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response


class StudentAPI(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # to get the params from the url, we need to name the param into get function as a string
        paramId = request.GET.get('id')
        data=''
        if paramId:
            try:
                # student = User.objects.get(name = paramData)
                student = User.objects.get(id = paramId)
                data = serializer.StudentSerializer(student).data
            except:
                return Response({"msg":"No Student found with id: "+str(paramId)})

        else:
            allStudent = User.objects.all()
            data=serializer.StudentSerializer(allStudent, many=True).data
        
        
        print("---------")
        print('Param :',paramId)
        print("---------")
        return Response({"data": data})
    
    #user register
    def post(self,request):
        pass
    
    def patch(self,request, id):
        try:
            student = User.objects.get(id = id)
        except:
            return Response({"msg":"No Student found with id: "+str(id)})
     
        ser = serializer.StudentSerializer(student, data = request.data, partial = True)
        if not ser.is_valid():
            return Response({"error":ser.errors})
        
        ser.save()
        return Response({"Student updated":ser.data})
    
    def put(self,request):
        pass
    
    def delete(self,request, id):
        try:
            student = User.objects.get(id = id)
        except:
            return Response({"msg":"No Student found with id: "+str(id)})
            
        stud=serializer.StudentSerializer(student).data

        student.delete()
        return Response({"msg":"Deleted","student":stud})   
        
        
class BookAPI(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            if 'my-books' in request.path:
                user = request.user
                books = Book.objects.filter(owner=user.id)
            elif request.GET.get('id'):
                paramId = request.GET.get('id')
                book = Book.objects.get(id = paramId)
                ser = serializer.BookFullDetailSerializer(book)
                
                return Response({"books": ser.data}, status=200)
            elif request.GET.get('section'):
                sectionId = request.GET.get('section')
                FilteredCategory = Category.objects.get(id = sectionId)
                books = Book.objects.filter(category = FilteredCategory)  
                ser = serializer.BookFullDetailSerializer(books, many=True)
                return Response({"books": ser.data}, status=200)               
            else:
                books = Book.objects.all()
                
            ser = serializer.BookFullDetailSerializer(books, many=True)
            return Response({"books": ser.data}, status=200)
        except Exception as e:
            return Response({'msg': 'Failed to fetch books', "error": str(e)}, status=500)
    
    def patch(self, request,id):
        try:
            book = Book.objects.get(id = id)
        except:
            return Response({"msg":"No book found with id: "+str(id)})
        
        book_detail = serializer.BookSerializer(book)
        if book_detail.data['owner']['id'] != request.user.id :
            return Response({"msg":"You do not have access to modify this Book: "+str(book_detail.data['title'])},status=401)
     
        ser = serializer.BookSerializer(book, data = request.data, partial = True)
        if not ser.is_valid():
            return Response({"error":ser.errors})
        
        ser.save()
        return Response({"book updated":ser.data})
    
    def post(self, request):
        loggedin_User = request.user
        payload = request.data
        payload["owner"]["id"] = loggedin_User.id
        try:
            ser = serializer.BookSerializer(data=payload,context={'request': request})
            if not ser.is_valid():
                return Response({"msg":"Something went wrong","error":ser.errors})
                
            ser.save()
            return Response({"Book added":ser.data}, status=201)
        except Exception as e:
            return Response({"msg":"Something went wrong","error":str(e)})
    
    def put(self, request):
        pass
    
    def delete(self, request,id):
        try:
            book = Book.objects.get(id = id)
        except Exception as e:
            return Response({"message":"Something went wrong", "error": str(e)})

            
        ser = serializer.BookSerializer(book)
        if ser.data['owner']['id'] != request.user.id :
            return Response({"msg":"You do not have access to modify this Book: "+str(ser.data['title'])},status=401)
            
        else: 
            book.delete()
            
        return Response({"msg":"Book deleted: ", "Book":ser.data},status=200)
    
class AuthAPI(APIView):
    def get(self, request):
        pass
    
    def post(self, request):
        if 'login' in request.path:
            username = request.data.get('username')
            password = request.data.get('password')
            
            if not username or not password:
                return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(username=username, password=password)
            if user is not None:
                new_token = RefreshToken.for_user(user)
                return Response({
                    "message": "User Logged in",
                    "AccessToken": str(new_token.access_token),
                    "RefreshToken": str(new_token)
                },status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        elif 'register' in request.path:
            payload = request.data
            serial = serializer.UserSerializer(data=payload)
            if not serial.is_valid():
                return Response({"message":"Something went wrong", "error": serial.errors},status=status.HTTP_400_BAD_REQUEST)
            
            serial.save()
            
            user = User.objects.get(username = request.data['username'] )
            new_token = RefreshToken.for_user(user)
            print('Request Data :',payload)
            return Response({"message": "User created","AccessToken":str(new_token.access_token),"data":payload})
        
        elif 'logout' in request.path:
            try:
                refresh_token = request.data["refresh"]
                print(refresh_token)
                RefreshToken(refresh_token)
                return Response({"message": "Successfully logged out."}, status=200)
            except Exception as e:
                return Response({"message": "Logout failed.", "error": str(e)}, status=400)