# Generated by Django 3.2.6 on 2021-08-15 07:59

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='content',
            field=froala_editor.fields.FroalaField(),
        ),
    ]
