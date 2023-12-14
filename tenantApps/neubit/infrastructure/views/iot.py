from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from tenantApps.neubit.infrastructure.forms import IotGatewayForm, IotDeviceForm
from tenantApps.neubit.infrastructure.models import IotGateway, IotDevice


## Gateway CRUD ####
@login_required(login_url='account_login')
def iotGatewayList(request):
	user_branches = request.user.branchUser.all()
	all_iotGateway = IotGateway.objects.filter(selectBranch__in=user_branches)
	context = {'all_iotGateway': all_iotGateway}
	return render(request, 'tenant/neubit/infrastructure/iot/gateway/index.html', context)


@login_required(login_url='account_login')
def iotGatewayCreate(request):
	iotGatewayAddForm = IotGatewayForm()
	if request.method == "POST":
		form = IotGatewayForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "IOT Gateway Added Successfully")
			return redirect('Infrastructure:iotGatewayList')
	context = {'iotGatewayAddForm': iotGatewayAddForm}
	return render(request, 'tenant/neubit/infrastructure/iot/gateway/partial/gatewayAdd.html', context)


@login_required(login_url='account_login')
def iotGatewayUpdate(request, iotId):
	context = {}
	return render(request, 'tenant/neubit/infrastructure/iot/gateway/partial/gatewayUpdate.html', context)


@login_required(login_url='account_login')
def iotGatewayDelete(request, iotId):
	reference = IotGateway.objects.get(id=iotId)
	reference.delete()
	messages.success(request, 'IOT Deleted Successfully')
	return redirect('Infrastructure:iotGatewayList')


### IOT Devices CRUD ####
@login_required(login_url='account_login')
def iotDeviceList(request):
	user_branches = request.user.branchUser.all()
	all_iot_device = IotDevice.objects.filter(selectBranch__in=user_branches)
	context = {'all_iot_device': all_iot_device}
	return render(request, 'tenant/neubit/infrastructure/iot/devices/index.html', context)


@login_required(login_url='account_login')
def iotDeviceCreate(request):
	iotDeviceForm = IotDeviceForm()
	if request.method == "POST":
		form = IotDeviceForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Sensor Added Successfully")
			return redirect('Infrastructure:iotDeviceList')
	context = {'iotDeviceForm': iotDeviceForm}
	return render(request, 'tenant/neubit/infrastructure/iot/devices/partial/deviceAdd.html', context)


@login_required(login_url='account_login')
def iotDeviceUpdate(request, deviceId):
	sensor_update = IotDevice.objects.get(id=deviceId)
	form = IotDeviceForm(instance=sensor_update)
	if request.method == "POST":
		form = IotDeviceForm(request.POST, instance=sensor_update)
		if form.is_valid():
			form.save()
			messages.success(request, 'Sensor Updated Successfully')
			return redirect('Infrastructure:iotDeviceList')
	context = {'updateForm': form, 'sensor_update': sensor_update}
	return render(request, 'tenant/neubit/infrastructure/iot/devices/partial/deviceUpdate.html', context)


@login_required(login_url='account_login')
def iotDeviceDelete(request, deviceId):
	reference = IotDevice.objects.get(id=deviceId)
	reference.delete()
	messages.success(request, 'Sensor Deleted Successfully')
	return redirect('Infrastructure:iotDeviceList')
