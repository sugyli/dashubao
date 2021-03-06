# Generated by Django 2.1 on 2018-11-11 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0026_noveldetail_must_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='noveldetail',
            name='laoshutongbu',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='老书同步'),
        ),
        migrations.AlterField(
            model_name='novelchapter',
            name='fenbiao',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='内容分表'),
        ),
        migrations.AlterField(
            model_name='noveldetail',
            name='iswenziname',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='标题文字'),
        ),
        migrations.AlterField(
            model_name='noveldetail',
            name='must_update',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='强制更新'),
        ),
        migrations.AlterField(
            model_name='noveldetail',
            name='novel_old_id',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='老书'),
        ),
        migrations.AlterField(
            model_name='noveldetail',
            name='stop_update',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='停止更新'),
        ),
        migrations.AlterIndexTogether(
            name='noveldetail',
            index_together={('iswenziname',), ('stop_update',), ('laoshutongbu',), ('update_time',), ('ishide',), ('novel_old_id',), ('have_chapter',), ('caiji_status',), ('create_time',), ('must_update',)},
        ),
    ]
