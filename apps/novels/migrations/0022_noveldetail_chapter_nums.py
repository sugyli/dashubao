# Generated by Django 2.1 on 2018-10-20 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0021_auto_20181019_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='noveldetail',
            name='chapter_nums',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='章节数'),
        ),
    ]