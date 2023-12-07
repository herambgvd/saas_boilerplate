# forms.py

from django import forms

from .models import Marketplace, MarketplaceFiles, Asset


class MarketplaceForm(forms.ModelForm):
	class Meta:
		model = Marketplace
		fields = ['name', 'icon', 'weights']


class MarketplaceFilesForm(forms.ModelForm):
	class Meta:
		model = MarketplaceFiles
		fields = ['name', 'fileName']


class AssetForm(forms.ModelForm):
	make_poly_lines = forms.BooleanField(required=False, label='Do you want to make Poly Lines?')

	class Meta:
		model = Asset
		fields = ['name', 'liveUrl', 'tagModel', 'make_poly_lines']
