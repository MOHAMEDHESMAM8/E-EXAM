# Generated by Django 4.0.4 on 2022-05-14 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_group_level'),
        ('question_bank', '0002_question_professor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.professor'),
        ),
    ]