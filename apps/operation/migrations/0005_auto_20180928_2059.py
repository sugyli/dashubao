# Generated by Django 2.1 on 2018-09-28 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_auto_20180927_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novelfavorite',
            name='chapterid',
            field=models.CharField(default=0, max_length=50, verbose_name='章节ID'),
        ),
    ]
