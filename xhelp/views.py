from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, send_mass_mail
from django.db.models import Q
from accounts.models import User
from django.utils import timezone
from .models import Help, Comment
from contactus.models import Connect
from userdetails.models import UserProfile
from .forms import  AddHelpForm, AddCommentForm
from contactus.forms import ConnectForm

@login_required(login_url='/')
def help_list(request):
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	profile = UserProfile.objects.all()
	help = Help.objects.all()

	args = {}
	args.update(csrf(request))
	args['help'] = help
	args['profile'] = profile
	args['profiles'] = profile_name
	return render_to_response('help/post_list.html',args,context_instance=RequestContext(request))

@login_required(login_url='/')
def help_detail(request,pk):
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	help = Help.objects.get(id=pk)
	profile = UserProfile.objects.all()
	comment = Comment.objects.all()
	u = User.objects.get(email = request.user.email)
	h = Help.objects.get(id=pk)
	context =  RequestContext(request)
	if request.POST.get("comment"):
		f = AddCommentForm(request.POST)
		if f.is_valid():
			c = f.save(commit = False)
			c.pub_date = timezone.now()
			c.user = u
			c.help = h
			c.save()
			return HttpResponseRedirect('/help_detail/%s' % pk) 
	else:
		f = AddCommentForm

	user1 = User.objects.get(email = request.user.email)
	user2 = Help.objects.get(id = pk)

	if request.POST.get("connect"):
		connectform = ConnectForm(request.POST)
		if connectform.is_valid():
			c = connectform.save(commit = False)
			c.send = user1
			c.receive = user2.user
			c.save()
			url = reverse('help_detail', kwargs={ 'pk': user2.id })
			return HttpResponseRedirect(url)
			
	else:
		connectform = ConnectForm()
	args = {}
	args.update(csrf(request))
	args = {'help':help,'comment':comment,'profile':profile,'form':f,'connectform':connectform,'profiles': profile_name
	}
	return render_to_response('help/post_detail.html',args,context)

@login_required(login_url='/')
def add_help(request):
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	u_list = User.objects.all()
	u = User.objects.get(email = request.user.email)
	context =  RequestContext(request)
	if request.method == "POST":
	    helpform = AddHelpForm(request.POST)
	    if helpform.is_valid():
	        save_it = helpform.save(commit = False)
	        save_it.user = u
	        save_it.save()
	        
	        for i in u_list:
				subject = "Help added"
				message = "New help is been added have a look on it."
				from_email = settings.EMAIL_HOST_USER
				to_list = [i.email]
				send_mail(subject,message,from_email,to_list,fail_silently=True)
	        return HttpResponseRedirect('/help/list/')
	else:
		helpform = AddHelpForm()

	args = {}
	args.update(csrf(request))
	args = {'helpform':helpform,'profiles': profile_name}
	return render_to_response("help/post.html",args,context)

		

		       
 





