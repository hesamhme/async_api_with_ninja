# Generated by Django 5.2 on 2025-04-15 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ninjaapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('count', models.PositiveIntegerField()),
                ('status', models.CharField(default='registered', max_length=20)),
                ('result_message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
