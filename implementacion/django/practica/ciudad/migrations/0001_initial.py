# Generated by Django 2.2.1 on 2019-05-07 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calle',
            fields=[
                ('nombre', models.CharField(max_length=200)),
                ('id', models.DecimalField(decimal_places=0, default=0, max_digits=15, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Hora',
            fields=[
                ('hora', models.DecimalField(decimal_places=0, default=0, max_digits=8, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ModeloCalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idcalle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ciudad.Calle')),
                ('idmodelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ciudad.Modelo')),
            ],
            options={
                'unique_together': {('idcalle', 'idmodelo')},
            },
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.DecimalField(decimal_places=0, default=0, max_digits=12, primary_key=True, serialize=False)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('precioPorHora', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ParkingModelo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idmodelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ciudad.Modelo')),
                ('idparking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ciudad.Parking')),
            ],
            options={
                'unique_together': {('idparking', 'idmodelo')},
            },
        ),
        migrations.CreateModel(
            name='Trafico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('congestion', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('hora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ciudad.Hora')),
                ('idModeloCalle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identificadorcalle', to='ciudad.ModeloCalle')),
            ],
            options={
                'unique_together': {('idModeloCalle', 'hora')},
            },
        ),
        migrations.CreateModel(
            name='Disponible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estaLibre', models.BooleanField()),
                ('hora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ciudad.Hora')),
                ('idParkingModelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identificadorparking', to='ciudad.ParkingModelo')),
            ],
            options={
                'unique_together': {('idParkingModelo', 'hora')},
            },
        ),
    ]
