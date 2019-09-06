from django import forms
import django.db.models as models
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError

from orihime.models import Source, Text, Word, WordRelation

from orihime.serializers import TextSerializer

from rest_framework import serializers

class SourceModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return "{}".format(obj.name)

class FlatPageForm(forms.ModelForm):

    contents = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    source = SourceModelChoiceField(queryset=Source.objects.all(),
                                    required=False,
                                    empty_label="",
                                    to_field_name="name")

    class Meta:
        model = Text
        fields = ['contents', 'source']

# Only allow viewing this page if authenticated        
def mce_test(request):

    if not request.user.is_authenticated: 

        return HttpResponseRedirect('/login/')

    if request.method == 'POST':

        form = FlatPageForm(request.POST)

        if form.is_valid():

            serialize_data = {
                'user': request.user.email,
                'source': form.fields['source'].clean(request.POST['source']),
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
        
        form = FlatPageForm()
        return render(request, 'flatpages/tinymce-test.html', {'form': form})
