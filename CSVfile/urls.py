from django.contrib import admin
from django.urls import path, include

from mainapp.views import DataSchemas, SchemaCreateView, SchemaDeleteView, SchemaUpdateView, SchemaCsvCreate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DataSchemas.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('newschema/', SchemaCreateView.as_view(), name='newschema'),
    path('schema_edit/<int:pk>', SchemaUpdateView.as_view(), name='schema_edit'),
    path('schema_delete/<int:pk>', SchemaDeleteView.as_view(), name='schema_delete'),
    path('schema_csv_create/<int:pk>', SchemaCsvCreate.as_view(), name='schema_csv_create'),
]
