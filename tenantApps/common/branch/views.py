import os

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from tenantApps.clarify.marketplace.models import Marketplace
from .forms import BranchForm
from .models import Branch


# Create your views here.
def LatLongCheck(form):
	form.save()
	api_key = os.environ.get('GOOGLE_MAP_KEY')
	address = " ".join([form.cleaned_data['branchAddress']])
	api_response = requests.get(
		'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key)).json()
	lat = api_response['results'][0]['geometry']['location']['lat']
	long = api_response['results'][0]['geometry']['location']['lng']
	Branch.objects.filter(branchCode=form.cleaned_data['branchCode']).update(
		latitude=lat, longitude=long)


@login_required(login_url='account_login')
def branch_list(request):
	branchAll = Branch.objects.all().order_by('-created_at')
	context = {'branchAll': branchAll}
	return render(request, 'tenant/common/branch/base/branch.html', context)


@login_required(login_url='account_login')
def branch_create(request):
	if request.method == 'POST':
		form = BranchForm(request.POST)
		if form.is_valid():
			LatLongCheck(form)
			messages.success(request, "Branch Created Successfully")
			return redirect('Branch:branch')
	else:
		form = BranchForm()
	context = {'form': form}
	return render(request, 'tenant/common/branch/base/partial/branch_create.html', context)


@login_required(login_url='account_login')
def branch_update(request, id):
	branch_instance = get_object_or_404(Branch, pk=id)
	if request.method == 'POST':
		form = BranchForm(request.POST, instance=branch_instance)
		if form.is_valid():
			LatLongCheck(form)
			messages.success(request, "Branch Updated Successfully")
			return redirect('Branch:branch')
	else:
		form = BranchForm(instance=branch_instance)
	context = {'form': form, 'branch_instance': branch_instance}
	return render(request, 'tenant/common/branch/base/partial/branch_update.html', context)


@login_required(login_url='account_login')
def branch_delete(request, id):
	branch_instance = get_object_or_404(Branch, pk=id)
	if request.method == 'POST':
		# Delete the database record
		branch_instance.delete()
		messages.success(request, "Branch Deleted Successfully")
		return redirect('Branch:branch')
	context = {'object': branch_instance}
	return render(request, 'tenant/common/branch/base/partial/branch_confirm.html', context)


# @login_required(login_url='account_login')
# def branch_detail(request, id):
# 	branch_instance = get_object_or_404(Branch, pk=id)
# 	assets_instance = Asset.objects.filter(selectBranch=id).order_by('-created_at')
# 	context = {'assets_instance': assets_instance, 'branch_instance': branch_instance}
# 	return render(request, 'tenant/branch/base/branchDetail.html', context)

# License Settings
@login_required(login_url='account_login')
def licenseSetting(request):
	modelLicense = Marketplace.objects.all()
	context = {'modelLicense': modelLicense}
	return render(request, 'tenant/common/branch/license/index.html', context)


# Camera Tags
