from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from .models import Cmap
from django import forms
from .parsers import CsvMap, CxlMap, Marker
import io
import json


class FileForm(forms.Form):
    csv = forms.FileField()
    cxl = forms.FileField()


def index(request):

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            csv = CsvMap(io.StringIO(request.FILES['csv'].read().decode()))
            cxl = CxlMap(io.StringIO(request.FILES['cxl'].read().decode()))
            m = Marker(csv, cxl)
            cmap = Cmap(csv=request.FILES['csv'].name, cxl=request.FILES['cxl'].name, content=m.to_json(indent=2))
            cmap.save()
            return HttpResponseRedirect('/%d/' % cmap.pk)

    if request.method == 'GET':
        context = {
            'file_list': Cmap.objects.order_by('-created'),
            'form': FileForm()
        }
        return render(request, './index.html', context)
    return HttpResponseBadRequest()


def view_map(request, pk):
    cmap = json.loads(Cmap.objects.get(pk=pk).content)
    cmap['json'] = json.dumps(cmap)
    return render(request, './map.html', {'cmap': cmap})


def view_comments(request, pk):
    cmap = json.loads(Cmap.objects.get(pk=pk).content)
    cmap['json'] = json.dumps(cmap)
    return render(request, './comments.html', {'cmap': cmap, 'pk': pk})
