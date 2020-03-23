# Generated by Django 2.2.10 on 2020-02-14 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_auto_20200214_1117'),
        ('treasurySS', '0107_auto_20200214_1117'),
        ('costcentre', '0029_auto_20190703_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='historiccostcentre',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historiccostcentre',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='SimpleHistoryHistoricCostCentre',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('archived', models.DateTimeField(blank=True, editable=False)),
                ('group_code', models.CharField(max_length=50, verbose_name='Group Code')),
                ('group_name', models.CharField(max_length=300, verbose_name='Group Name')),
                ('dg_fullname', models.CharField(blank=True, max_length=200, null=True, verbose_name='Director General')),
                ('directorate_code', models.CharField(max_length=50, verbose_name='Directorate Code')),
                ('directorate_name', models.CharField(max_length=300, verbose_name='Directorate Name')),
                ('director_fullname', models.CharField(blank=True, max_length=200, null=True, verbose_name='Director')),
                ('cost_centre_code', models.CharField(max_length=50, verbose_name='Cost Centre Code')),
                ('cost_centre_name', models.CharField(max_length=300, verbose_name='Cost Centre Name')),
                ('deputy_director_fullname', models.CharField(blank=True, max_length=200, null=True, verbose_name='Deputy Director')),
                ('business_partner_fullname', models.CharField(blank=True, max_length=200, null=True, verbose_name='Business Partner')),
                ('active', models.BooleanField(default='True')),
                ('disabled_with_actual', models.BooleanField(default='False', verbose_name='Disabled (Actuals to be cleared)')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('bsce_email', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='costcentre.BSCEEmail', verbose_name='BSCE Email')),
                ('financial_year', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.FinancialYear')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Historic Cost Centre',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='SimpleHistoryDirectorate',
            fields=[
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=False)),
                ('directorate_code', models.CharField(db_index=True, max_length=6, verbose_name='Directorate Code')),
                ('directorate_name', models.CharField(max_length=300, verbose_name='Directorate Name')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('director', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='costcentre.CostCentrePerson')),
                ('group', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='costcentre.DepartmentalGroup')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Directorate',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='SimpleHistoryDepartmentalGroup',
            fields=[
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=False)),
                ('group_code', models.CharField(db_index=True, max_length=6, verbose_name='Group Code')),
                ('group_name', models.CharField(max_length=300, verbose_name='Group Name')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('director_general', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='costcentre.CostCentrePerson')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('treasury_segment_fk', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='treasurySS.Segment', verbose_name='Treasury Segment')),
            ],
            options={
                'verbose_name': 'historical Departmental Group',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='SimpleHistoryCostCentrePerson',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('is_director', models.BooleanField(default=False, verbose_name='Director')),
                ('is_dg', models.BooleanField(default=False, verbose_name='General Director')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Hierarchy Responsibility',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='SimpleHistoryCostCentre',
            fields=[
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=False)),
                ('cost_centre_code', models.CharField(db_index=True, max_length=6, verbose_name='Cost Centre Code')),
                ('cost_centre_name', models.CharField(max_length=300, verbose_name='Cost Centre Name')),
                ('disabled_with_actual', models.BooleanField(default='False', verbose_name='Disabled (Actuals to be cleared)')),
                ('used_for_travel', models.BooleanField(default='True', verbose_name='Used for Travel')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('bsce_email', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='costcentre.BSCEEmail', verbose_name='BSCE Email')),
                ('business_partner', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='costcentre.BusinessPartner', verbose_name='Finance Business Partner')),
                ('deputy_director', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='costcentre.CostCentrePerson', verbose_name='Deputy Director')),
                ('directorate', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='costcentre.Directorate')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Cost Centre',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='SimpleHistoryBusinessPartner',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('bp_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Business Partner email')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Business Partner',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='SimpleHistoryBSCEEmail',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('active', models.BooleanField(default=False)),
                ('bsce_email', models.EmailField(db_index=True, max_length=254, verbose_name='BSCE email')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical BSCE Email',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
