# coding: utf-8
"""
   여보세요 Views
"""
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from yeoboseyo.models import Trigger
from yeoboseyo.forms import TriggerForm


def delete_trigger(request, pk):
    """

    :param request:
    :param id:
    :return:
    """
    trigger = Trigger.objects.get(id=pk)
    description = trigger.description
    trigger.delete()
    messages.add_message(request, messages.INFO, f'Trigger {description} <strong>deleted</strong>')
    return HttpResponseRedirect(reverse('home'))


def on_off(status):
    """

    :param status:
    :return:
    """
    return 'Off' if status else 'On'


def switch_status(request, id, status):
    """

    :param request:
    :param id:
    :param status:
    :return:
    """

    Trigger.objects.filter(id=id).update(status=status)
    messages.add_message(request, messages.INFO, f'Trigger switch to <strong>{on_off(status)}</strong>')
    return HttpResponseRedirect(reverse('home'))


def switch_mail(request, id, status):
    """

    :param request:
    :param id:
    :param status:
    :return:
    """

    Trigger.objects.filter(id=id).update(mail=status)
    messages.add_message(request, messages.INFO, f'Trigger mail switch to <strong>{on_off(status)}</strong>')
    return HttpResponseRedirect(reverse('home'))


def switch_masto(request, id, status):
    """

    :param request:
    :param id:
    :param status:
    :return:
    """

    Trigger.objects.filter(id=id).update(mastodon=status)
    messages.add_message(request, messages.INFO, f'Trigger mastodon switch to <strong>{on_off(status)}</strong>')
    return HttpResponseRedirect(reverse('home'))


class Home(ListView):

    model = Trigger
    paginate_by = 100
    ordering = ['description']

    def get_template_names(self):
        display = 'table'
        if 'display' in self.request.GET and self.request.GET['display'] in ('table', 'card'):
            display = self.request.GET['display']
        return ['yeoboseyo/trigger_list_%s.html' % display]

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

        display = 'table'
        if 'display' in self.request.GET and self.request.GET['display'] in ('table', 'card'):
            display = self.request.GET['display']
        context['display'] = 'card' if display == 'table' else 'table'

        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)

        return context


class TriggerMixin:

    def get_context_data(self, **kwargs):
        context = super(TriggerMixin, self).get_context_data(**kwargs)
        context['MY_NOTES_FOLDER'] = settings.MY_NOTES_FOLDER
        return context


class TriggerCreate(TriggerMixin, CreateView):

    model = Trigger
    form_class = TriggerForm
    success_url = reverse_lazy('home')


class TriggerUpdate(TriggerMixin, UpdateView):

    model = Trigger
    form_class = TriggerForm
    success_url = reverse_lazy('home')


class TriggerDelete(DeleteView):

    model = Trigger
    success_url = reverse_lazy('home')
