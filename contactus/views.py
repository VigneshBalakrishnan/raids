from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.db.models import Q
from django.conf import settings
from accounts.models import User
from xhelp.models import Help
from models import Connect
from userdetails.models import UserProfile
from forms import ConnectForm

@login_required(login_url='/')
def contactus(request):
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	if request.GET.get('name'):
		name = request.GET.get('name')
	if request.GET.get('feedback'):
		feedback = request.GET.get('feedback')
		string = "User:"+"\n"+"\t"+str(request.user.email)+"\n"+"\n"+"Feedback:"+"\n"+"\t"+str(feedback)
		subject = name
		message = string
		from_email = request.user.email
		to_list = [settings.EMAIL_HOST_USER]

		send_mail(subject,message,from_email,to_list,fail_silently=True)
		return HttpResponseRedirect('/dashboard/')
	args = {'profiles': profile_name}	
	return render_to_response("contact/contact.html",args,context_instance=RequestContext(request))

@login_required(login_url='/')
def connect(request,pk):
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	user1 = User.objects.get(email = request.user.email)
	user2 = Help.objects.get(id = pk)
	if request.method == "POST":
		form = ConnectForm(request.POST)
		if form.is_valid():
			c = form.save(commit = False)
			c.send = user1
			c.receive = user2.user
			c.save()
			url = reverse('help_detail', kwargs={ 'pk': user2.id })
			return HttpResponseRedirect(url)
			
	else:
		form = ConnectForm()
	args={}
	args.update(csrf(request))
	args = {'profile': profile_name,'form':form}
	return render_to_response('contact/connect.html',args)

@login_required(login_url='/')
def connect_list(request):
	user = User.objects.get(email = request.user.email)
	profile = UserProfile.objects.all()
	profile_name = UserProfile.objects.get(user = user)
	msgs = Connect.objects.all()
	li = []
	s = []
	la = []
	d = []
	for i in msgs:
		li.append(i.receive)
	for i in li:
		if i not in s:
			s.append(i)
	
	for i in msgs:
		if i.receive == user:
				la.append(i.send)
	for i in la:
		if i not in d:
			d.append(i)

	args={'msgs':msgs,'user':user,'profile':profile,'s':s,'d':d,'profiles': profile_name}
	return render_to_response('contact/connect_list.html',args)

@login_required(login_url='/')
def connect_message(request,pk):
	user = User.objects.get(email = request.user.email)
	sender = User.objects.get(id = pk)
	msgs = Connect.objects.all()
	profile = UserProfile.objects.all()
	profile_name = UserProfile.objects.get(user = user)

	if request.POST.get("send"):
		form = ConnectForm(request.POST)
		if form.is_valid():
			c = form.save(commit = False)
			c.send = user
			c.receive = sender
			c.save()
			
			return HttpResponseRedirect('/messages/%s' % pk)
			
	else:
		form = ConnectForm()
	args={}
	args.update(csrf(request))
	args={'msgs':msgs,'user':user,'profile':profile,'s_id':pk,'sender':sender,'form':form,'profiles': profile_name}
	return render_to_response('contact/connect_message.html',args,context_instance=RequestContext(request))

@login_required(login_url='/')
def invite(request):
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	if request.GET.get('email'):
		email = request.GET.get('email')
		send = '127.0.0.1:8000'
		subject = 'Invitation for Helpdesk'
		message = 'From :'+'\n'+'\t'+str(request.user.email)+'\n'+'Your friend has joined in this forum .He likes you to take part in it.If you are willing click the below link.'+'\n'+str(send)
		from_email = request.user.email
		to_list = [email]

		send_mail(subject,message,from_email,to_list,fail_silently=True)
		return HttpResponseRedirect('/dashboard/')
	args = {'profiles': profile_name}	
	return render_to_response("contact/invite.html",args,context_instance=RequestContext(request))








