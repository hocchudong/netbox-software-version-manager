# Generated by Django 3.2.9 on 2022-04-15 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0153_created_datetimefield'),
        ('virtualization', '0029_created_datetimefield'),
        ('netbox_svm', '0003_auto_20220407_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='softwareproduct',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dcim.manufacturer'),
        ),
        migrations.AlterField(
            model_name='softwareproductinstallation',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dcim.device'),
        ),
        migrations.AlterField(
            model_name='softwareproductinstallation',
            name='software_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='netbox_svm.softwareproduct'),
        ),
        migrations.AlterField(
            model_name='softwareproductinstallation',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='netbox_svm.softwareproductversion'),
        ),
        migrations.AlterField(
            model_name='softwareproductinstallation',
            name='virtualmachine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='virtualization.virtualmachine'),
        ),
        migrations.AlterField(
            model_name='softwareproductversion',
            name='software_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='netbox_svm.softwareproduct'),
        ),
    ]
