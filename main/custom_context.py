from main.models import SiteConfiguration

def config(request):
    return {'config': SiteConfiguration.objects.all().first(),}