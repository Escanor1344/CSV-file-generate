from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages

from mainapp.forms import SchemasGeneralForm
from mainapp.models import SchemasGeneral, SchemasColumns
from mainapp.forms import SchemasColumnsFormset
from mainapp.services import CSVStream


class DataSchemas(ListView):
    """ Display main page with list of users schemas. """
    paginate_by = 13
    template_name = 'index.html'
    context_object_name = 'schemas'

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return SchemasGeneral.objects.none()
        return SchemasGeneral.objects.filter(user=self.request.user).order_by('-id')


class SchemaCreateView(LoginRequiredMixin, CreateView):
    """ Create new schema. """
    form = SchemasGeneralForm
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        return render(request, 'schema_create-update.html', context={
            'form': self.form,  #SchemaGeneralForm
            'formset': SchemasColumnsFormset(queryset=SchemasColumns.objects.none())  # SchemaColumnsFormSet.
        })

    def post(self, request, *args, **kwargs):
        form_post = self.form(request.POST) # SchemaGeneralForm.
        formset = SchemasColumnsFormset(request.POST) # SchemaColumnsFormSet.

        if all([formset.is_valid(), form_post.is_valid()]):
            parent = form_post.save(commit=False)
            parent.user = request.user
            parent.save()
            for form in formset:
                child = form.save(commit=False)
                child.general = parent
                child.save()
            messages.success(request, 'New schema was added')
            return redirect('home')


class SchemaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """ Delete the schema. """
    model = SchemasGeneral
    success_url = reverse_lazy('home')
    login_url = '/accounts/login/'
    success_message = 'Schema was deleted'


class SchemaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """ Update the schema. """
    model = SchemasGeneral
    template_name = 'schema_create-update.html'
    success_url = reverse_lazy('home')
    form_class = SchemasGeneralForm
    login_url = '/accounts/login/'
    success_message = 'Schema was updated'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Contex for formset.
        context['formset'] = SchemasColumnsFormset(queryset=SchemasColumns.objects.filter(general_id=self.kwargs['pk']))
        return context

    def post(self, request, *args, **kwargs):
        super(SchemaUpdateView, self).post(request)
        # Post for formset.
        formset = SchemasColumnsFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                x = form.save(commit=False)
                x.general_id = self.kwargs['pk']
                x.save()
            return redirect('home')


class SchemaCsvCreate(LoginRequiredMixin, ListView):
    """ Download the current schema. """
    model = SchemasColumns
    template_name = 'schema_csv_create.html'
    context_object_name = 'schema'
    login_url = '/accounts/login/'

    def get_queryset(self):
        # Get SchemasColumns objects by SchemaGeneral.id.
        return SchemasColumns.objects.filter(general_id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        schema_values = self.get_queryset()
        # Get number of rows from user.
        csv_rows = request.GET.get('csv_rows', False)
        delimiter = SchemasGeneral.objects.get(id=self.kwargs['pk']).column_separator
        quotechar = SchemasGeneral.objects.get(id=self.kwargs['pk']).string_character

        # If my/url/?csv_rows=int.
        if csv_rows:
            csv_stream = CSVStream()
            return csv_stream.export_csv_file(request, schema_values, csv_rows, delimiter, quotechar)
        return super(SchemaCsvCreate, self).get(request, *args, **kwargs)
