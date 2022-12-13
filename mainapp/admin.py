from django.contrib import admin

from .models import SchemasColumns, SchemasGeneral


class SchemasColumnsInline(admin.StackedInline):
    model = SchemasColumns
    extra = 0


class SchemaAdmin(admin.ModelAdmin):
    inlines = [SchemasColumnsInline]
    list_display = ['title', 'user_id']


admin.site.register(SchemasGeneral, SchemaAdmin)
