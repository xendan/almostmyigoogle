from django.db import models
from django.contrib.auth.models import User

class Outline(models.Model):
	user = models.ForeignKey(User, editable = False)
	text = models.CharField(max_length = 300)
	title = models.CharField(max_length = 300)
	class Meta:
		abstract = True

class Category(Outline):
	pass

class RssEntry(Outline):
	url = models.CharField(max_length = 2000) 
	get_from_site = models.BooleanField(default = False)
	category = models.ForeignKey(Category, related_name='feeds')
	updated = models.DateTimeField(default=None, blank=True, null=True)

class Item(models.Model):
	title = models.CharField(max_length = 1000)
	link = models.CharField(max_length = 1500)
	content = models.TextField("content")
	pub_date = models.DateTimeField()
	visited = models.BooleanField(default = False)
	rss_entry = models.ForeignKey(RssEntry, related_name='items')
