# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from account.models import UserCustom as user

class BoardConsult(models.Model):
    board_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=75)
    contents = models.TextField()
    creationdate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(user, models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'board_consult'


class CommentsConsult(models.Model):
    comment_id = models.AutoField(primary_key=True)
    contents = models.TextField()
    creationdate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(user, models.SET_NULL, blank=True, null=True)
    board = models.ForeignKey(BoardConsult, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'comments_consult'
