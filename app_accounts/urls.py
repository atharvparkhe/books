from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('api/signup/', views.signUp, name="signup"),
	path('api/verify/', views.verify, name="verify"),
	path('api/login/', views.logIn, name="login"),
	path('api/forgot/', views.forgot, name="forgot"),
	path('api/reset/', views.reset, name="reset"),
]