from django.utils import simplejson
from django.http import HttpResponse
from rss_feed.models import Category, Item
from django.forms.models import model_to_dict
import re
from datetime import datetime, timedelta
import calendar
from django.conf import settings
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def visited(request):
	if request.method == "POST":
		if request.POST.has_key(u'id') and request.POST.has_key(u'visited'):
			id = int(request.POST[u'id'])
			is_visisted = 'true' == request.POST[u'visited']		
			item = Item.objects.get(pk=id)
			updated = False
			if item:
				item.visited = is_visisted
				item.save()
				updated = True
	return HttpResponse({'updated': updated}, mimetype='application/json')

def default(obj):
    """Default JSON serializer."""
    if isinstance(obj, datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    return int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)

def lookup_item(request):
	items = []
	if request.method == "GET":
		if request.GET.has_key(u'category'):
			cat_id = request.GET[u'category']
			page = int(request.GET[u'page']) if request.GET.has_key(u'page') else 1
			paginator = Paginator(get_items(cat_id, request.user), settings.PAGE_SIZE)
			for item in paginator.page(page):
				model_dict = model_to_dict(item)
				model_dict['entry_title'] = item.rss_entry.title 
				m = re.search("(https?://[^/]+)", item.rss_entry.url)
				model_dict['main_link'] = m.group(0)
				items.append(model_dict)
			result = {'num_pages':paginator.num_pages, 'items': items}
			json = simplejson.dumps(result, default=default)
			return HttpResponse(json, mimetype='application/json')
	return HttpResponse({'error': 'Category is not set'}, mimetype='application/json')
def get_items(cat_id, user):
	if cat_id == '-1':
		return Item.objects.filter(visited = False).order_by('-pub_date')
	else:
		return Item.objects.filter(rss_entry__category__id = cat_id, visited = False).order_by('-pub_date')
