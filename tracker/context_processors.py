from django.conf import settings


def extra_context(request):
    return {"demo_mode": settings.DEMO_MODE}
