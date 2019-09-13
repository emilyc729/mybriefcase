# Generated by Django 2.2.3 on 2019-09-13 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='portfolio_photo',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_photo',
        ),
        migrations.AddField(
            model_name='photo',
            name='portfolio_photo',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.Portfolio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='project_photo',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.Project'),
            preserve_default=False,
        ),
    ]