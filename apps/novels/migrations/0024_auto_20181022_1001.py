# Generated by Django 2.1 on 2018-10-22 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0023_auto_20181022_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapternewcontent',
            name='isdel',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='chapternewcontenteight',
            name='isdel',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='chapternewcontentfive',
            name='isdel',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='chapternewcontentfour',
            name='isdel',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='chapternewcontentnine',
            name='isdel',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='chapternewcontentone',
            name='isdel',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='chapternewcontentseven',
            name='isdel',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='chapternewcontentsix',
            name='isdel',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='chapternewcontentthree',
            name='isdel',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='chapternewcontenttwo',
            name='isdel',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='是否删除'),
        ),
        migrations.AlterIndexTogether(
            name='chapternewcontent',
            index_together={('isdel',)},
        ),
        migrations.AlterIndexTogether(
            name='chapternewcontenteight',
            index_together={('isdel',)},
        ),
        migrations.AlterIndexTogether(
            name='chapternewcontentfive',
            index_together={('isdel',)},
        ),
        migrations.AlterIndexTogether(
            name='chapternewcontentfour',
            index_together={('isdel',)},
        ),
        migrations.AlterIndexTogether(
            name='chapternewcontentnine',
            index_together={('isdel',)},
        ),
        migrations.AlterIndexTogether(
            name='chapternewcontentone',
            index_together={('isdel',)},
        ),
        migrations.AlterIndexTogether(
            name='chapternewcontentseven',
            index_together={('isdel',)},
        ),
        migrations.AlterIndexTogether(
            name='chapternewcontentsix',
            index_together={('isdel',)},
        ),
        migrations.AlterIndexTogether(
            name='chapternewcontentthree',
            index_together={('isdel',)},
        ),
        migrations.AlterIndexTogether(
            name='chapternewcontenttwo',
            index_together={('isdel',)},
        ),
    ]
