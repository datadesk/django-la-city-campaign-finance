from django.db import models


class LACityContribution(models.Model):
    amount_received = models.DecimalField(max_digits=16, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateField(auto_now=False, null=True, blank=True)
    office_type = models.CharField(max_length=250, blank=True)
    district_number = models.CharField(max_length=250, blank=True)
    occupation = models.CharField(max_length=250, blank=True)
    employer = models.CharField(max_length=250, blank=True)
    contributor_first_name = models.CharField(max_length=250, blank=True)
    contributor_last_name = models.CharField(max_length=250, blank=True)
    contributor_address_line_one = models.CharField(max_length=250, blank=True)
    contributor_address_line_two = models.CharField(max_length=250, blank=True)
    contributor_city = models.CharField(max_length=250, blank=True)
    contributor_state = models.CharField(max_length=250, blank=True)
    contributor_zip_code = models.CharField(max_length=250, blank=True)
    contributor_zip_code_ext = models.CharField(max_length=250, blank=True)
    schedule = models.CharField(max_length=250, blank=True)
    contribution_type = models.CharField(max_length=250, blank=True)
    filing_start_date = models.DateField(null=True, blank=True)
    filing_end_date = models.DateField(null=True, blank=True)
    election_date = models.DateField(null=True, blank=True)
    intermediary_name = models.CharField(max_length=250, blank=True)
    intermediary_city = models.CharField(max_length=250, blank=True)
    intermediary_state = models.CharField(max_length=250, blank=True)
    intermediary_zip_code = models.CharField(max_length=250, blank=True)
    intermediary_occupation = models.CharField(max_length=250, blank=True)
    intermediary_employer = models.CharField(max_length=250, blank=True)
    memo = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    document_id = models.CharField(max_length=250, blank=True)
    record_id = models.CharField(max_length=250, blank=True)
    # So we can keep track of when it was loaded
    load_date = models.DateField(auto_now_add=True)
    lacitycommittee = models.ForeignKey('LACityCommittee', null=True, blank=True)
    
    class Meta:
        ordering = ['date', '-amount_received', '-amount_paid']
    
    def __unicode__(self):
        return '%s: %s' % (self.pk, self.amount_received)


class LACityCommittee(models.Model):
    name = models.CharField(max_length=250, blank=True)
    committee_id = models.CharField(max_length=250)
    committee_type = models.CharField(max_length=250, blank=True)
    lacitycandidate = models.ForeignKey('LACityCandidate')
        
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name


class LACityCandidate(models.Model):
    """
    A candidate for office in L.A. City.
    """
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    
    class Meta:
        ordering = ['last_name']
    
    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)
