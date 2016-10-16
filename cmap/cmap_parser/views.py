from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from .models import Cmap
from django import forms
from .parsers import CsvMap, CxlMap, Marker
import io
import json
from itertools import chain


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
    concepts = cmap['concepts']
    minx = min(i['x'] for i in concepts.values())
    miny = min(i['y'] for i in concepts.values())
    maxx = max(i['x'] for i in concepts.values())
    maxy = max(i['y'] for i in concepts.values())
    width = maxx - minx
    height = maxy - miny
    scale = 588/width
    for i in concepts.values():
        i['x'] -= minx
        i['y'] -= miny
        i['x'] = int(i['x'] * scale)
        i['y'] = int(i['y'] * scale)
    width = int(width * scale)
    height = int(height * scale)

    cmap['json'] = json.dumps(cmap)

    num = 0
    for i in chain(cmap['correct propsitions'], cmap['incorrect propsitions'], cmap['absent propsitions'], cmap['neutral propsitions']):
        i['id'] = num
        num += 1

    return render(request, './map.html', {'cmap': cmap, 'width': width, 'height': height})
