# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LACityCandidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=250, blank=True)),
                ('last_name', models.CharField(max_length=250, blank=True)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='LACityCommittee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, blank=True)),
                ('committee_id', models.CharField(max_length=250)),
                ('committee_type', models.CharField(max_length=250, blank=True)),
                ('lacitycandidate', models.ForeignKey(to='lacity.LACityCandidate')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LACityContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_received', models.DecimalField(max_digits=16, decimal_places=2)),
                ('amount_paid', models.DecimalField(max_digits=16, decimal_places=2)),
                ('date', models.DateField(null=True, blank=True)),
                ('office_type', models.CharField(max_length=250, blank=True)),
                ('district_number', models.CharField(max_length=250, blank=True)),
                ('occupation', models.CharField(max_length=250, blank=True)),
                ('employer', models.CharField(max_length=250, blank=True)),
                ('contributor_first_name', models.CharField(max_length=250, blank=True)),
                ('contributor_last_name', models.CharField(max_length=250, blank=True)),
                ('contributor_address_line_one', models.CharField(max_length=250, blank=True)),
                ('contributor_address_line_two', models.CharField(max_length=250, blank=True)),
                ('contributor_city', models.CharField(max_length=250, blank=True)),
                ('contributor_state', models.CharField(max_length=250, blank=True)),
                ('contributor_zip_code', models.CharField(max_length=250, blank=True)),
                ('contributor_zip_code_ext', models.CharField(max_length=250, blank=True)),
                ('schedule', models.CharField(max_length=250, blank=True)),
                ('contribution_type', models.CharField(max_length=250, blank=True)),
                ('filing_start_date', models.DateField(null=True, blank=True)),
                ('filing_end_date', models.DateField(null=True, blank=True)),
                ('election_date', models.DateField(null=True, blank=True)),
                ('intermediary_name', models.CharField(max_length=250, blank=True)),
                ('intermediary_city', models.CharField(max_length=250, blank=True)),
                ('intermediary_state', models.CharField(max_length=250, blank=True)),
                ('intermediary_zip_code', models.CharField(max_length=250, blank=True)),
                ('intermediary_occupation', models.CharField(max_length=250, blank=True)),
                ('intermediary_employer', models.CharField(max_length=250, blank=True)),
                ('memo', models.CharField(max_length=250, blank=True)),
                ('description', models.TextField(blank=True)),
                ('document_id', models.CharField(max_length=250, blank=True)),
                ('record_id', models.CharField(max_length=250, blank=True)),
                ('load_date', models.DateField(auto_now_add=True)),
                ('lacitycommittee', models.ForeignKey(blank=True, to='lacity.LACityCommittee', null=True)),
            ],
            options={
                'ordering': ['date', '-amount_received', '-amount_paid'],
            },
        ),
    ]
