# Generated by Django 3.0.8 on 2020-09-03 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uservolunteer',
            options={'ordering': ['-applied_at']},
        ),
        migrations.AddField(
            model_name='uservolunteer',
            name='applied_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
