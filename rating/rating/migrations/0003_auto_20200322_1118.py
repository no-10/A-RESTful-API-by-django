# Generated by Django 3.0.3 on 2020-03-22 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0002_auto_20200322_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='nameId',
            field=models.CharField(max_length=20),
        ),
    ]