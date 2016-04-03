from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from accounts.models import User
from models import UserProfile
from forms import UserProfileForm

@login_required(login_url='/')
def user_profile(request):
	user = User.objects.get(email = request.user.email)
	try:
		profiles = UserProfile.objects.get(user = user)
	except:
		profiles = ""
	if request.method == 'POST':
		email = request.user.email
		form = UserProfileForm(request.POST,request.FILES,instance=request.user.profile)
		if form.is_valid():
			save_it = form.save(commit = False)
			save_it.email_id = email
			save_it.save()

			return HttpResponseRedirect('/profile/')

	else:
		user = request.user
		profile = user.profile
		form = UserProfileForm(instance=profile)

	args = {}
	args.update(csrf(request))
	args['form'] = form
	args['profiles'] = profiles
	try:
		profile_name = UserProfile.objects.get(user = user)
		args['email'] = profile_name.name
	except:
		args['email'] = request.user.email
	return render_to_response('profile/profile.html', args,context_instance=RequestContext(request))

@login_required(login_url='/')
def profile(request):
	profile = UserProfile.objects.get(user=request.user)
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	args = {}
	args.update(csrf(request))
	args['profile'] = profile
	args['user'] = user
	args['email'] = profile_name.name
	return render_to_response('profile/profiledisp.html', args)

@login_required(login_url='/')
def profile_disp(request,pk):
	profile = UserProfile.objects.get(user_id=pk)
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	args = {}
	args.update(csrf(request))
	args['profile'] = profile
	args['email'] = profile_name.name
	return render_to_response('profile/profiledisp.html',args)




 

