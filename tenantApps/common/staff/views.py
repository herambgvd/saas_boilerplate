from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from .forms import GroupForm, CustomUserUpdateForm, CustomUserCreationForm


#### Groups Views #####
@login_required(login_url="account_login")
def groups(request):
	all_roles = Group.objects.annotate(user_count=Count('user'))
	context = {'all_roles': all_roles}
	return render(request, 'tenant/common/staff/groups/index.html', context)


@login_required(login_url="account_login")
def group_create(request):
	if request.method == "POST":
		form = GroupForm(request.POST)
		if form.is_valid():
			group = form.save()
			group.permissions.set(form.cleaned_data['permissions'])
			messages.success(request, "Group Created Successfully")
			return redirect('Staff:groups')
	else:
		form = GroupForm()

	# Define package-based model groupings
	package_model_mapping = {
		'common': ['group', 'user', 'country', 'state', 'city', 'branch'],
		'neubit': ['panel', 'cctv', 'nvr', 'cameratag', 'testalert', 'testalertacknowledge'],
		'iot': ['iotgateway', 'iotdevice']
	}

	# Determine which packages to include based on tenant attributes
	model_names = package_model_mapping['common']  # 'common' package is always included
	if getattr(request.tenant, 'neubit', False):
		model_names.extend(package_model_mapping['neubit'])
	if getattr(request.tenant, 'iot', False):
		model_names.extend(package_model_mapping['iot'])

	# Fetch the relevant ContentType objects
	content_types = ContentType.objects.filter(model__in=model_names)

	# Fetch permissions for the relevant models
	permissions = Permission.objects.filter(content_type__in=content_types)

	# Group the permissions by content type
	grouped_permissions = {}
	for perm in permissions:
		ct_name = perm.content_type.name
		if ct_name not in grouped_permissions:
			grouped_permissions[ct_name] = []
		grouped_permissions[ct_name].append(perm)

	context = {'form': form, 'grouped_permissions': grouped_permissions}
	return render(request, 'tenant/common/staff/groups/partial/group_create.html', context)


@login_required(login_url="account_login")
def group_update(request, group_id):
	group = get_object_or_404(Group, pk=group_id)

	if request.method == "POST":
		form = GroupForm(request.POST, instance=group)
		if form.is_valid():
			updated_group = form.save()
			updated_group.permissions.set(form.cleaned_data['permissions'])
			messages.success(request, "Group Updated Successfully")
			return redirect('Staff:groups')
	else:
		form = GroupForm(instance=group)

	# Define package-based model groupings
	package_model_mapping = {
		'common': ['group', 'user', 'country', 'state', 'city', 'branch'],
		'neubit': ['panel', 'cctv', 'nvr', 'cameratag', 'testalert', 'testalertacknowledge'],
		'iot': ['iotgateway', 'iotdevice']
	}

	# Determine packages to include based on tenant attributes
	model_names = package_model_mapping['common']
	if getattr(request.tenant, 'neubit', False):
		model_names.extend(package_model_mapping['neubit'])
	if getattr(request.tenant, 'iot', False):
		model_names.extend(package_model_mapping['iot'])

	# Fetch the relevant ContentType objects
	content_types = ContentType.objects.filter(model__in=model_names)

	# Fetch permissions for the relevant models
	permissions = Permission.objects.filter(content_type__in=content_types)

	# Fetch current permissions of the group
	group_permissions = set(group.permissions.all())

	# Group the permissions by content type
	grouped_permissions = {}
	for perm in permissions:
		ct_name = perm.content_type.name
		if ct_name not in grouped_permissions:
			grouped_permissions[ct_name] = []
		grouped_permissions[ct_name].append(perm)

	context = {
		'form': form,
		'grouped_permissions': grouped_permissions,
		'group_permissions': group_permissions,
		'group': group
	}
	return render(request, 'tenant/common/staff/groups/partial/group_update.html', context)


@login_required(login_url="account_login")
def group_delete(request, group_id):
	group = get_object_or_404(Group, pk=group_id)
	if request.method == "POST":
		messages.success(request, "Group Deleted Successfully")
		group.delete()
		return redirect('Staff:groups')
	return render(request, 'tenant/common/staff/groups/partial/group_confirm.html', {'group': group})


@login_required(login_url="account_login")
def user_list(request):
	user_data = User.objects.all()
	context = {'user_data': user_data}
	return render(request, 'tenant/common/staff/user/index.html', context)


@login_required(login_url="account_login")
def create_user(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('Staff:user_list')
	else:
		form = CustomUserCreationForm()
	return render(request, 'tenant/common/staff/user/partial/user_create.html', {'form': form})


@login_required(login_url="account_login")
def update_user(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	if request.method == 'POST':
		form = CustomUserUpdateForm(request.POST, instance=user)
		if form.is_valid():
			updated_user = form.save()
			group_ids = [group.id for group in form.cleaned_data["groups"]]
			updated_user.groups.set(group_ids)
			return redirect('Staff:user_list')
	else:
		form = CustomUserUpdateForm(instance=user)
	return render(request, 'tenant/common/staff/user/partial/user_update.html', {'form': form, 'user_id': user_id})


@login_required
def delete_user(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	if request.method == 'POST':
		user.delete()
		return redirect('Staff:user_list')
	return render(request, 'tenant/common/staff/user/partial/user_confirm.html', {'user': user})
