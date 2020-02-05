# Generated by Django 2.2.8 on 20200130 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_historicalgroup_historicalpermission_historicaluser'),
        ('chartofaccountDIT', '0051_auto_20191106_1235'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HistoricalAnalysis1',
            new_name='ArchivedAnalysis1',
        ),
        migrations.RenameModel(
            old_name='HistoricalAnalysis2',
            new_name='ArchivedAnalysis2',
        ),
        migrations.RenameModel(
            old_name='HistoricalCommercialCategory',
            new_name='ArchivedCommercialCategory',
        ),
        migrations.RenameModel(
            old_name='HistoricalExpenditureCategory',
            new_name='ArchivedExpenditureCategory',
        ),
        migrations.RenameModel(
            old_name='HistoricalFCOMapping',
            new_name='ArchivedFCOMapping',
        ),
        migrations.RenameModel(
            old_name='HistoricalInterEntity',
            new_name='ArchivedInterEntity',
        ),
        migrations.RenameModel(
            old_name='HistoricalNaturalCode',
            new_name='ArchiveNaturalCode',
        ),
        migrations.RenameModel(
            old_name='HistoricalProgrammeCode',
            new_name='ArchivedProgrammeCode',
        ),
        migrations.RenameModel(
            old_name='HistoricalProjectCode',
            new_name='ArchivedProjectCode',
        ),
    ]
