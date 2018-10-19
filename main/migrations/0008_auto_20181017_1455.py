# Generated by Django 2.1.1 on 2018-10-17 21:55

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import functools
import main.models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20181008_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidedesign',
            name='target_tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('start_codon', 'Within 36bp after start codon'), ('stop_codon', 'Within 36bp before or after stop codon')], max_length=40), blank=True, default=[], size=None),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='hdr_seq',
            field=models.CharField(blank=True, help_text='Sequence for Homology Directed Repair', max_length=160, validators=[utils.validators.validate_seq]),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='hdr_tag',
            field=models.CharField(blank=True, choices=[('start_codon', 'Within 36bp after start codon'), ('stop_codon', 'Within 36bp before or after stop codon')], help_text='Insert GFP (Green Fluorescent Protein) by HDR (Homology Directed Repair). Requires ENST transcript IDs.', max_length=40, verbose_name='Insert tag by HDR'),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='pam',
            field=models.CharField(choices=[('NGG', '20bp-NGG (SpCas9, SpCas9-HF1, eSpCas9, ...)')], default='NGG', help_text='Protospacer Adjacent Motif', max_length=80, verbose_name='PAM'),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='targets',
            field=django.contrib.postgres.fields.ArrayField(base_field=main.models.ChrLocField(blank=True, max_length=80, validators=[utils.validators.validate_chr]), size=None),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='targets_raw',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=65536, validators=[utils.validators.validate_chr_or_seq_or_enst_or_gene]), default=['ENST00000221138', 'ENST00000227618', 'ENST00000237380', 'ENST00000237530', 'ENST00000251871', 'ENST00000254950', 'ENST00000255764', 'ENST00000257287', 'ENST00000258091', 'ENST00000261819', 'ENST00000263205', 'ENST00000265350', 'ENST00000267935', 'ENST00000282892', 'ENST00000283195', 'ENST00000287598', 'ENST00000296255', 'ENST00000299300', 'ENST00000306467', 'ENST00000310955', 'ENST00000311832', 'ENST00000315368', 'ENST00000325542', 'ENST00000341068', 'ENST00000345046', 'ENST00000352035', 'ENST00000354910', 'ENST00000355801', 'ENST00000356221', 'ENST00000366542', 'ENST00000366999', 'ENST00000371485', 'ENST00000372457', 'ENST00000373842', 'ENST00000374080', 'ENST00000374206', 'ENST00000376227', 'ENST00000376300', 'ENST00000378230', 'ENST00000394128', 'ENST00000394440', 'ENST00000394886', 'ENST00000397527', 'ENST00000397786', 'ENST00000424347', 'ENST00000430055', 'ENST00000456793', 'ENST00000481195', 'ENST00000503026', 'ENST00000506447', 'ENST00000556440', 'ENST00000602624'], help_text='Chromosome location, fasta sequence, ENST transcript ID, or\n          gene name. One per line. No extra whitespace. Add ",N" or ",C" to a\n          line to indicate tagging at N or C terminus.', size=None, verbose_name='Target regions'),
        ),
        migrations.AlterField(
            model_name='guideselection',
            name='selected_guides',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Guides returned by Crispor. Filtered and ranked.', validators=[functools.partial(utils.validators.validate_num_wells, *(), **{'max': 192}), main.models.GuideSelection._validate_selected_guides]),
        ),
        migrations.AlterField(
            model_name='primerdesign',
            name='max_amplicon_length',
            field=models.IntegerField(default=400, help_text='amplicon = primer product', validators=[django.core.validators.MinValueValidator(200), django.core.validators.MaxValueValidator(400)], verbose_name='Maximum amplicon length'),
        ),
        migrations.AlterField(
            model_name='primerdesign',
            name='primer_temp',
            field=models.IntegerField(default=60, validators=[django.core.validators.MinValueValidator(58), django.core.validators.MaxValueValidator(62)], verbose_name='Primer melting temperature'),
        ),
    ]
