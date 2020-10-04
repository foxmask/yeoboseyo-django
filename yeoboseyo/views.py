# coding: utf-8
"""
   여보세요 Views
"""
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from yeoboseyo.models import Trigger
from yeoboseyo.forms import TriggerForm


def switch_status(request, id, status):
    """

    """
    Trigger.objects.filter(id=id).update(status=status)
    messages.add_message(request, messages.INFO, f'Trigger switch to <strong>{status}</strong>')
    return HttpResponseRedirect(reverse('home'))


def switch_mail(request, id, status):
    """

    """
    Trigger.objects.filter(id=id).update(mail=status)
    messages.add_message(request, messages.INFO, f'Trigger mail switch to <strong>{status}</strong>')
    return HttpResponseRedirect(reverse('home'))


def switch_masto(request, id, status):
    """

    """
    Trigger.objects.filter(id=id).update(mastodon=status)
    messages.add_message(request, messages.INFO, f'Trigger mastodon switch to <strong>{status}</strong>')
    return HttpResponseRedirect(reverse('home'))



class Home(ListView):

    model = Trigger
    paginate_by = 9
    ordering = ['-date_created']

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        page_size = self.paginate_by
        context_object_name = self.get_context_object_name(queryset)

        context = super(Home, self).get_context_data(**kwargs)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context['paginator'] = paginator
            context['page_obj'] = page
            context['is_paginated'] = is_paginated
            context['object_list'] = queryset
        else:
            context['paginator'] = None
            context['page_obj'] = None
            context['is_paginated'] = False
            context['object_list'] = queryset

        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)

        return context


class TriggerMixin:

    def get_context_data(self, **kwargs):
        context = super(TriggerMixin, self).get_context_data(**kwargs)
        context['MY_NOTES_FOLDER'] = settings.MY_NOTES_FOLDER
        print(settings.MY_NOTES_FOLDER)
        return context


class TriggerCreate(TriggerMixin, CreateView):

    model = Trigger
    fields = '__all__'
    success_url = '/'


class TriggerUpdate(TriggerMixin, UpdateView):

    model = Trigger
    fields = '__all__'
    success_url = '/'

