from django import forms

from .models import Branch


class BranchForm(forms.ModelForm):
	class Meta:
		model = Branch
		fields = ['regionName', 'country', 'state', 'city', 'branchCode', 'branchName', 'branchAddress', 'users']
