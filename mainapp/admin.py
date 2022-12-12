from django.contrib import admin

from .models import SchemasColumns, SchemasGeneral


class SchemasColumnsInline(admin.StackedInline):
    model = SchemasColumns
    extra = 0
    # readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']


class SchemaAdmin(admin.ModelAdmin):
    inlines = [SchemasColumnsInline]
    # list_display = ['name', 'user']
    # readonly_fields = ['timestamp', 'updated']
    # raw_id_fields = ['user']


admin.site.register(SchemasGeneral, SchemaAdmin)
