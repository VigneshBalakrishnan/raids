from django.forms import ModelForm
from .models import Help, Comment

class AddHelpForm(ModelForm):
	class Meta:
		model = Help
		fields = ('title', 'description', 'urgent')

class AddCommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)

