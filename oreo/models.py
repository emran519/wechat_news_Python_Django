from django.db import models

# Create your models here.
from django.db import models


class Navigator(models.Model):
    id = models.AutoField(primary_key=True)
    image_src = models.TextField()
    article_id = models.IntegerField()
    status = models.IntegerField()
    add_time = models.DateTimeField()

class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_openid = models.CharField(max_length=64)
    user_nickname = models.CharField(max_length=125)
    user_sex = models.IntegerField()
    user_city = models.CharField(max_length=125)
    user_province = models.CharField(max_length=125)
    user_country = models.CharField(max_length=125)
    user_headimgurl = models.TextField()
    add_time = models.DateTimeField()

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    text = models.TextField()
    title_img = models.TextField()
    status = models.IntegerField()
    add_time = models.DateField()


class Collect(models.Model):
    id = models.AutoField(primary_key=True)
    user_openid = models.CharField(max_length=64)
    # article_id = models.IntegerField()
    collect_time = models.DateField()
    # 设置关联
    # article = models.OneToOneField("Article", on_delete=models.DO_NOTHING)
    article = models.ForeignKey("Article", on_delete=models.DO_NOTHING, null=True)

class Config(models.Model):
    k = models.CharField(primary_key=True, max_length=200)
    v = models.TextField()