# Generated by Django 2.2 on 2020-04-11 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0008_auto_20200408_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='insta_handle',
            name='code',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='email_handle',
            name='password',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='facebook_handle',
            name='password',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='insta_handle',
            name='password',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
