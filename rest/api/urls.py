# from base.views import users , updateUser, getBooks
from base.views import BookAPI , StudentAPI
from django.urls import path , include

urlpatterns = [
    # path('',users),
    path('',StudentAPI.as_view()),
    path('update/<int:id>',StudentAPI.as_view()),
    path('book',BookAPI.as_view())
]
