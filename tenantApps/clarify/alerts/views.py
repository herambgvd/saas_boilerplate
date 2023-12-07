from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tenantApps.clarify.marketplace.models import Asset


# Create your views here.
@login_required(login_url='account_login')
def inferenceList(request):
	inference_stream = Asset.objects.all()
	context = {'inferenceStream': inference_stream}
	return render(request, 'tenant/clarify/alert/inferenceList.html', context)


@login_required(login_url='account_login')
def inferenceAlertList(request, id):
	aiServer = settings.CLARIFY_BASE_URL
	tenantRequest = request.tenant.name
	assetName = Asset.objects.get(id=id)
	context = {'tenantRequest': tenantRequest, 'assetName': assetName, 'aiServer': aiServer}
	return render(request, 'tenant/clarify/alert/inferenceAlertList.html', context)
