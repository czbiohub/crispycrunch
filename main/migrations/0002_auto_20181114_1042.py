# Generated by Django 2.1.1 on 2018-11-14 18:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidedesign',
            name='guides_per_target',
            field=models.IntegerField(default=60, help_text='The top N number of guides per target to select', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(96)]),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='hdr_tag',
            field=models.CharField(blank=True, choices=[('start_codon', 'Within 36bp after start codon (N-terminus)'), ('stop_codon', 'Within 36bp before or after stop codon (C-terminus)'), ('per_target', 'As specified per target ("N" or "C")')], default='per_target', help_text='Insert a sequence by HDR (Homology Directed Repair). Requires ENST transcript IDs.', max_length=40, verbose_name='Insert tag by HDR'),
        ),
    ]
