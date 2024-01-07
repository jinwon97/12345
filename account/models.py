from django.db import models
from django.contrib.auth.models import AbstractUser

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=75)
    password = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'admin'

class UserCustom(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=75)
    name = models.CharField(max_length = 25,  default = "dave the QA tester")
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=254)
    phonenumber = models.CharField(max_length=11)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length = 1)

    # class Meta:
    #     managed = False
    #     db_table = 'user'
    
    # groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    # user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

class LogInfo(models.Model):
    user = models.OneToOneField(UserCustom, on_delete=models.CASCADE, primary_key=True)
    isLogedIn = models.BooleanField(default=False)
    logtime = models.DateTimeField(auto_now=True)
    isadmin = models.BooleanField(default = False)