# Generated by Django 4.2.2 on 2023-06-25 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('book_description', models.CharField(max_length=5000)),
            ],
        ),
    ]
