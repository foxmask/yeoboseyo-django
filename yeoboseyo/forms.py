# coding: utf-8
"""
   여보세요 Forms
"""
from django.forms import ModelForm, TextInput, CheckboxInput
from yeoboseyo.models import Trigger


class TriggerForm(ModelForm):
    class Meta:
        model = Trigger
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'rss_url': TextInput(attrs={'class': 'form-control'}),
            'joplin_folder': TextInput(attrs={'class': 'form-control'}),
            'localstorage': TextInput(attrs={'class': 'form-control'}),
            'reddit': TextInput(attrs={'class': 'form-control'}),
            'mastodon': CheckboxInput(attrs={'class': 'form-check-input'}),
            'mail': CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': CheckboxInput(attrs={'class': 'form-check-input'}),
        }
