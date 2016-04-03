from django import forms
from models import UserSales, Comments

class UserSaleForm(forms.ModelForm):
	
	class Meta:
		model =  UserSales
		fields = ('title','description','pic')

class AddCommentForm(forms.ModelForm):
	class Meta:
		model = Comments
		fields = ('body',)