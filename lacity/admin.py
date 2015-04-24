from django.contrib import admin
from lacity.models import LACityContribution, LACityCommittee, LACityCandidate


class LACityCandidateAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name']


class LACityCommitteeAdmin(admin.ModelAdmin):
    list_display = ['name', 'committee_id', 'committee_type', 'lacitycandidate']


class LACityContributionAdmin(admin.ModelAdmin):
    pass
    # date_hierarchy = 'filing_start_date'
    # list_display = ['amount', 'committee',
    #     'first_name', 'last_name', 'occupation', 'employer',
    #     'city', 'state', 'initial_category',
    #     'verified_category', 'date', 'record_id', 'entry_type']
    # search_fields = ['committee__name', 'first_name',
    #     'last_name', 'occupation', 'employer', 'city',
    #     'state', 'zip_code', 'initial_category',
    #     'record_id', 'description']
    # list_filter = ['entry_type', 'contribution_type',
    #     'initial_category', 'verified_category', 'committee']
    # list_editable = ['initial_category', 'verified_category']
    # fieldsets = (
    #     (None, {
    #         'fields': (
    #             ('amount', 'description'),
    #             'date', 'initial_category',
    #             ('entry_type', 'is_unitemized', 'verified_category'),
    #         ),
    #     }),
    #     ('Contributor', {
    #         'fields': (
    #             ('first_name', 'last_name'),
    #             ('occupation', 'employer'),
    #             ('address_line_one', 'address_line_two'),
    #             ('city', 'state', 'zip_code'),
    #             'candidate_to_self',
    #         ),
    #     }),
    #     ('Intermediary', {
    #         'fields': (
    #             ('intermediary_name', 'intermediary_city'),
    #             ('intermediary_state', 'intermediary_zip_code'),
    #             ('intermediary_occupation', 'intermediary_employer'),
    #         ),
    #     }),
    #     ('Meta', {
    #         'fields': (
    #             ('schedule', 'contribution_type'),
    #             ('filing_start_date', 'filing_end_date'),
    #             ('document_id', 'record_id'),
    #             'committee', 'clean_city',
    #         ),
    #     }),
    # )


admin.site.register(LACityCandidate, LACityCandidateAdmin)
admin.site.register(LACityCommittee, LACityCommitteeAdmin)
admin.site.register(LACityContribution, LACityContributionAdmin)
