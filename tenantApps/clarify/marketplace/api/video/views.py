from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tenantApps.clarify.marketplace.models import MarketplaceFiles
from .serializers import MarketplaceFilesSerializer


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_marketplace_file(request, id):
	try:
		marketplace_file = MarketplaceFiles.objects.get(id=id)
	except MarketplaceFiles.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	serializer = MarketplaceFilesSerializer(marketplace_file, data=request.data, partial=True)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
