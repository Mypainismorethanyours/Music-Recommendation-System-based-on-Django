# Generated by Django 3.2.8 on 2022-11-11 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255, verbose_name='')),
                ('singer', models.CharField(default='', max_length=255, verbose_name='歌手')),
                ('pid', models.CharField(default='', max_length=10)),
                ('remark', models.CharField(default='', max_length=255)),
                ('style', models.CharField(default='', max_length=255)),
                ('url', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'music',
            },
        ),
    ]
