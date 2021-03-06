# Generated by Django 2.1 on 2018-10-08 03:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('novels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NovelFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapterid', models.CharField(default=0, max_length=50, verbose_name='章节ID')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '用户收藏',
                'verbose_name_plural': '用户收藏',
            },
        ),
        migrations.CreateModel(
            name='UserZan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=datetime.date.today, verbose_name='添加时间')),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novels.NovelDetail', to_field='url_md5', verbose_name='小说')),
            ],
            options={
                'verbose_name': '用户点赞',
                'verbose_name_plural': '用户点赞',
            },
        ),
    ]
