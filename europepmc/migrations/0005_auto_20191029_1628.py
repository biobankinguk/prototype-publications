# Generated by Django 2.2.6 on 2019-10-29 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europepmc', '0004_auto_20191029_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='pid',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='source',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]