# coding: utf-8
"""
   여보세요 Forms
"""
from django.forms import ModelForm
from yeoboseyo.models import Trigger


class TriggerForm(ModelForm):
    class Meta:
        model = Trigger
        fields = '__all__'
