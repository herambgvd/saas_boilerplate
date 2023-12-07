from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404

from tenantApps.clarify.marketplace.forms import AssetForm
from tenantApps.clarify.marketplace.models import Asset
from tenantApps.common.branch.models import Branch
from tenantApps.common.branch.models import ConfigManager


#### Branch View #####
@login_required(login_url='account_login')
def branch_list(request):
	branchAll = Branch.objects.all().order_by('-created_at')
	context = {'branchAll': branchAll}
	return render(request, 'tenant/clarify/branch/base/branch.html', context)


@login_required(login_url='account_login')
def branch_detail(request, id):
	branch_instance = get_object_or_404(Branch, pk=id)
	assets_instance = Asset.objects.filter(selectBranch=id).order_by('-created_at')
	context = {'assets_instance': assets_instance, 'branch_instance': branch_instance}
	return render(request, 'tenant/clarify/branch/base/branchDetail.html', context)


########### Assets Views End ##############

@login_required(login_url='account_login')
def branch_asset_create(request, branchId):
	if request.method == 'POST':
		form = AssetForm(request.POST)
		if form.is_valid():
			try:
				# Extract the tagModel (Marketplace instances) from the form
				tagModel = form.cleaned_data.get('tagModel')

				# Create the asset using the custom manager's method
				Asset.objects.create_asset(
					name=form.cleaned_data.get('name'),
					liveUrl=form.cleaned_data.get('liveUrl'),
					selectBranch=Branch.objects.get(id=branchId),
					tagModel=tagModel
				)
				messages.success(request, "Live Created Successfully")
				return redirect('Marketplace:branch_detail', id=branchId)
			except ValidationError as e:
				# Extract the actual message from the list and add to Django's messages
				error_message = e.messages[0] if e.messages else str(e)
				messages.error(request, error_message)
	else:
		form = AssetForm()
	context = {'branchId': branchId, 'form': form}
	return render(request, 'tenant/clarify/branch/assets/asset_create.html', context)


@login_required(login_url='account_login')
def branch_asset_update(request, branchId, assetId):
	asset_instance = get_object_or_404(Asset, pk=assetId)
	initial_tagModel = set(asset_instance.tagModel.all())  # Get the initial set of Marketplaces
	if request.method == 'POST':
		form = AssetForm(request.POST, instance=asset_instance)
		if form.is_valid():
			new_tagModel = set(form.cleaned_data.get('tagModel'))  # Get the new set of Marketplaces
			# Determine which Marketplaces were added or removed
			added_marketplaces = new_tagModel - initial_tagModel
			removed_marketplaces = initial_tagModel - new_tagModel

			try:
				# Check and update usage for added Marketplaces
				for marketplace in added_marketplaces:
					if marketplace.no_of_used >= marketplace.no_of_usage_allowed:
						raise ValidationError(f"Usage limit for {marketplace.name} has been exceeded.")
					marketplace.no_of_used += 1
					marketplace.save()

				# Update usage for removed Marketplaces
				for marketplace in removed_marketplaces:
					marketplace.no_of_used -= 1
					marketplace.save()

				form.save()
				messages.success(request, "Live Updated Successfully")
				return redirect('Marketplace:branch_detail', id=branchId)
			except ValidationError as e:
				error_message = e.messages[0] if e.messages else str(e)
				messages.error(request, error_message)
	else:
		form = AssetForm(instance=asset_instance)
	context = {'form': form, 'asset_instance': asset_instance, 'branchId': branchId}
	return render(request, 'tenant/clarify/branch/assets/asset_update.html', context)


@login_required(login_url='account_login')
def branch_asset_delete(request, branchId, assetId):
	asset_instance = get_object_or_404(Asset, pk=assetId)
	associated_marketplaces = asset_instance.tagModel.all()  # Get the associated Marketplaces

	if request.method == 'POST':
		# Decrement the no_of_used field for each associated Marketplace
		for marketplace in associated_marketplaces:
			marketplace.no_of_used -= 1
			marketplace.save()
		# Delete the database record
		asset_instance.delete()
		messages.success(request, "URL Deleted Successfully")
		return redirect('Marketplace:branch_detail', id=branchId)
	context = {'asset_instance': asset_instance, 'branchId': branchId}
	return render(request,
	              'tenant/clarify/branch/assets/asset_confirm.html', context)


# Branch Inference
@login_required(login_url='account_login')
def branch_live_inferences(request, branchId, assetId):
	serverInfo = ConfigManager.objects.get(configName="ANALYSE")
	streamingInfo = ConfigManager.objects.get(configName="STREAMING")
	asset_info = get_object_or_404(Asset, pk=assetId)
	tenant_request = request.tenant.name
	context = {'branchId': branchId, 'asset_info': asset_info, 'tenant_request': tenant_request,
	           'serverInfo': serverInfo.configValue,
	           'streamingInfo': streamingInfo.configValue}
	return render(request, 'tenant/clarify/branch/inference/liveInference.html', context)
