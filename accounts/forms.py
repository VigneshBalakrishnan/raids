from django import forms
from models import User
from django.utils.translation import ugettext_lazy as _

class SignupForm(forms.Form):
    email 			= forms.EmailField(required=True)
    password 		= forms.CharField(widget=forms.PasswordInput(render_value=False))
    re_password 	= forms.CharField(widget=forms.PasswordInput(render_value=False))
    class Meta:
        model = User
    
    def clean_email(self):
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("The email already exists. Please try another one."))

    def clean(self):
        if 'password' in self.cleaned_data and 're_password' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['re_password']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
