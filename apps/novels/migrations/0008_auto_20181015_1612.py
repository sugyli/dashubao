# Generated by Django 2.1 on 2018-10-15 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0007_auto_20181015_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='chaptercontent',
            name='ishide',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否隐藏'),
        ),
        migrations.AddField(
            model_name='novelcontent',
            name='feiqi',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否废弃'),
        ),
        migrations.RemoveField(
            model_name='novelcontent',
            name='ishide',
        ),
        migrations.AlterIndexTogether(
            name='novelcontent',
            index_together={('feiqi',)},
        ),
    ]