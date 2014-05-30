# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mgr', '0002_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='home_page',
            field=models.URLField(default=b'http://www.ftj.agh.edu.pl/'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(null=True, upload_to=b'attachments', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='department',
            name='shortcut',
            field=models.CharField(default=b'WFIIS', max_length=10),
            preserve_default=True,
        ),
    ]
