# Generated by Django 3.1.3 on 2020-12-03 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('text', models.TextField()),
                ('title_img', models.TextField()),
                ('status', models.IntegerField()),
                ('add_time', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('k', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('v', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Navigator',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image_src', models.TextField()),
                ('article_id', models.IntegerField()),
                ('status', models.IntegerField()),
                ('add_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_openid', models.CharField(max_length=64)),
                ('user_nickname', models.CharField(max_length=125)),
                ('user_sex', models.IntegerField()),
                ('user_city', models.CharField(max_length=125)),
                ('user_province', models.CharField(max_length=125)),
                ('user_country', models.CharField(max_length=125)),
                ('user_headimgurl', models.TextField()),
                ('add_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_openid', models.CharField(max_length=64)),
                ('collect_time', models.DateField()),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='oreo.article')),
            ],
        ),
    ]
