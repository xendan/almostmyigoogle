from celery.task import periodic_task
from celery.schedules import crontab
import datetime
from rss_feed.models import RssEntry, Item
import urllib2
import traceback
from pytz import timezone
import pytz
from dateutil import parser
from dateutil.tz import tzoffset
from datetime import datetime, timedelta
import feedparser

def now_zone():
	return datetime.utcnow().replace(tzinfo = pytz.utc)

@periodic_task(ignore_result=True, run_every=crontab(hour=12, minute=0))
def update_feeds():
	for entry in RssEntry.objects.all():
		if not entry.updated or (now_zone() - entry.updated) > timedelta(hours = 1):
			#?? more pythonic: http://stackoverflow.com/questions/6586040/django-how-to-get-the-0th-item-from-a-possibly-empty-list
			try:
				last_date = Item.objects.filter(rss_entry = entry).order_by('-pub_date')[0].pub_date
			except IndexError:
				last_date = datetime(2000, 1, 1).replace(tzinfo = pytz.utc)
			parse_items(entry, last_date)		

def parse_items(rss_entry, last_date):
	for entry in feedparser.parse(rss_entry.url)['entries']: 
		parse_entry(entry, last_date, rss_entry)
	rss_entry.updated = now_zone() 
	rss_entry.save()

def parse_entry(entry,  last_date, rss_entry):
	item = Item()
	item_time = parser.parse(entry['updated']).replace(tzinfo = pytz.utc)
	if (item_time - last_date).total_seconds() > 0:
		item = Item()
		item.title = entry['title'].encode('utf-8')
		if entry['links']:	
			item.link = entry['links'][0]['href']
		else:
			item.link = ''
		item.pub_date = item_time 
		item.rss_entry = rss_entry
		item.content = entry['summary'].encode('utf-8')
		item.save()	

