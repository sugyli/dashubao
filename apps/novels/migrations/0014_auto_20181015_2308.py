# Generated by Django 2.1 on 2018-10-15 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0013_auto_20181015_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='novelchapter',
            name='fenbiao',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='使用分表的内容'),
        ),
        migrations.AlterIndexTogether(
            name='novelchapter',
            index_together={('update_time',), ('chapter_type',), ('create_time',), ('chapter_old_id',), ('chapter_order',), ('ishide',), ('fenbiao',)},
        ),
        migrations.RemoveField(
            model_name='noveldetail',
            name='fenbiao',
        ),
        migrations.AlterIndexTogether(
            name='noveldetail',
            index_together={('update_time',), ('stop_update',), ('create_time',), ('have_chapter',), ('novel_old_id',), ('ishide',), ('iswenziname',)},
        ),
    ]
