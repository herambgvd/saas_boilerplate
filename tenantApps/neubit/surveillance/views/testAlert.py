from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from tenantApps.neubit.surveillance.forms import TestAlertForm, TestAlertAckForm
from tenantApps.neubit.surveillance.models import TestAlert, TestAlertAcknowledge


@login_required(login_url="account_login")
def testAlert(request):
	alert_data = TestAlert.objects.all()
	context = {'alert_data': alert_data}
	return render(request, 'tenant/neubit/surveillance/testAlert/alertSetup/index.html', context)


@login_required(login_url="account_login")
def testAlertCreate(request):
	alertAddForm = TestAlertForm()
	if request.method == "POST":
		form = TestAlertForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Alert Added Successfully')
			return redirect('Surveillance:test-alert-list')
	context = {'alertAddForm': alertAddForm}
	return render(request, 'tenant/neubit/surveillance/testAlert/alertSetup/partials/alertAdd.html', context)


@login_required(login_url="account_login")
def testAlertUpdate(request, pk):
	alert_update = TestAlert.objects.get(id=pk)
	form = TestAlertForm(instance=alert_update)
	if request.method == "POST":
		form = TestAlertForm(request.POST, instance=alert_update)
		if form.is_valid():
			form.save()
			messages.success(request, 'Alert Updated Successfully')
			return redirect('Surveillance:test-alert-list')
	context = {'updateForm': form}
	return render(request, 'tenant/neubit/surveillance/testAlert/alertSetup/partials/alertUpdate.html', context)


@login_required(login_url="account_login")
def testAlertDelete(request, pk):
	alertDelete = TestAlert.objects.get(id=pk)
	alertDelete.delete()
	messages.success(request, 'Alert Deleted Successfully')
	return redirect('Surveillance:test-alert-list')


# Generate Alert
@login_required(login_url="account_login")
def generateAlert(request):
	alertCode = request.GET.get('alertCode')
	data = TestAlert.objects.get(id=alertCode)
	testGenerate = TestAlertAcknowledge.objects.create(alert=data)
	testGenerate.save()
	return JsonResponse({'alertName': data.alertName})


@login_required(login_url="account_login")
def testAlertAckList(request):
	data = TestAlertAcknowledge.objects.filter(ack="Pending").order_by('-created_at')
	context = {'data': data}
	return render(request, 'tenant/neubit/surveillance/testAlert/alert/index.html', context)


@login_required(login_url="account_login")
def testAlertAcknowledge(request, pk):
	ackForm = TestAlertAckForm()
	data = TestAlertAcknowledge.objects.get(id=pk)
	if request.method == 'POST':
		form = TestAlertAckForm(request.POST)
		if form.is_valid():
			data.alertType = form.cleaned_data['alertType']
			data.description = form.cleaned_data['description']
			data.ack = form.cleaned_data['ack']
			data.ack_status = True
			data.save()
			return redirect('Surveillance:test-alert-ack-list')
	context = {'data': data, 'form': ackForm}
	return render(request, 'tenant/neubit/surveillance/testAlert/alert/acknowledge/alertAcknowledge.html', context)


@login_required(login_url="account_login")
def testAlertHistory(request):
	data = TestAlertAcknowledge.objects.filter(ack_status=True).order_by('-created_at')
	context = {'data': data}
	return render(request, 'tenant/neubit/surveillance/testAlert/alert/acknowledge/alertHistory.html', context)
