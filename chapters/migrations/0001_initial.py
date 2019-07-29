# Generated by Django 2.1.7 on 2019-07-29 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id_chapter', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('id_unity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='units.Unity')),
            ],
        ),
    ]
