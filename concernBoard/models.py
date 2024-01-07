# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=75)
    password = models.CharField(max_length=75)
    email = models.CharField(max_length=254)
    phonenumber = models.CharField(max_length=11)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'user'


class BoardConcern(models.Model):
    board_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=75)
    contents = models.TextField()
    creationdate = models.DateTimeField()
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'board_concern'


class CommentsConcern(models.Model):
    comment_id = models.AutoField(primary_key=True)
    contents = models.TextField()
    creationdate = models.DateTimeField()
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    board = models.ForeignKey(BoardConcern, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'comments_concern'
