from django.db import models
from app_accounts.models import CustomerModel
from app_base.models import BaseModel
import random


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
    def get_answers(self):
        answers = list(AnswersModel.objects.filter(question = self))
        random.shuffle(answers)
        ans_list = []
        for ans in answers:
            ans_list.append({
                "id" : ans.id,
                "user" : ans.user,
                "img" : ans.img.url,
                "option" : ans.answer
            })
        return ans_list
    def __str__(self):
        return self.title
    


class AnswersModel(BaseModel):
    user = models.ForeignKey(CustomerModel, related_name="user_answer", on_delete=models.CASCADE)
    answer = models.TextField()
    img = models.ImageField(upload_to="Answers", null=True, blank=True)
    votes = models.IntegerField(default=0, null=True, blank=True)
    question = models.ForeignKey(QuestionModel, related_name="question", on_delete=models.CASCADE)


class ImageModel(BaseModel):
    img = models.ImageField(upload_to="book_img")


class BookModel(BaseModel):
    current_owner = models.ForeignKey(CustomerModel, related_name="book_owner", on_delete=models.CASCADE)
    imgs = models.ForeignKey(ImageModel, related_name="book_imgs", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    category = models.ForeignKey(CategoryModel, related_name="book_category", on_delete=models.CASCADE)
    desc = models.TextField()
    value = models.IntegerField(default=30)
    def __str__(self):
        return self.title
    