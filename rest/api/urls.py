from base.views import users , updateUser, getBooks
from django.urls import path , include

urlpatterns = [
    path('',users),
    path('update/<int:id>',updateUser),
    path('book',getBooks)
]
