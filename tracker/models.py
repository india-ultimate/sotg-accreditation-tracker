from django.db import models


class Accreditation(models.Model):
    STANDARD = 'Standard'
    ADVANCED = 'Advanced'
    TYPE_CHOICES = [
        (STANDARD, 'Standard'),
        (ADVANCED, 'Advanced'),
    ]
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False, unique=True)
    type = models.CharField(choices=TYPE_CHOICES, default=STANDARD, max_length=8, blank=False)
    date = models.DateField(verbose_name="Accreditation Date", blank=True)
    uc_username = models.CharField(max_length=50, blank=False, verbose_name='Ultimate Central username', unique=True)
    wfdf_userid = models.IntegerField(verbose_name='WFDF user ID', blank=True, unique=True)
    last_modified_at = models.DateTimeField(auto_now=True)
