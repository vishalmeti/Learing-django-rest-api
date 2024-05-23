# from base.views import users , updateUser, getBooks
from base.views import getBooks , StudentAPI
from django.urls import path , include

urlpatterns = [
    # path('',users),
    path('',StudentAPI.as_view()),
    path('update/<int:id>',StudentAPI.as_view()),
    path('book',getBooks)
]
