from django.db import models


class Accreditation(models.Model):
    STANDARD = 'Standard'
    ADVANCED = 'Advanced'
    TYPE_CHOICES = [
        (STANDARD, 'Standard'),
        (ADVANCED, 'Advanced'),
    ]
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    type = models.CharField(choices=TYPE_CHOICES, default=STANDARD, max_length=8, blank=False)
    date = models.DateField()
    uc_username = models.CharField(max_length=50, blank=False)
    wfdf_userid = models.IntegerField()
    last_modified_at = models.DateTimeField(auto_now=True)
