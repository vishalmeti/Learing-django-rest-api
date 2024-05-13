from base.views import hello_world
from django.urls import path , include

urlpatterns = [
    path('v1/',hello_world),
]
