from django.db import models
from accounts.models import User

class Help(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=255)
	description = models.TextField()
	urgent = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

class Comment(models.Model):
	user = models.ForeignKey(User)
	help = models.ForeignKey(Help)
	body = models.CharField(max_length=500)
	pub_date = models.DateTimeField('date commented')

	