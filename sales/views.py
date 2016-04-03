from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.utils import timezone
from django.core.urlresolvers import reverse
from accounts.models import User
from userdetails.models import UserProfile
from .models import UserSales, Comments
from forms import UserSaleForm, AddCommentForm
from contactus.forms import ConnectForm

@login_required(login_url='/')
def sales(request):
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	if request.method == 'POST':
		u = User.objects.get(email = request.user.email)
		form = UserSaleForm(request.POST,request.FILES)
		if form.is_valid():
			save_it = form.save(commit = False)
			save_it.user = u
			save_it.save()
	        
			return HttpResponseRedirect('/sales_detail/')

	else:
		user = request.user
		profile = user.profile
		form = UserSaleForm()

	args = {}
	args.update(csrf(request))
	args = {'form':form,'profiles': profile_name}
	return render_to_response('sales/sale.html', args, context_instance=RequestContext(request))

@login_required(login_url='/')
def sales_detail(request):
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	salesprofile = UserSales.objects.all()
	profile = UserProfile.objects.all()
	args = {}
	args.update(csrf(request))
	args = {'salesprofile':salesprofile,'profiles': profile_name,'profile':profile}
	return render_to_response('sales/saledisp.html', args, context_instance=RequestContext(request))

@login_required(login_url='/')
def sale_detail(request,pk):
	user = User.objects.get(email = request.user.email)
	profile_name = UserProfile.objects.get(user = user)
	sale = UserSales.objects.get(id=pk)
	profile = UserProfile.objects.all()
	comment = Comments.objects.all()

	if request.POST.get("comment"):
		f = AddCommentForm(request.POST)
		if f.is_valid():
			c = f.save(commit = False)
			c.pub_date = timezone.now()
			c.user = user
			c.sale = sale
			c.save()

			return HttpResponseRedirect('/sale_detail/%s' % pk) 

	else:
		f = AddCommentForm()

	user1 = User.objects.get(email = request.user.email)
	user2 = UserSales.objects.get(id = pk)

	if request.POST.get("connect"):
		connectform = ConnectForm(request.POST)
		if connectform.is_valid():
			c = connectform.save(commit = False)
			c.send = user1
			c.receive = user2.user
			c.save()
			url = reverse('sale_detail', kwargs={ 'pk': user2.id })
			return HttpResponseRedirect(url)
			
	else:
		connectform = ConnectForm()


	args = {'sale':sale,'comment':comment,'profile':profile,'profiles': profile_name,'form':f,'connectform':connectform}
	return render_to_response('sales/sale_detail.html',args,context_instance=RequestContext(request))
