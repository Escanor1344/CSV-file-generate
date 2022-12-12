from django.contrib.auth.models import User
from django.db import models

CHOICES1 = (
        ('Full name', 'Full name'),
        ('Job', 'Job'),
        ('Email',  'Email'),
        ('Domain name',  'Domain name'),
        ('Phone number', 'Phone number'),
        ('Company name', 'Company name'),
        ('Text', 'Text'),
        ('Integer', 'Integer'),
        ('Address', 'Address'),
        ('Date', 'Date'),
)

CHOICES2 = (
    (',', " Comma (,)"),
    (';', "Semicolon(;)")
)

CHOICES3 = (
    ('"', 'Double-quote(")'),
    ('hz', "hz")
)


class SchemasGeneral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=15)
    modified = models.DateField(auto_now_add=True)
    column_separator = models.CharField(max_length=1, choices=CHOICES2)
    string_character = models.CharField(max_length=2, choices=CHOICES3)


class SchemasColumns(models.Model):
    general = models.ForeignKey(SchemasGeneral, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=20)
    column_type = models.CharField(max_length=12, choices=CHOICES1)
