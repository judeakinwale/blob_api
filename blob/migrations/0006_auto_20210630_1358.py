# Generated by Django 3.2.3 on 2021-06-30 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blob', '0005_auto_20210630_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blobfile',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='blobfile',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='blobimage',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='blobimage',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
