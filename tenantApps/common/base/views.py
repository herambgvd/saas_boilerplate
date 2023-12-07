from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tenantApps.neubit.infrastructure.models import IotDevice


# Create your views here.
@login_required(login_url='account_login')
def dashboard(request):
	return render(request, 'tenant/common/dashboard/iocDashboard.html')


@login_required(login_url='account_login')
def aiDashboard(request):
	# aiServer = settings.CLARIFY_BASE_URL
	aiServer = "122.76.34.21"
	tenant_request = request.tenant.name
	context = {'aiServer': aiServer, 'tenant_request': tenant_request}
	return render(request, 'tenant/common/dashboard/aiDashboard.html', context)


@login_required(login_url='account_login')
def bmsDashboard(request):
	return render(request, 'tenant/common/dashboard/bmsDashboard.html')


@login_required(login_url='account_login')
def iotDashboard(request):
	sensor_groups = {}
	for sensor in IotDevice.sensorChoices:
		sensor_type = sensor[0]
		devices = IotDevice.objects.filter(selectSensor=sensor_type)
		sensor_groups[sensor_type] = devices

	context = {'sensor_groups': sensor_groups}
	return render(request, 'tenant/common/dashboard/iotDashboard.html', context)


@login_required(login_url='account_login')
def iotBranchDashboard(request, branchId):
	sensor_groups = {}
	for sensor in IotDevice.sensorChoices:
		sensor_type = sensor[0]
		devices = IotDevice.objects.filter(selectBranch=branchId).filter(selectSensor=sensor_type)
		sensor_groups[sensor_type] = devices
	context = {'sensor_groups': sensor_groups}
	return render(request, 'tenant/common/dashboard/iot/iotBranchDashboard.html', context)


def custom_404(request, exception):
	return render(request, 'tenant/common/404.html', {}, status=404)


def custom_500(request):
	return render(request, 'tenant/common/500.html', {}, status=500)
