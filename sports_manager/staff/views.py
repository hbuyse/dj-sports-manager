# -*- coding: utf-8 -*-
"""Staff views."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context, loader
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View

# Current django project
from sports_manager.mixins import StaffMixin
from sports_manager.license.models import License

logger = logging.getLogger(__name__)


class StaffLinksView(TemplateView):

    template_name = 'sports_manager/staff/index.html'


class StaffLicenseListView(View):

    csv_template_name = "sports_manager/staff/licenses.csv"

    def get(self, request, *args, **kwargs):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(self.csv_template_name.split('/')[-1])

        t = loader.get_template(self.csv_template_name)
        datas = {
            'licenses': License.objects.all(),
        }
        response.write(t.render(datas))
        return response