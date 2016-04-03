from django.db import models
from django.core.validators import MaxValueValidator
from accounts.models import User
from time import time

def get_upload(instance,filename):
	return "media/%s_%s" % (str(time()).replace('.','_'),filename)

class UserProfile(models.Model):
	user                  = models.OneToOneField(User)
	name                  = models.CharField(max_length=120,blank=False)
	age 				  = models.IntegerField(null=True,max_length=3,validators=[MaxValueValidator(999)])
	occupation 			  = models.CharField(max_length=120,blank=True)
	number 				  = models.IntegerField(null=True,max_length=10,validators=[MaxValueValidator(9999999999)])
	email_id 			  = models.EmailField()
	location 			  = models.CharField(max_length=120,blank=True)
	profile_pic 		  = models.FileField(upload_to=get_upload)
	show_personal_details = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])	



