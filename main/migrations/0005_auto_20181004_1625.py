# Generated by Django 2.1.1 on 2018-10-04 23:25

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import functools
import main.models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180920_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guidedesign',
            name='donor_data',
        ),
        migrations.RemoveField(
            model_name='guideselection',
            name='selected_donors',
        ),
        migrations.AddField(
            model_name='guidedesign',
            name='hdr_tag',
            field=models.CharField(blank=True, choices=[('start_codon', 'Start Codon'), ('stop_codon', 'Stop Codon')], help_text='Insert GFP (Green Fluorescent Protein) by HDR (Homology Directed Repair)', max_length=40),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='experiment',
            field=models.ForeignKey(help_text='The Crispycrunch experiment to be analyzed', on_delete=django.db.models.deletion.CASCADE, to='main.Experiment'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='researcher',
            field=models.ForeignKey(help_text='The researcher doing the analysis', on_delete=django.db.models.deletion.CASCADE, to='main.Researcher'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='researcher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Researcher'),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='experiment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Experiment'),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='genome',
            field=models.CharField(choices=[('hg38', 'Homo sapiens - Human - UCSC Dec. 2013 (GRCh38/hg38)'), ('hg19', 'Homo sapiens - Human - UCSC Feb. 2009 (GRCh37/hg19)'), ('todo', 'TODO: more genomes')], default='hg38', max_length=80),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='hdr_seq',
            field=models.CharField(blank=True, help_text='Sequence for Homology Directed Repair', max_length=65536, validators=[main.validators.validate_seq]),
        ),
        migrations.AlterField(
            model_name='guidedesign',
            name='targets',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=65536, validators=[main.validators.validate_chr_or_seq_or_enst_or_gene]), help_text='Chr location, seq, ENST, or gene. One per line. For reverse strand, write chr location right-to-left.', size=None),
        ),
        migrations.AlterField(
            model_name='guideselection',
            name='guide_design',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.GuideDesign'),
        ),
        migrations.AlterField(
            model_name='guideselection',
            name='selected_guides',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Guides returned by Crispor', validators=[functools.partial(main.validators.validate_num_wells, *(), **{'max': 192}), main.models.GuideSelection._validate_selected_guides]),
        ),
        migrations.AlterField(
            model_name='primerdesign',
            name='guide_selection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.GuideSelection'),
        ),
        migrations.AlterField(
            model_name='primerdesign',
            name='max_amplicon_length',
            field=models.IntegerField(default=400, validators=[django.core.validators.MinValueValidator(150), django.core.validators.MaxValueValidator(400)]),
        ),
        migrations.AlterField(
            model_name='primerdesign',
            name='primer_temp',
            field=models.IntegerField(default=60, validators=[django.core.validators.MinValueValidator(58), django.core.validators.MaxValueValidator(62)]),
        ),
        migrations.AlterField(
            model_name='primerselection',
            name='primer_design',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.PrimerDesign'),
        ),
    ]
