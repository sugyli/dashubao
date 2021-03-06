# Generated by Django 2.1 on 2018-10-15 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0011_auto_20181015_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='noveldetail',
            name='fenbiao',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='使用分表的内容'),
        ),
        migrations.AlterIndexTogether(
            name='noveldetail',
            index_together={('fenbiao',), ('novel_old_id',), ('iswenziname',), ('have_chapter',)},
        ),
    ]
