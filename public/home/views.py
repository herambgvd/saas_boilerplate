from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from tenant.models import Client, Domain
from .forms import TenantForm, DomainForm


@login_required(login_url='account_login')
def dashboard(request):
	return render(request, 'public/dashboard/index.html')


######### Tenant CRUD #########
@login_required(login_url='account_login')
def tenantList(request):
	allTenants = Client.objects.all()
	context = {'allTenants': allTenants}
	return render(request, 'public/tenant/tenantManagement/index.html', context)


@login_required(login_url='account_login')
def createTenant(request):
	form = TenantForm()
	if request.method == "POST":
		form = TenantForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Tenant Added Successfully")
			return redirect('publicHome:tenantList')
	context = {'form': form}
	return render(request, 'public/tenant/tenantManagement/createTenant.html', context)


@login_required(login_url='account_login')
def deleteTenant(request, tenantId):
	tenantDelete = Client.objects.get(id=tenantId)
	tenantDelete.delete()
	messages.success(request, 'Tenant Deleted Successfully')
	return redirect('publicHome:tenantList')


######### Domain CRUD #########
@login_required(login_url='publicLogin')
def domainList(request):
	allDomains = Domain.objects.all()
	context = {'allDomains': allDomains}
	return render(request, 'public/tenant/domainManagement/index.html', context)


@login_required(login_url='account_login')
def createDomain(request):
	form = DomainForm()
	context = {'form': form}
	return render(request, 'public/tenant/domainManagement/createDomain.html', context)


def custom_404(request, exception):
	return render(request, 'tenant/common/404.html', {}, status=404)


def custom_500(request):
	return render(request, 'tenant/common/500.html', {}, status=500)
