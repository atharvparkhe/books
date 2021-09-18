from django.db import models
from app_base.models import *


class CustomerModel(BaseUser):
    points = models.IntegerField(default=100)
    def __str__(self):
        return self.email