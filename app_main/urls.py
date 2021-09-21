from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('api/category/', views.category, name="category"),
    path('api/question/', views.Question.as_view(), name="question"),
    path('api/answer/', views.Answer.as_view(), name="answer"),
    path('api/book/', views.Book.as_view(), name="book"),
    path('api/gift/', views.gift_points, name="gift"),
    path('api/request/', views.request_points, name="request"),
    path('api/buy/', views.buy, name="buy"),
    path('api/sell/', views.sell, name="sell"),
]