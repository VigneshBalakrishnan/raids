from django import forms
from models import Connect

class ConnectForm(forms.ModelForm):
	class Meta:
		model = Connect
		fields = ('msg',)