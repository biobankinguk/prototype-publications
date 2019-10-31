# Generated by Django 2.2.6 on 2019-10-29 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('europepmc', '0003_publication_biobank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exact', models.CharField(max_length=256)),
                ('aid', models.CharField(max_length=256)),
                ('atype', models.CharField(max_length=256)),
                ('section', models.CharField(max_length=256)),
                ('provider', models.CharField(max_length=256)),
            ],
        ),
        migrations.AlterModelOptions(
            name='biobank',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='publication',
            options={'ordering': ['-year', 'title']},
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('uri', models.CharField(max_length=256)),
                ('annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='europepmc.Annotation')),
            ],
        ),
        migrations.AddField(
            model_name='annotation',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='europepmc.Publication'),
        ),
    ]