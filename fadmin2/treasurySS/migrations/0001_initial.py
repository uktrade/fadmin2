# Generated by Django 2.0.2 on 2018-09-06 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EstimateRow',
            fields=[
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('estimate_row_code', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='estimates row code')),
                ('estimate_row_long_name', models.CharField(max_length=255, verbose_name='estimates row long name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('segment_code', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='segment code')),
                ('segment_long_name', models.CharField(max_length=255, verbose_name='segment long name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SegmentGrandParent',
            fields=[
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('segment_grand_parent_code', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='segment grand parent code')),
                ('segment_grand_parent_long_name', models.CharField(max_length=255, verbose_name='segment grandparent long name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SegmentParent',
            fields=[
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('segment_parent_code', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='segment parent code')),
                ('segment_parent_long_name', models.CharField(max_length=255, verbose_name='segment parent long name')),
                ('segment_grand_parent_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='treasurySS.SegmentGrandParent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubSegment',
            fields=[
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sub_segment_code', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='sub segment code')),
                ('sub_segment_long_name', models.CharField(max_length=255, verbose_name='sub segment long name')),
                ('control_budget_detail_code', models.CharField(choices=[('NON-BUDGET', 'NON-BUDGET'), ('AME', (('DEPT AME', 'DEPT AME'), ('NON-DEPT AME', 'NON-DEPT AME'))), ('DEL', (('DEL ADMIN', 'DEL ADMIN'), ('DEL PROG', 'DEL PROG')))], default='NON-BUDGET', max_length=50, verbose_name='control budget detail code')),
                ('net_subhead_code', models.CharField(max_length=255, verbose_name='net subhead code')),
                ('policy_ringfence_code', models.CharField(max_length=255, verbose_name='policy ringfence code')),
                ('accounting_authority_code', models.CharField(max_length=255, verbose_name='accounting authority code')),
                ('accounting_authority_DetailCode', models.CharField(choices=[('VT', 'VOTED'), ('NVT', (('NON - VOTED_DEPT', 'NON - VOTED_DEPT'), ('NON-VOTED_CFER', 'NON-VOTED_CFER'), ('NON-VOTED_CF', 'NON-VOTED_CF'), ('NON-VOTED_PC', 'NON-VOTED_PC'), ('NON-VOTED_NIF', 'NON-VOTED_NIF'), ('NON-VOTED_NLF', 'NON-VOTED_NLF'), ('NON-VOTED_CEX', 'NON-VOTED_CEX'), ('NON-VOTED_SF', 'NON-VOTED_SF'), ('NON-VOTED_LG', 'NON-VOTED_LG'), ('NON-VOTED_DA', 'NON-VOTED_DA'))), ('N/A', 'N/A')], default='N/A', max_length=255, verbose_name='accounting authority detail code')),
                ('Segment_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='treasurySS.Segment')),
                ('estimates_row_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='treasurySS.EstimateRow')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='segment',
            name='segment_parent_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='treasurySS.SegmentParent'),
        ),
    ]
