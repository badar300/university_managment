# Generated by Django 5.0 on 2023-12-15 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject_supervision', '0006_major_std_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dissertation',
            name='title',
            field=models.CharField(default='', max_length=15),
        ),
    ]