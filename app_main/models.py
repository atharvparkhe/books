from django.db import models
from app_accounts.models import CustomerModel
from app_base.models import BaseModel


class CategoryModel(BaseModel):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class QuestionModel(BaseModel):
    user = models.ForeignKey(CustomerModel, related_name="user_question", on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    desc = models.TextField()
    img = models.ImageField(upload_to="Questions", null=True, blank=True)
    votes = models.IntegerField(default=0, null=True, blank=True)
    category = models.ForeignKey(CategoryModel, related_name="category", on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class AnswersModel(BaseModel):
    user = models.ForeignKey(CustomerModel, related_name="user_answer", on_delete=models.CASCADE)
    answer = models.TextField()
    img = models.ImageField(upload_to="Answers", null=True, blank=True)
    votes = models.IntegerField(default=0, null=True, blank=True)
    question = models.ForeignKey(QuestionModel, related_name="question", on_delete=models.CASCADE)

    def __str__(self):
        return self.answer






class BookModel(BaseModel):
    current_owner = models.ForeignKey(CustomerModel, related_name="book_owner", on_delete=models.CASCADE)
    imgs =  models.ImageField(upload_to="book_img", null=True, blank=True)
    title = models.CharField(max_length=50)

    desc = models.TextField()
    credit = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title


class BookPurchasedModel(BaseModel):
    book = models.ForeignKey(BookModel, related_name="book_purchased", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomerModel, related_name="book_purchased_user", on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title


