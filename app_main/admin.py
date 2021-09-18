from django.contrib import admin
from .models import *

admin.site.register(AnswersModel)
admin.site.register(QuestionModel)
admin.site.register(CategoryModel)