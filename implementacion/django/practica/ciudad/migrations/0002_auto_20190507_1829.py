# Generated by Django 2.2.1 on 2019-05-07 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafico',
            name='congestion',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=8),
        ),
    ]
