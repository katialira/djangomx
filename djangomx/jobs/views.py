# coding: utf-8
from django.views.generic import DetailView
from django.core.mail import send_mail
from django.conf import settings

from annoying.decorators import render_to, ajax_request

from .models import Job
from .forms import JobForm


@render_to("jobs_home.html")
def jobs_home(request):
    """ Render Job opportunities home page. """
    jobs = Job.objects.filter(is_active=True, is_approved=True)
    form = JobForm()
    return {'jobs': jobs, 'form': form}


@ajax_request
def new_job(request):
    """ Add a new job"""
    if request.POST:
        form = form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            send_mail(
                'Nueva oferta de trabajo',
                'https://django.mx/admin/jobs/',
                settings.DEFAULT_FROM_EMAIL,
                [settings.NOTIFICATION_EMAIL],
                fail_silently=False
            )
            return {'success': True}
        else:
            return {'success': False, 'errors': form.errors.keys()}
    return {'success': False, 'error': 'Request not valid'}


class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'
