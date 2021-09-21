from django.urls import path
from .views import *

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'BookViewAdmin', BookAdminViewSet)
router.register(r'QuestionUpload', UploadQuestion)


urlpatterns = [
  
 path('buybook/',BookBuy.as_view(),name='buybook'),
    path('booklist/',AllBooksView.as_view(),name='booklist'),
    path('allquestionview/',QusetionView.as_view(),name='allquestionview'),
    path('answersview/',AnswerView.as_view(),name='answersview'),
    path('purchasedbook/',BookPurchasedView.as_view(),name='purchasedbook'),
    path('getCategory/',GetCategory.as_view(),name='getCategory'),
    path('answerupload/',AnswerUpload.as_view(),name='answerupload'),
    path('viewProfile/',ViewProfile.as_view(),name='viewProfile'),
]
urlpatterns += router.urls