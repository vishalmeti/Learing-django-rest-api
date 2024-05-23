# from base.views import users , updateUser, getBooks
from base.views import BookAPI , StudentAPI , AuthAPI
from django.urls import path , include

urlpatterns = [
    # path('',users),
    path('',StudentAPI.as_view()),
    path('login/',AuthAPI.as_view()),
    path('register/',AuthAPI.as_view()),
    path('logout/',AuthAPI.as_view()),
    path('update/<int:id>',StudentAPI.as_view()),
    
    path('all-books/',BookAPI.as_view()),
    path('add-books/',BookAPI.as_view()),
    path('book/',BookAPI.as_view()),
    path('my-books/',BookAPI.as_view())
]
