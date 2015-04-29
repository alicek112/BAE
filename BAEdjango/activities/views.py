from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Catlist
from .models import Mainbae

def index(request):
    return render(request, 'activities/index.html')

def cat(request, cat_id):
    try:
        catl = Catlist.objects.get(pk = cat_id)
    except Catlist.DoesNotExist:
        raise Http404("Category does not exist")
    events = Mainbae.objects.filter(category = cat_id).order_by('start')
    context = {'cat': catl, 'events': events}
    return render(request, 'activities/category.html', context)
