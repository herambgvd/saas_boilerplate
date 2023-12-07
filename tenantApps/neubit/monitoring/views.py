from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tenantApps.common.branch.models import Branch
from tenantApps.neubit.infrastructure.models import CameraTag, CCTV, NVR


# Create your views here.
@login_required(login_url="account_login")
def branchList(request):
	allBranch = Branch.objects.only('branchName', 'branchCode')
	context = {'allBranch': allBranch}
	return render(request, 'tenant/neubit/monitoring/branchStreaming/index.html', context)


@login_required(login_url="account_login")
def branchLiveStream(request, id):
	streamBranch = Branch.objects.get(id=id)
	branchCamera = NVR.objects.prefetch_related('nvr_cctv').filter(selectBranch=id)
	context = {'streamBranch': streamBranch, 'branchCamera': branchCamera}
	return render(request, 'tenant/neubit/monitoring/branchStreaming/streaming.html', context)


@login_required(login_url="account_login")
def tagList(request):
	allTag = CameraTag.objects.all()
	context = {'allTag': allTag}
	return render(request, 'tenant/neubit/monitoring/tagStreaming/index.html', context)


@login_required(login_url="account_login")
def dynamicTagStreaming(request, id):
	allCamera = CCTV.objects.only('slugName', 'hlsLink')
	context = {'allCamera': allCamera}
	return render(request, 'tenant/neubit/monitoring/tagStreaming/streaming.html', context)
