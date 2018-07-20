# Generated by Django 2.0.7 on 2018-07-20 19:04

import django.contrib.postgres.fields
from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_experiment_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guidedesign',
            name='hdr_seq',
        ),
        migrations.AddField(
            model_name='guidedesign',
            name='tag_in',
            field=models.CharField(blank=True, choices=[('FLAG', 'FLAG'), ('3XFLAG', '3XFLAG'), ('V5', 'V5'), ('HA', 'HA'), ('MYC', 'MYC'), ('TODO', 'TODO: tag used by Manu group')], default='FLAG', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='targets',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=65536, validators=[main.validators.validate_chr_or_seq_or_enst]), default=['ENST00000330949'], help_text='Chr location or seq or ENST, one per line', size=None),
        ),
    ]
