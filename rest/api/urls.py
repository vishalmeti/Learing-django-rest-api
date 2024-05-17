from base.views import users , updateUser
from django.urls import path , include

urlpatterns = [
    path('',users),
    path('update/<int:id>',updateUser)
]
