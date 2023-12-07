from django.http import JsonResponse

from tenantApps.common.branch.models import Branch
from tenantApps.neubit.infrastructure.models import NVR, CCTV, Panel
from tenantApps.neubit.surveillance.models import TestAlertAcknowledge


def branch_data(request):
	branches = Branch.objects.all()
	nvr = NVR.objects.all()
	cctv = CCTV.objects.all()
	panel = Panel.objects.all()

	region_counts = {
		'North': branches.filter(regionName='North').count(),
		'East': branches.filter(regionName='East').count(),
		'West': branches.filter(regionName='West').count(),
		'South': branches.filter(regionName='South').count(),
		'Total': branches.count(),
		'nvr': nvr.count(),
		'cctv': cctv.count(),
		'panel': panel.count()
	}

	return JsonResponse(region_counts)


def devices_per_branch_data(request):
	branches = Branch.objects.all()
	data = {
		"branch": [branch.branchName for branch in branches],
		"camera": [CCTV.objects.filter(selectNvr__selectBranch=branch).count() for branch in branches],
		"panel": [Panel.objects.filter(selectBranch=branch).count() for branch in branches],
		"nvr": [NVR.objects.filter(selectBranch=branch).count() for branch in branches],
	}
	return JsonResponse(data)


def get_branch_map(request):
	branches = Branch.objects.all()
	branch_info = [
		{
			"name": branch.branchName,
			"address": branch.branchAddress,
			"latitude": float(branch.latitude),
			"longitude": float(branch.longitude),
			"id": branch.id
		}
		for branch in branches
	]

	return JsonResponse({"branches": branch_info})


def get_demo_alert_data(request):
	total_alerts = TestAlertAcknowledge.objects.count()
	pending_alerts = TestAlertAcknowledge.objects.filter(ack="Pending").count()
	open_alerts = TestAlertAcknowledge.objects.filter(ack="Open").count()
	close_alerts = TestAlertAcknowledge.objects.filter(ack="Close").count()

	return JsonResponse({
		'totalAlerts': total_alerts,
		'pendingAlerts': pending_alerts,
		'openAlerts': open_alerts,
		'closeAlerts': close_alerts,
	})
