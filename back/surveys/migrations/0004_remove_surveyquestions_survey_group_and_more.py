# Generated by Django 4.0.2 on 2022-02-27 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_rename_fromuser_survey_from_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyquestions',
            name='survey_group',
        ),
        migrations.AddField(
            model_name='surveyquestions',
            name='survey_group',
            field=models.ManyToManyField(to='surveys.SurveyGroup'),
        ),
    ]