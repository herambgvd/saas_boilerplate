from django import forms

from tenant.models import Client, Domain


class TenantForm(forms.ModelForm):
	class Meta:
		model = Client
		exclude = ['is_active', 'neubit', 'clarify', 'bms', 'iot', 'cloudRecording']


class DomainForm(forms.ModelForm):
	class Meta:
		model = Domain
		fields = "__all__"
