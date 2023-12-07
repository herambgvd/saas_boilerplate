from django.db.models import Sum
from django.http import JsonResponse

from tenantApps.clarify.marketplace.models import Marketplace, MarketplaceFiles


def ai_models_data(request):
    ai_models = Marketplace.objects.all()
    ai_models_info = []

    for model in ai_models:
        files = MarketplaceFiles.objects.filter(selectMarketplace=model)
        total_file_size = files.aggregate(Sum('fileSize'))['fileSize__sum'] or 0
        total_files_count = files.count()

        ai_models_info.append({
            'name': model.name,
            'icon': model.icon.url,
            'usages_allowed': model.no_of_usage_allowed,
            'times_used': model.no_of_used,
            'total_files_count': total_files_count,
            'total_file_size': total_file_size,
        })

    return JsonResponse(ai_models_info, safe=False)
