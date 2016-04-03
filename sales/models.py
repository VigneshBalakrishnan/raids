from django.db import models
from accounts.models import User
from time import time

def get_upload(instance,filename):
	return "media/%s_%s" % (str(time()).replace('.','_'),filename)

class UserSales(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=255)
	description = models.TextField()
	pic 		 = models.FileField(upload_to=get_upload)
	
	def __unicode__(self):
		return self.user

class Comments(models.Model):
	user = models.ForeignKey(User)
	sale = models.ForeignKey(UserSales)
	body = models.CharField(max_length=500)
	pub_date = models.DateTimeField('date commented')

	def __unicode__(self):
		return self.help



