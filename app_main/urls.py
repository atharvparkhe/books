from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('api/category/', views.category, name="category"),
    path('api/question/', views.Question.as_view(), name="question"),
]