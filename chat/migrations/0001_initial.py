from django.conf import settings
from django.db import migrations, models

import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies=[]

    operations = [
        migrations.CreateModel(
            name = 'Response',
            fields ={
                ('inp',models.CharField(max_length=1024)),

            },
            options ={
                'abstract': False,
            }
        ),
    ]