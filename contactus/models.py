from django.db import models
from accounts.models import User
from xhelp.models import Help

class Connect(models.Model):
	send = models.ForeignKey(User, related_name="sender")
	receive = models.ForeignKey(User, related_name="receiver")
	msg = models.CharField(max_length=500)

	def __unicode__(self):
		return self.msg
