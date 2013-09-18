from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import redirect
from rss_feed.models import RssEntry, Category
from rss_feed.forms import ImportForm
from django.shortcuts import render_to_response
import xml.etree.cElementTree as etree
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.conf  import settings

@csrf_protect
def index(request):
	if not request.user.is_authenticated():
		return redirect('/openid/login/') 
	if request.method == 'POST':
		form = ImportForm(request.POST, request.FILES)
		if form.is_valid():
			handel_uploaded_file(request.FILES['docfile'], request.user)
	else:
		form = ImportForm()
	categories = build_categories(request.user)
	temp_vars = {'form' : form, 'categories':categories, 'page_size':settings.PAGE_SIZE}	
	return	render_to_response('main.html', temp_vars , context_instance=RequestContext(request))
def build_categories(user):
	categories = Category.objects.filter(user = user)
	return categories.values('title', 'id')
	#for idx,value in enumerate(values):
	#value['feeds'] = categories[idx].feeds.values('title', 'text', 'url')

def handel_uploaded_file(docfile, user):	
	#TODO:validation
	content = docfile.read()
	xml_doc_tree = etree.XML(content)
	node = xml_doc_tree.getchildren()[1]
	others = Category(text="others", title="others", user=user)
	others.save()
	for outline in node:
		if 'xmlUrl' in  outline.attrib:
			create_rss_entry(outline.attrib, user, others)
		else:
			category = create_outline(Category(), user, outline.attrib);
			category.save()
			for sub_outline in outline:
				create_rss_entry(sub_outline.attrib, user, category)

def create_outline(outline, user, attrib):
	outline.text = attrib['text']
	outline.title = attrib['title']
	outline.user = user
	return outline

def create_rss_entry(attrib, user, category):
	entry = create_outline(RssEntry(url=attrib['xmlUrl']), user, attrib)
	entry.category = category
	entry.save()
