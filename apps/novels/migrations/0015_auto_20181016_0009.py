# Generated by Django 2.1 on 2018-10-16 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0014_auto_20181015_2308'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='noveldetail',
            index_together={('have_chapter',), ('novel_old_id',), ('iswenziname',)},
        ),
    ]
