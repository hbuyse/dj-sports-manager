# -*- coding: utf-8 -*-
"""Staff views."""

# Standard library
import logging

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from django.template import loader
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import FormView, TemplateView, View

# Current django project
from sports_manager.models.license import License
from sports_manager.forms.staff import StaffSendEmailForm
from sports_manager.mixins import StaffMixin

logger = logging.getLogger(__name__)


class StaffLinksView(LoginRequiredMixin, StaffMixin, TemplateView):

    template_name = 'sports_manager/staff/index.html'


class StaffLicenseListView(LoginRequiredMixin, StaffMixin, View):

    csv_template_name = "sports_manager/staff/licenses.csv"

    def get(self, request, *args, **kwargs):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(self.csv_template_name.split('/')[-1])

        t = loader.get_template(self.csv_template_name)
        datas = {
            'licenses': get_list_or_404(License),
        }
        response.write(t.render(datas))
        return response

class StaffSendEmailView(LoginRequiredMixin, StaffMixin, FormView):

    template_name = "sports_manager/staff/send_email.html"
    form_class = StaffSendEmailForm

    def form_valid(self, form):
        form.get_list_of_recipients()
    