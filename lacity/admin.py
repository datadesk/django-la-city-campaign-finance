from django.contrib import admin
from lacity.models import (
    LACityContribution,
    LACityCandidate,
    LACityCommittee
)


class LACityCandidateAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name']


class LACityCommitteeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'committee_id',
        'committee_type',
        'lacitycandidate'
    ]
    raw_id_fields = ('lacitycandidate',)


class LACityContributionAdmin(admin.ModelAdmin):
    list_display = [
        'amount_received',
        'amount_paid',
        'load_date',
        'date',
        'lacitycommittee',
        'contributor_first_name',
        'contributor_last_name',
        'occupation',
        'employer',
        'schedule',
        'contribution_type',
        'document_id',
        'record_id',
    ]
    search_fields = [
        'lacitycommittee',
        'contributor_first_name',
        'contributor_last_name',
        'occupation',
        'employer',
        'contributor_city',
        'document_id',
        'record_id',
    ]
    list_filter = [
        'schedule',
        'contribution_type',
    ]
    raw_id_fields = ('lacitycommittee',)
    readonly_fields = ('load_date',)
    fieldsets = (
        (None, {
            'fields': (
                ('amount_received', 'amount_paid'),
                ('date', 'lacitycommittee'),
            ),
        }),
        ('Meta', {
            'fields': (
                ('schedule', 'contribution_type'),
                ('filing_start_date', 'filing_end_date'),
                ('election_date', 'load_date'),
                ('office_type', 'district_number'),
                ('document_id', 'record_id'),
                'memo', 'description',
            ),
        }),
        ('Contributor', {
            'fields': (
                ('contributor_first_name', 'contributor_last_name'),
                ('occupation', 'employer'),
                ('contributor_address_line_one',
                    'contributor_address_line_two'),
                ('contributor_city', 'contributor_state'),
                ('contributor_zip_code', 'contributor_zip_code_ext'),
            ),
        }),
        ('Intermediary', {
            'fields': (
                ('intermediary_name', 'intermediary_city'),
                ('intermediary_state', 'intermediary_zip_code'),
                ('intermediary_occupation', 'intermediary_employer'),
            ),
        }),
    )

admin.site.register(LACityCandidate, LACityCandidateAdmin)
admin.site.register(LACityCommittee, LACityCommitteeAdmin)
admin.site.register(LACityContribution, LACityContributionAdmin)
