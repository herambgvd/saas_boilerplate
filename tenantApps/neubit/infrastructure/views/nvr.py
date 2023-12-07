import csv
import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from tenantApps.common.branch.models import Branch
from tenantApps.neubit.infrastructure.forms import NvrAddForm, NVRUploadForm
from tenantApps.neubit.infrastructure.models import NVR, CCTV


# NVR CRUD
@login_required(login_url="account_login")
def deviceNvrInfo(request):
	user_branches = request.user.branchUser.all()
	all_devices = NVR.objects.filter(selectBranch__in=user_branches)
	context = {'all_devices': all_devices}
	return render(request, 'tenant/neubit/infrastructure/nvr/index.html', context)


@login_required(login_url="account_login")
def deviceNvrAdd(request):
	nvrAddForm = NvrAddForm()
	if request.method == "POST":
		form = NvrAddForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "NVR Added Successfully")
			return redirect('Infrastructure:deviceNvrInfo')
	context = {'nvrAddForm': nvrAddForm}
	return render(request, 'tenant/neubit/infrastructure/nvr/partials/nvrAdd.html', context)


@login_required(login_url="account_login")
def deviceNvrUpdate(request, pk):
	nvr_update = NVR.objects.get(id=pk)
	form = NvrAddForm(instance=nvr_update)
	if request.method == "POST":
		form = NvrAddForm(request.POST, instance=nvr_update)
		if form.is_valid():
			form.save()
			messages.success(request, 'NVR Updated Successfully')
			return redirect('Infrastructure:deviceNvrInfo')
	context = {'updateForm': form, 'nvr_Update': nvr_update}
	return render(request, 'tenant/neubit/infrastructure/nvr/partials/nvrUpdate.html', context)


@login_required(login_url="account_login")
def deviceNvrDelete(request, pk):
	nvrDelete = NVR.objects.get(id=pk)
	nvrDelete.delete()
	messages.success(request, 'NVR Deleted Successfully')
	return redirect("Infrastructure:deviceNvrInfo")


@login_required(login_url="account_login")
def nvrDetails(request, pk):
	nvrDetail = get_object_or_404(NVR, pk=pk)
	cctvDetail = CCTV.objects.filter(selectNvr=nvrDetail)
	context = {'nvrDetail': nvrDetail, 'cctvDetail': cctvDetail}
	return render(request, 'tenant/neubit/infrastructure/nvr/detail.html', context)


@login_required(login_url="account_login")
def bulkUpload(request):
	if request.method == 'POST':
		form = NVRUploadForm(request.POST, request.FILES)
		if form.is_valid():
			csv_file = request.FILES['csv_file']
			decoded_file = csv_file.read().decode('utf-8')
			io_string = io.StringIO(decoded_file)
			reader = csv.DictReader(io_string)

			for row in reader:
				branch = Branch.objects.get(name=row['BranchName'])  # Adjust field names as necessary
				NVR.objects.create(
					selectBranch=branch,
					selectManufacturer=row['Manufacturer'],
					slugName=row['SlugName'],
					username=row['Username'],
					password=row['Password'],
					ipAddress=row['IPAddress'],
					port=row['Port'],
				)
			return redirect('Infrastructure:deviceNvrInfo')
	else:
		form = NVRUploadForm()
	context = {'form': form}
	return render(request, 'tenant/neubit/infrastructure/nvr/upload.html', context)
