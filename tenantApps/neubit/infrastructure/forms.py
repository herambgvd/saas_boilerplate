from django import forms

from .models import Panel, NVR, CCTV, CameraTag, IotGateway, IotDevice


class PanelAddForm(forms.ModelForm):
	class Meta:
		model = Panel
		fields = '__all__'


class NvrAddForm(forms.ModelForm):
	class Meta:
		model = NVR
		fields = ['selectBranch', 'selectManufacturer', 'slugName', 'username',
		          'password', 'ipAddress', 'port', 'playbackUrl']


class CctvAddForm(forms.ModelForm):
	class Meta:
		model = CCTV
		exclude = ['selectNvr']


class TagForm(forms.ModelForm):
	class Meta:
		model = CameraTag
		fields = '__all__'


class IotGatewayForm(forms.ModelForm):
	class Meta:
		model = IotGateway
		exclude = ['fetchDevice']


class IotDeviceForm(forms.ModelForm):
	class Meta:
		model = IotDevice
		fields = '__all__'


class NVRUploadForm(forms.Form):
	csv_file = forms.FileField()
