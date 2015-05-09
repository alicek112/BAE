from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from .models import Catlist, Mainbae

# main page
def index(request):
	allcats = Catlist.objects.all().order_by('name')
	context = RequestContext(request, {'allcats': allcats})
	template = loader.get_template('activities/index.html')
	return HttpResponse(template.render(context))

# about/product showcase
def about(request):
    context = RequestContext(request)
    template = loader.get_template('activities/about.html')
    return HttpResponse(template.render(context))

# specific category page
def cat(request, cat_id):
    try:
       catl = Catlist.objects.get(pk = cat_id)
    except Catlist.DoesNotExist:
        raise Http404("Category does not exist")
    allcats = Catlist.objects.all().order_by('name')
    context = RequestContext(request, {'cat': catl, 'allcats': allcats})
    template = loader.get_template('activities/category.html')
    return HttpResponse(template.render(context))
