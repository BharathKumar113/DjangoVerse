from django.db import models
class Sample(models.Model):
    name=models.CharField(max_length=200)
    age=models.IntegerField()
    hobbies=models.CharField(max_length=200)