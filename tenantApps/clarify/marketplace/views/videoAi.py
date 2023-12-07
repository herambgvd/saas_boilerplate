from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from tenantApps.clarify.marketplace.forms import MarketplaceFilesForm
from tenantApps.clarify.marketplace.models import Marketplace, MarketplaceFiles
from tenantApps.clarify.marketplace.utils.delete_file import delete_file
from tenantApps.common.branch.models import ConfigManager


##### Marketplace Views #######
@login_required(login_url='account_login')
def marketplace(request):
	modelList = Marketplace.objects.all()
	context = {'modelList': modelList}
	return render(request, 'tenant/clarify/marketplace/base/marketplaceList.html', context)


##### Marketplace File Manager Views #######
@login_required(login_url='account_login')
def marketplace_files_list(request, modelId):
	modelName = Marketplace.objects.get(id=modelId)
	files = MarketplaceFiles.objects.filter(selectMarketplace=modelId)
	context = {'files': files, 'modelId': modelId, 'modelName': modelName}
	return render(request, 'tenant/clarify/marketplace/videoManager/modelFileManager.html', context)


@login_required(login_url='account_login')
def marketplace_files_create(request, modelId):
	if request.method == 'POST':
		form = MarketplaceFilesForm(request.POST, request.FILES)
		if form.is_valid():
			marketplace_file = form.save(commit=False)
			# File Size is calculated
			file_size_MB = marketplace_file.fileName.size / (1024 * 1024)
			marketplace_file.fileSize = file_size_MB
			# Marketplace Selections
			marketplace_file.selectMarketplace = Marketplace.objects.get(id=modelId)
			marketplace_file.tenant_name = str(request.tenant.schema_name)
			marketplace_file.save()
			messages.success(request, "File Uploaded Successfully")
			return redirect('Marketplace:marketplace_files_list', modelId=modelId)
	else:
		form = MarketplaceFilesForm()
	context = {'form': form, 'modelId': modelId}
	return render(request, 'tenant/clarify/marketplace/videoManager/partial/marketplace_files_form.html', context)


@login_required(login_url='account_login')
def marketplace_files_update(request, modelId, pk):
	file_instance = get_object_or_404(MarketplaceFiles, pk=pk)
	if request.method == 'POST':
		form = MarketplaceFilesForm(request.POST, request.FILES, instance=file_instance)
		if form.is_valid():
			# If the user uploaded a new file, delete the old one
			if 'fileName' in request.FILES:
				delete_file(file_instance.fileName.path)
			form.save()
			return redirect('Marketplace:marketplace_files_list')
	else:
		form = MarketplaceFilesForm(instance=file_instance)
	context = {'form': form, 'modelId': modelId}
	return render(request, 'tenant/clarify/marketplace/videoManager/partial/marketplace_files_form.html', context)


@login_required(login_url='account_login')
def marketplace_files_delete(request, modelId, pk):
	file_instance = get_object_or_404(MarketplaceFiles, pk=pk)
	if request.method == 'POST':
		# Delete the database record
		file_instance.delete()
		messages.success(request, "File Deleted Successfully")
		return redirect('Marketplace:marketplace_files_list', modelId=modelId)
	context = {'object': file_instance, 'modelId': modelId}
	return render(request, 'tenant/clarify/marketplace/videoManager/partial/marketplace_files_confirm.html', context)


##### End Marketplace File Manager Views #######
@login_required(login_url='account_login')
def streamingInference(request, modelId, fileId):
	file = MarketplaceFiles.objects.get(id=fileId)
	aiServer = ConfigManager.objects.get(configName="ANALYSE")
	apiServer = aiServer.configValue + 'video/get-analysed-video/'
	print(apiServer)
	context = {'topic': file.name.replace(" ", "-"), 'file': file, 'apiServer': apiServer,
	           'modelId': file.selectMarketplace.id}
	return render(request, 'tenant/clarify/marketplace/videoManager/videoInference.html', context)
