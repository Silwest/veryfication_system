# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mgr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_of_question', models.ForeignKey(to='mgr.FieldOfQuestion', to_field='id')),
                ('value', models.CharField(default=b'Put you question here!', max_length=200)),
                ('answer_1', models.ForeignKey(to='mgr.Answer', to_field='id')),
                ('answer_2', models.ForeignKey(to='mgr.Answer', to_field='id')),
                ('answer_3', models.ForeignKey(to='mgr.Answer', to_field='id')),
                ('answer_4', models.ForeignKey(to='mgr.Answer', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
