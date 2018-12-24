# Generated by Django 2.1.2 on 2018-11-23 08:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('chartofaccountDIT', '0008_merge_20181123_0859'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analysis1',
            options={'ordering': ['analysis1_code'],
                     'verbose_name': 'Contract Reconciliation (Analysis 1)',
                     'verbose_name_plural': 'Contract Reconciliations (Analysis 1)'},
        ),
        migrations.AlterModelOptions(
            name='analysis2',
            options={'ordering': ['analysis2_code'], 'verbose_name': 'Market (Analysis 2)',
                     'verbose_name_plural': 'Markets (Analysis 2)'},
        ),
        migrations.AlterModelOptions(
            name='commercialcategory',
            options={'ordering': ['commercial_category'], 'verbose_name': 'Commercial Category',
                     'verbose_name_plural': 'Commercial Categories'},
        ),
        migrations.AlterModelOptions(
            name='expenditurecategory',
            options={'ordering': ['grouping_description'], 'verbose_name': 'Budget Category',
                     'verbose_name_plural': 'Budget Categories'},
        ),
        migrations.AlterModelOptions(
            name='interentity',
            options={'ordering': ['l2_value'], 'verbose_name': 'Inter-Entity',
                     'verbose_name_plural': 'Inter-Entities'},
        ),
        migrations.AlterModelOptions(
            name='interentityl1',
            options={'ordering': ['l1_value'], 'verbose_name': 'Government Body',
                     'verbose_name_plural': 'Government Bodies'},
        ),
        migrations.AlterModelOptions(
            name='naccategory',
            options={'ordering': ['NAC_category_description'], 'verbose_name': 'Budget Grouping',
                     'verbose_name_plural': 'Budget Groupings'},
        ),
        migrations.AlterModelOptions(
            name='programmecode',
            options={'ordering': ['programme_code'], 'verbose_name': 'Programme Code',
                     'verbose_name_plural': 'Programme Codes'},
        ),
        migrations.AlterModelOptions(
            name='projectcode',
            options={'ordering': ['project_code'], 'verbose_name': 'Project',
                     'verbose_name_plural': 'Projects'},
        ),
    ]
