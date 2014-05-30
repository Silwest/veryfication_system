# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(default=b'Put your answer here!', max_length=50)),
                ('correct', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Wydzial Fizyki i Informatyki Stosowanej', max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldOfStudy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Informatyka Stosowana', max_length=30)),
            ],
            options={
                'verbose_name_plural': b'Field of studies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldOfQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Dziedzina pytania', max_length=40)),
                ('field_of_study', models.ForeignKey(to='mgr.FieldOfStudy', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
