# Generated by Django 3.1.6 on 2021-04-04 14:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0016_GlobalComments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='code',
            field=models.CharField(help_text='Code from Edison like C/01, P/01 or custom identification like Komb', max_length=20),
        ),
        migrations.AlterField(
            model_name='class',
            name='day',
            field=models.CharField(choices=[('PO', 'Monday'), ('UT', 'Tuesday'), ('ST', 'Wednesday'), ('CT', 'Thursday'), ('PA', 'Friday'), ('SO', 'Saturday'), ('NE', 'Sunday')], max_length=5),
        ),
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(blank=True, help_text='Students can be imported in bulk from the index page', related_name='students', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='code',
            field=models.CharField(max_length=255, unique=True, verbose_name='Directory'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='submit',
            name='jobid',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
