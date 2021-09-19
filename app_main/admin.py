from django.contrib import admin
from .models import *

admin.site.register(CategoryModel)

class AnswerModelAdmin(admin.StackedInline):
    model = AnswersModel

class QuestionModelAdmin(admin.ModelAdmin):
    inlines = [ AnswerModelAdmin ]

admin.site.register(QuestionModel, QuestionModelAdmin)

class BookModelAdmin(admin.ModelAdmin):
    list_display = ["current_owner", "title", "value"]

admin.site.register(BookModel, BookModelAdmin)