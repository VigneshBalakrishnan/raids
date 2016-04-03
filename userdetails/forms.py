from django import forms
from models import UserProfile

class UserProfileForm(forms.ModelForm):
	
	class Meta:
		model =  UserProfile
		fields = ('name','age','occupation','number','location','profile_pic','show_personal_details')