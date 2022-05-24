# Generated by Django 3.1.12 on 2022-05-18 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, 
                serialize=False, verbose_name='ID')),
                ('gmail_account', models.TextField(default='', null=True)),
                ('gmail_passwd', models.TextField(default='', null=True)),
                ('json_data_base', models.TextField(default='', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
