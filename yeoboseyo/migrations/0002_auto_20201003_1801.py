# Generated by Django 3.1.2 on 2020-10-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yeoboseyo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trigger',
            name='joplin_folder',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='trigger',
            name='localstorage',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='trigger',
            name='reddit',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
