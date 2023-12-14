import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SaaS_Boilerplate.settings')

import django

django.setup()

from django.contrib.auth.models import User
from django_tenants.utils import tenant_context
from tenant.models import Client, Domain


def create_public_tenant():
	# Check if public tenant already exists
	if not Client.objects.filter(schema_name='public').exists():
		tenantPublic = Client(schema_name='public', name="Super Admin", description="Platform Manager")
		tenantPublic.save()

		# Add one or more domains for the tenant
		domain = Domain()
		domain.domain = 'localhost'  # Replace 'your_domain.com' with your domain.
		domain.tenant = tenantPublic
		domain.is_primary = True
		domain.save()


def create_client_tenant(domain_url, schema_name, clientName, clientDescription):
	tenantClient = Client(schema_name=schema_name, name=clientName, description=clientDescription)
	tenantClient.save()

	domain = Domain()
	domain.domain = domain_url
	domain.tenant = tenantClient
	domain.is_primary = True
	domain.save()

	return tenantClient


def create_tenant_superuser(tenantClient, username, email, password):
	with tenant_context(tenantClient):
		user = User(username=username, email=email, is_staff=True, is_superuser=True)
		user.set_password(password)
		user.save()


if __name__ == "__main__":
	create_public_tenant()
	# Gather input for client tenant
	domain_urlClient = input("Enter the domain URL for the client tenant (e.g., client1.your_domain.com): ")
	schema_nameClient = input("Enter a unique schema name for the client tenant: ")
	nameOfClient = input("Enter the Name of Client:")
	descriptionOfClient = input("Enter shot description of Client:")
	usernameClient = input("Enter a username for the superuser: ")
	emailClient = input("Enter an email for the superuser: ")
	passwordClient = input("Enter a password for the superuser: ")

	tenant = create_client_tenant(domain_urlClient, schema_nameClient, nameOfClient, descriptionOfClient)
	create_tenant_superuser(tenant, usernameClient, emailClient, passwordClient)
	print(f"Tenant {domain_urlClient} created with superuser {usernameClient}.")


# {
#   "name":"Airtel-Environ-Sensor",
#   "co2":"1298",
#   "hcho":"0.06",
#   "humidity":"49.5",
#   "light_level":"1",
#   "pir_trigger":"0",
#   "pm10":"66",
#   "pm2_5":"55",
#   "pressure":"986.5",
#   "temperature":"37.35",
#   "tvoc":"1.0",
#   "category":"Environment Sensor",
#   "schema":"airtel"
# }