from django import forms
from django.forms import modelformset_factory

from mainapp.models import SchemasGeneral, SchemasColumns


class SchemasGeneralForm(forms.ModelForm):
    class Meta:
        model = SchemasGeneral
        fields = ['title', 'column_separator', 'string_character']


class SchemasColumnsForm(forms.ModelForm):
    class Meta:
        model = SchemasColumns
        fields = ('column_name', 'column_type')

SchemasColumnsFormset = modelformset_factory(SchemasColumns, form=SchemasColumnsForm, extra=0)
