# Generated by Django 4.0.4 on 2022-05-05 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_groupstudents_options_and_more'),
        ('question_bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.professor'),
        ),
    ]