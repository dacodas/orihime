from django import forms
from django.contrib.flatpages.models import FlatPage
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError
from django.utils.translation import gettext, gettext_lazy
from django.shortcuts import render

import django.db.models as models

import logging

from rest_framework import serializers

from tinymce.widgets import TinyMCE

from orihime.models import Source, Text, Word, WordRelation
from orihime.serializers import TextSerializer

logger = logging.getLogger(__name__)

class SourceModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return "{}".format(obj.name)

class TinyMCETextForm(forms.ModelForm):

    contents = \
        forms.CharField(
            widget=TinyMCE(attrs={'cols': 80,
                                  'rows': 30}),
            label=gettext_lazy("contents"))

    source = SourceModelChoiceField(queryset=Source.objects.all(),
                                    required=False,
                                    empty_label="",
                                    to_field_name="name",
                                    label=gettext_lazy("source"))

    class Meta:
        model = Text
        fields = ['contents', 'source']

def TinyMCETextView(request):

    if not request.user.is_authenticated: 

        return HttpResponseRedirect('/login/')

    if request.method == 'POST':

        form = TinyMCETextForm(request.POST)

        if form.is_valid():

            # TODO: Better understand the clean method on fields and
            # clean this bit up if it makes better sense to
            serialize_data = {
                'user': request.user.email,
                'source': form.fields['source'].clean(request.POST['source']).name,
                'contents': form.fields['contents'].clean(request.POST['contents'])
                }
                
            serializer = TextSerializer(data=serialize_data)

            if serializer.is_valid():
                
                text = serializer.save()
                return HttpResponseRedirect('/text-tree/{}'.format(text.id))

            else:

                return HttpResponseServerError(content="Your form was valid, but we failed to serialize it... Sorry!")

        else:

            return HttpResponseBadRequest(content=form.errors)

    else:
        
        form = TinyMCETextForm()
        return render(request, 'orihime/tinymce-text-view.html', {'form': form})
