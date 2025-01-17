# Generated by Django 5.0.2 on 2024-04-22 13:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_remove_userprofile_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='return_date',
        ),
        migrations.AddField(
            model_name='equipment',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='last_audit',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='equipment',
            name='status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='asset_tag',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.location'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='type',
            field=models.CharField(max_length=100),
        ),
    ]
