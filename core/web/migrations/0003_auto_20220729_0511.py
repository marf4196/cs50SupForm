# Generated by Django 3.2.14 on 2022-07-29 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20220729_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='students',
            name='phone',
            field=models.BigIntegerField(),
        ),
    ]
