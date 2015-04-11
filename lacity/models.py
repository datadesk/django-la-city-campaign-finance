from django.db import models


class LACityContribution(models.Model):
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateField(auto_now=False, null=True, blank=True)
    intermediary = models.CharField(max_length=250, blank=True)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    occupation = models.CharField(max_length=250, blank=True)
    employer = models.CharField(max_length=250, blank=True)
    address_line_one = models.CharField(max_length=250, blank=True)
    address_line_two = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    state = models.CharField(max_length=250, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
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
    document_id = models.CharField(max_length=250, blank=True)
    record_id = models.CharField(max_length=250, blank=True)
    committee = models.ForeignKey('LACityCommittee', null=True, blank=True)
    
    class Meta:
        ordering = ['date', '-amount']
    
    def __unicode__(self):
        return '%s: %s' % (self.pk, self.amount)


class LACityCandidate(models.Model):
    """
    A candidate for office in Los Angeles City
    """
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    district = models.CharField(max_length=250, blank=True)
    is_active = models.NullBooleanField(null=True)
    office = models.CharField(max_length=250, blank=True)
    candidate_id = models.CharField(max_length=250, blank=True)
    
    class Meta:
        ordering = ['last_name']
    
    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class LACityCommittee(models.Model):
    name = models.CharField(max_length=250, blank=True)
    committee_id = models.CharField(max_length=250)
    COMMITTEE_TYPE_CHOICES = (
        ('candidate', 'candidate'),
        ('independent', 'independent'),
        ('office_holder', 'office_holder'),
    )
    committee_type = models.CharField(max_length=250, choices=COMMITTEE_TYPE_CHOICES, blank=True)
    lacitycandidate = models.ForeignKey('LACityCandidate', null=True, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name