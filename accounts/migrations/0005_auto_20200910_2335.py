# Generated by Django 3.0.8 on 2020-09-10 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_shelter_limit_of_volunteer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shelter',
            old_name='image',
            new_name='thumbnail',
        ),
    ]
