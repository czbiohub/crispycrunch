# Generated by Django 2.0.7 on 2018-07-16 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20180715_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guideplatelayout',
            name='name',
        ),
        migrations.RemoveField(
            model_name='primerplatelayout',
            name='name',
        ),
        migrations.AlterField(
            model_name='primerplatelayout',
            name='group_by',
            field=models.CharField(choices=[('cell_type', 'Cell Type'), ('random', 'Random'), ('todo', 'TODO: more plate groupings')], default='cell_type', max_length=40),
        ),
        migrations.AlterField(
            model_name='primerplatelayout',
            name='order_by',
            field=models.CharField(choices=[('alphabetical', 'Alphabetical'), ('todo', 'TODO: more plate orderings')], default='alphabetical', max_length=40),
        ),
    ]
