from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User


class GroupForm(forms.ModelForm):
	permissions = forms.ModelMultipleChoiceField(
		queryset=Permission.objects.all(),
		widget=forms.CheckboxSelectMultiple,
	)

	class Meta:
		model = Group
		fields = ['name', 'permissions']


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'first_name', 'last_name', 'groups']


class CustomUserCreationForm(UserCreationForm):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	is_active = forms.BooleanField(required=False, initial=True)
	groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email", "password1", "password2", "is_active", "groups")

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		user.is_active = self.cleaned_data["is_active"]
		if commit:
			user.save()
			user.groups.set(self.cleaned_data["groups"])
		return user


class CustomUserUpdateForm(UserChangeForm):
	password = None  # Hides the password field
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	is_active = forms.BooleanField(required=False)
	groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email", "is_active", "groups")

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		user.is_active = self.cleaned_data["is_active"]
		if commit:
			user.save()
			user.groups.set(self.cleaned_data["groups"])
		return user
