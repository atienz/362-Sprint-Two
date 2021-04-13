from django.db import models


# Create your models here.
class MyModel(models.Model):
    id = models.AutoField(null=False, primary_key=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    middle_name = models.CharField(max_length=255)
    age = models.IntegerField(null=False)
    current_status = models.CharField(max_length=100, null=False, default='new')


# User List


# UI List