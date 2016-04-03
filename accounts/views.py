from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import hashlib, datetime, random
from django.utils import timezone
from forms import SignupForm
from models import User, UserConfirmation
from contactus.models import Connect
from userdetails.models import UserProfile
from contactus.forms import ConnectForm

def signin(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('accounts/login.html',c)

# def sign(request):
#     c = {}
#     c.update(csrf(request))
#     return render_to_response('accounts/signup.html',c)

# def log(request):
#     c = {}
#     c.update(csrf(request))
#     return render_to_response('accounts/login.html',c)

def auth_view(request):
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    user = auth.authenticate(email=email,password=password)
    if user is not None:
        if user.is_active:
            auth.login(request,user)
            user = User.objects.get(email = request.user.email)
            try:
                UserProfile.objects.get(user = user)
                return HttpResponseRedirect('/dashboard/')
            except:
                return HttpResponseRedirect('/profile/')
        else:
            return HttpResponseRedirect('/not_active/')
    return HttpResponseRedirect('/invalid/')

def not_active(request):
    return render_to_response('accounts/not_active.html')

@login_required(login_url='/')
def dashboard(request): 
    user = User.objects.get(email = request.user.email)
    profile_name = UserProfile.objects.get(user = user)
    args = {'profiles': profile_name}
    return render_to_response('accounts/dashboard.html',args)

def invalid(request):
    return render_to_response('accounts/invalid.html')

def signout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user( 
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            )
            
            email           = form.cleaned_data['email']
            salt            = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key  = hashlib.sha1(salt+email).hexdigest()            
            key_expires     = datetime.datetime.today() + datetime.timedelta(2)

            #get email
            user            = User.objects.get(email=email)

            # Create and save user profile                                                                                                                                  
            new_profile     = UserConfirmation(user=user, activation_key=activation_key, key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject   = 'Account confirmation'
            email_body      = "Hey %s, thanks for signing up. To activate your account, click this link within 48hours http://127.0.0.1:8000/confirm/%s" % (email, activation_key)
            from_email      = settings.EMAIL_HOST_USER
            send_mail(email_subject, email_body,from_email,[email], fail_silently=True)
            
            return HttpResponseRedirect('/registered/')
    else:

        form= SignupForm()
    return render(request,'accounts/signup.html',{'form':form},context_instance=RequestContext(request))



def register_confirm(request, activation_key):
    if request.user.is_authenticated():
        HttpResponseRedirect('/dashboard/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserConfirmation , activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('accounts/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('accounts/confirm.html')


def register_success(request):
    return render_to_response('accounts/registered.html')

 