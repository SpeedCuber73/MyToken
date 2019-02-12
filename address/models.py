from django.db import models
from django.contrib.auth.models import User


class AddressBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    house_num = models.IntegerField()
