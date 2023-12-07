from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from tenantApps.neubit.infrastructure.forms import PanelAddForm
from tenantApps.neubit.infrastructure.models import Panel


# Panel CRUD
@login_required(login_url="account_login")
def devicePanelInfo(request):
	user_branches = request.user.branchUser.all()
	all_devices = Panel.objects.filter(selectBranch__in=user_branches)
	context = {'all_devices': all_devices}
	return render(request, 'tenant/neubit/infrastructure/panel/index.html', context)


@login_required(login_url="account_login")
def devicePanelAdd(request):
	panelAddForm = PanelAddForm()
	if request.method == 'POST':
		form = PanelAddForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Panel Added Successfully')
			return redirect('Infrastructure:devicePanelInfo')
	context = {'panelAddForm': panelAddForm}
	return render(request, 'tenant/neubit/infrastructure/panel/partials/panelAdd.html', context)


@login_required(login_url="account_login")
def devicePanelUpdate(request, pk):
	panel_update = Panel.objects.get(id=pk)
	form = PanelAddForm(instance=panel_update)
	if request.method == 'POST':
		form = PanelAddForm(request.POST, instance=panel_update)
		if form.is_valid():
			form.save()
			messages.success(request, 'Panel Updated Successfully')
			return redirect('Infrastructure:devicePanelInfo')
	context = {'updateForm': form, 'panel_Update': panel_update}
	return render(request, 'tenant/neubit/infrastructure/panel/partials/panelUpdate.html', context)


@login_required(login_url="account_login")
def devicePanelDelete(request, pk):
	panDelete = Panel.objects.get(id=pk)
	panDelete.delete()
	messages.success(request, 'Panel Deleted Successfully')
	return redirect("Infrastructure:devicePanelInfo")
