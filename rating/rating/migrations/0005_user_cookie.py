# Generated by Django 3.0.3 on 2020-03-23 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0004_auto_20200322_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cookie',
            field=models.CharField(default='', max_length=512),
        ),
    ]
