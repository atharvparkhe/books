from django.contrib import admin
from .models import *

admin.site.register(AnswersModel)
admin.site.register(QuestionModel)
admin.site.register(CategoryModel)
admin.site.register(BookModel)
admin.site.register(BookPurchasedModel)
admin.site.register(Voting)
admin.site.register(BookImage)