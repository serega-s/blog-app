# Generated by Django 3.2.6 on 2021-08-15 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_blogmodel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogmodel',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
