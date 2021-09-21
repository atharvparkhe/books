from django.contrib import admin
from .models import *

admin.site.register(CategoryModel)


class AnswerModelAdmin(admin.StackedInline):
    model = AnswersModel

class QuestionModelAdmin(admin.ModelAdmin):
    inlines = [ AnswerModelAdmin ]

admin.site.register(QuestionModel, QuestionModelAdmin)


class BookModelAdmin(admin.ModelAdmin):
    list_display = ["title", "current_owner", "value"]

admin.site.register(BookModel, BookModelAdmin)


class TransactionsModelAdmin(admin.ModelAdmin):
    list_display = ["seller", "buyer", "book"]

admin.site.register(TransactionsModel, TransactionsModelAdmin)