# Generated by Django 2.0.7 on 2018-07-11 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_guideset'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuideDesign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genome', models.CharField(choices=[('homo_sapiens', 'Home sapiens - USCS (GRCh37/hg19)'), ('todo', 'TODO: more genomes')], max_length=80)),
                ('PAM', models.CharField(choices=[('Cas9', '20bp-NGG - Sp Cas9'), ('todo', 'TODO: more PAMs')], max_length=80)),
                ('targets', models.CharField(max_length=65536)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='GuidePlateLayout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('group_by', models.CharField(choices=[('cell_type', 'Cell Type'), ('random', 'Random'), ('todo', 'TODO: more plate groupings')], max_length=40)),
                ('order_by', models.CharField(choices=[('alphabetical', 'Alphabetical'), ('todo', 'TODO: more plate orderings')], max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='GuideSelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide_data', models.CharField(max_length=65536)),
                ('is_selected', models.BooleanField(default=False)),
                ('guide_design', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.GuideDesign')),
            ],
        ),
        migrations.CreateModel(
            name='PrimerDesign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=80)),
                ('melting_temp', models.IntegerField()),
                ('length', models.IntegerField()),
                ('amplicon_size', models.IntegerField()),
                ('primers_per_guide', models.IntegerField()),
                ('guide_selection', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.GuideSelection')),
            ],
        ),
        migrations.CreateModel(
            name='PrimerPlateLayout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('group_by', models.CharField(choices=[('cell_type', 'Cell Type'), ('random', 'Random'), ('todo', 'TODO: more plate groupings')], max_length=40)),
                ('order_by', models.CharField(choices=[('alphabetical', 'Alphabetical'), ('todo', 'TODO: more plate orderings')], max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='PrimerSelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primer_data', models.CharField(max_length=65536)),
                ('is_selected', models.BooleanField(default=False)),
                ('primer_design', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.PrimerDesign')),
            ],
        ),
        migrations.DeleteModel(
            name='GuideSet',
        ),
        migrations.AddField(
            model_name='primerplatelayout',
            name='primer_selection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.PrimerSelection'),
        ),
        migrations.AddField(
            model_name='guideplatelayout',
            name='guide_selection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.GuideSelection'),
        ),
    ]
