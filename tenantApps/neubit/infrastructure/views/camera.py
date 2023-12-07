import json
from urllib.parse import urlparse

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from tenantApps.neubit.infrastructure.forms import CctvAddForm, TagForm
from tenantApps.neubit.infrastructure.models import NVR, CCTV, CameraTag, VOD


@login_required(login_url='account_login')
def cctvCreate(request, nvrId):
	nvr = get_object_or_404(NVR, pk=nvrId)
	if request.method == 'POST':
		form = CctvAddForm(request.POST)
		if form.is_valid():
			cctv = form.save(commit=False)
			cctv.selectNvr = nvr
			cctv.save()
			messages.success(request, 'CCTV Created Successfully')
			return redirect('Infrastructure:nvrDetails', nvrId)
	else:
		form = CctvAddForm()
	context = {'cctvAddForm': form, 'nvrId': nvrId}
	return render(request, 'tenant/neubit/infrastructure/cctv/partial/cctvAdd.html', context)


@login_required(login_url='account_login')
def cctvUpdate(request, nvrId, cctvId):
	reference = CCTV.objects.get(id=cctvId)
	if request.method == 'POST':
		form = CctvAddForm(request.POST, instance=reference)
		if form.is_valid():
			panelData = form.save(commit=False)
			panelData.save()
			messages.success(request, 'CCTV Updated Successfully')
			return redirect('Infrastructure:nvrDetails', nvrId)
	else:
		form = CctvAddForm(instance=reference)
	context = {'form': form, 'reference': reference, 'nvrId': nvrId}
	return render(request, 'tenant/neubit/infrastructure/cctv/partial/cctvUpdate.html', context)


@login_required(login_url='account_login')
def cctvDelete(request, nvrId, cctvId):
	reference = CCTV.objects.get(id=cctvId)
	reference.delete()
	messages.success(request, 'CCTV Deleted Successfully')
	return redirect('Infrastructure:nvrDetails', nvrId)


@login_required(login_url="account_login")
def pushRtspAndStart(request, nvrId, cctvId):
	rtsp = CCTV.objects.get(id=cctvId)
	if rtsp.hlsCreated:
		streamId = urlparse(rtsp.hlsLink).path.split('/')[-1].split('.')[0]
		url = "https://stream.geniusvision.in:5443/LiveApp/rest/v2/broadcasts/" + str(streamId)
		payload = {}
		headers = {}
		response = requests.request("DELETE", url, headers=headers, data=payload)
		CCTV.objects.filter(id=cctvId).update(hlsCreated=False)
		messages.success(request, "Successfully Stream Stopped")
	else:
		url = "https://stream.geniusvision.in:5443/LiveApp/rest/v2/broadcasts/create"
		payload = json.dumps({
			"name": rtsp.slugName,
			"description": "Stream",
			"type": "streamSource",
			"streamUrl": rtsp.rtspLink
		})
		headers = {
			'Content-Type': 'application/json'
		}
		streamAdding = requests.request("POST", url, headers=headers, data=payload)
		res = json.loads(streamAdding.text)
		streamId = res["streamId"]
		hlsLinkCreated = "https://stream.geniusvision.in:5443/LiveApp/streams/" + streamId + ".m3u8"
		CCTV.objects.filter(id=cctvId).update(hlsLink=hlsLinkCreated)
		CCTV.objects.filter(id=cctvId).update(hlsCreated=True)
		url = "https://stream.geniusvision.in:5443/LiveApp/rest/v2/broadcasts/" + str(streamId) + "/start"
		streamStarting = requests.request("POST", url, headers=headers, data=payload)
		messages.success(request, "Successfully Stream Start in 2sec")
	return redirect('Infrastructure:nvrDetails', nvrId)


@login_required(login_url="account_login")
def recordingStartAndStop(request, nvrId, cctvId):
	rtsp = CCTV.objects.get(id=cctvId)
	if rtsp.hlsCreated:
		if rtsp.recordingStatus:
			streamId = urlparse(rtsp.hlsLink).path.split('/')[-1].split('.')[0]
			url = f"https://stream.geniusvision.in:5443/LiveApp/rest/v2/broadcasts/{{}}/recording/false?recordType=mp4".format(
				streamId)
			payload = {}
			headers = {}
			response = requests.request("PUT", url, headers=headers, data=payload)
			CCTV.objects.filter(id=cctvId).update(recordingStatus=False)
			messages.warning(request, "Recording Stop")
		else:
			streamId = urlparse(rtsp.hlsLink).path.split('/')[-1].split('.')[0]
			url = f"https://stream.geniusvision.in:5443/LiveApp/rest/v2/broadcasts/{{}}/recording/true?recordType=mp4".format(
				streamId)
			payload = {}
			headers = {}
			response = requests.request("PUT", url, headers=headers, data=payload)
			CCTV.objects.filter(id=cctvId).update(recordingStatus=True)
			messages.warning(request, "Recording On")
	else:
		messages.error(request, "Stream is not active")
	return redirect('Infrastructure:nvrDetails', nvrId)


@login_required(login_url="account_login")
def streamCamera(request, nvrId, cctvId):
	camera = CCTV.objects.get(id=cctvId)
	context = {'nvrId': nvrId, 'camera': camera}
	return render(request, 'tenant/neubit/infrastructure/cctv/singleStream.html', context)


# Tag Views
@login_required(login_url="account_login")
def tagAll(request):
	userTags = CameraTag.objects.filter(users=request.user)
	context = {'allTag': userTags}
	return render(request, "tenant/neubit/infrastructure/cameraTag/index.html", context)


@login_required(login_url="account_login")
def tagAdd(request):
	tagForm = TagForm()
	if request.method == "POST":
		form = TagForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Tag Added Successfully')
			return redirect('Infrastructure:allTag')
	context = {'tagForm': tagForm}
	return render(request, "tenant/neubit/infrastructure/cameraTag/partials/tagAdd.html", context)


@login_required(login_url="account_login")
def tagUpdate(request, pk):
	tag_update = CameraTag.objects.get(id=pk)
	form = TagForm(instance=tag_update)
	if request.method == "POST":
		form = TagForm(request.POST, instance=tag_update)
		if form.is_valid():
			form.save()
			messages.success(request, 'Tag Updated Successfully')
			return redirect('Infrastructure:allTag')
	context = {'updateForm': form, 'tag_Update': tag_update}
	return render(request, "tenant/neubit/infrastructure/cameraTag/partials/tagUpdate.html", context)


@login_required(login_url="account_login")
def tagDelete(request, pk):
	tagDel = CameraTag.objects.get(id=pk)
	tagDel.delete()
	messages.success(request, 'Tag Deleted Successfully')
	return redirect('Infrastructure:allTag')


# Fetch VODs
@login_required(login_url="account_login")
def fetch_and_save_vod_data(request, nvrId):
	url = "https://stream.geniusvision.in:5443/LiveApp/rest/v2/vods/list/0/100"
	headers = {
		'Authorization': 'Basic YWRtaW46R3ZkQDYwMDE='
	}

	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		vod_data = json.loads(response.text)

		for item in vod_data:
			stream_id = item['streamId']
			vod_id = item['vodId']

			# Check if the VOD ID already exists in the database
			if not VOD.objects.filter(vod_id=vod_id).exists():
				# Extract the CCTV object with the HLS link containing the stream ID
				try:
					cctv = CCTV.objects.get(hlsLink__contains=stream_id)
				except CCTV.DoesNotExist:
					print(f"No CCTV found with stream ID: {stream_id}")
					continue
				# print("########################")
				# print("CCTV Info:", cctv)
				# print("stream_id:", stream_id)
				# print("creation_date:", item['creationDate'])
				# print("start_time:", item['startTime'])
				# print("duration:", item['duration'])
				# print("file_size:", item['fileSize'])
				# print("file_path:", item['filePath'])
				# print("vod_id:", vod_id)
				# print("########################")

			# Create a new VOD object, associate it with the CCTV object, and save it to the database
				VOD.objects.create(
					cctv=cctv,  # Associate with the CCTV object
					stream_id=stream_id,
					creation_date=item['creationDate'],
					start_time=item['startTime'],
					duration=item['duration'],
					file_size=item['fileSize'],
					file_path=item['filePath'],
					vod_id=vod_id
				)

		return redirect('Infrastructure:nvrDetails', nvrId)


@login_required(login_url="account_login")
def streamVod(request, nvrId, cctvId):
	cameraVod = VOD.objects.filter(cctv=cctvId).order_by('-creation_date')
	context = {'nvrId': nvrId, 'cameraVod': cameraVod}
	return render(request, 'tenant/neubit/infrastructure/cctv/vod/index.html', context)
