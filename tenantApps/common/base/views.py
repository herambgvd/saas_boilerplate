from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tenantApps.neubit.infrastructure.models import IotDevice, IotGateway


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
	gatewayCount = IotGateway.objects.all().count()
	sensorCount = IotDevice.objects.all().count()
	sensor_groups = {}
	for sensor in IotDevice.sensorChoices:
		sensor_type = sensor[0]
		devices = IotDevice.objects.filter(selectSensor=sensor_type)
		sensor_groups[sensor_type] = devices
	print(sensor_groups)
	context = {'sensor_groups': sensor_groups, 'gatewayCount': gatewayCount, 'sensorCount': sensorCount}
	return render(request, 'tenant/common/dashboard/iotDashboard.html', context)


@login_required(login_url='account_login')
def iotBranchDashboard(request, branchId):
	sensor_groups = {}
	for sensor in IotDevice.sensorChoices:
		sensor_type = sensor[0]
		devices = IotDevice.objects.filter(selectBranch=branchId).filter(selectSensor=sensor_type)
		sensor_groups[sensor_type] = devices
	# print(sensor_groups)

	odorSensor = IotDevice.objects.filter(selectBranch=branchId).filter(name__startswith="GS301")
	# Attach the latest GS301 readings to each device
	for device in odorSensor:
		device.latest_reading = device.gs301History.order_by('-created_at').first()
	enviroSensor = IotDevice.objects.filter(selectBranch=branchId).filter(name__startswith="AM319")
	for device in enviroSensor:
		device.latest_reading = device.am319History.order_by('-created_at').first()
	em300 = IotDevice.objects.filter(selectBranch=branchId).filter(name__startswith="EM300")
	for device in em300:
		device.latest_reading = device.em300History.order_by('-created_at').first()
	em400 = IotDevice.objects.filter(selectBranch=branchId).filter(name__startswith="EM400")
	for device in em400:
		device.latest_reading = device.em400History.order_by('-created_at').first()
	vs121 = IotDevice.objects.filter(selectBranch=branchId).filter(name__startswith="VS121")
	for device in vs121:
		device.latest_reading = device.vs121History.order_by('-created_at').first()
	context = {'sensor_groups': sensor_groups,
	           'odorSensor': odorSensor,
	           'enviroSensor': enviroSensor, 'em300': em300,
	           'em400': em400, 'vs121': vs121}
	return render(request, 'tenant/common/dashboard/iot/newIotBranch.html', context)


def custom_404(request, exception):
	return render(request, 'tenant/common/404.html', {}, status=404)


def custom_500(request):
	return render(request, 'tenant/common/500.html', {}, status=500)
