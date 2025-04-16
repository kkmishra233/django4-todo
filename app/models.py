from django.contrib.auth.models import User
from django.db import models

class Todo(models.Model):
    id =  models.BigAutoField(primary_key=True)
    task = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now_add=True)

