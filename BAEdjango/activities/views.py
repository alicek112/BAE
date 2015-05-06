from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import RequestContext, loader
from .models import Catlist
from .models import Mainbae
from django.contrib.auth import authenticate, login

def index(request):
	if not request.user.is_authenticated():
		user = authenticate()
		if user is not None:
			login(request, user)
		else:
			return HttpResponse("invalid login")

	allcats = Catlist.objects.all().order_by('name')
	context = RequestContext(request, {'allcats': allcats})
	template = loader.get_template('activities/index.html')
	return HttpResponse(template.render(context))


	

def cat(request, cat_id):
	if not request.user.is_authenticated():
		user = authenticate()
		if user is not None:
			login(request, user)
		else:
			return HttpResponse("invalid login")
			
    try:
       catl = Catlist.objects.get(pk = cat_id)
    except Catlist.DoesNotExist:
        raise Http404("Category does not exist")
    allcats = Catlist.objects.all().order_by('name')
    context = RequestContext(request, {'cat': catl, 'allcats': allcats})
    template = loader.get_template('activities/category.html')
    return HttpResponse(template.render(context))
