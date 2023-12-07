from django.forms import ModelForm

from .models import TestAlert, TestAlertAcknowledge


class TestAlertForm(ModelForm):
	class Meta:
		model = TestAlert
		fields = "__all__"


class TestAlertAckForm(ModelForm):
	class Meta:
		model = TestAlertAcknowledge
		fields = ['alertType', 'description', 'ack']
