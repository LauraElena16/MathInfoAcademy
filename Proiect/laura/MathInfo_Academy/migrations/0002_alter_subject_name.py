# Generated by Django 4.2.13 on 2024-05-30 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MathInfo_Academy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
