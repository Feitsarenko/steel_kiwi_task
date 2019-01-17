from .models import PageLoadsLogbook
from ipware.ip import get_ip


class PageLoadsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.path[:6] == '/shop/' and response.status_code == 200:

            if request.user.is_authenticated:
                visit = PageLoadsLogbook.objects.create(user=request.user, url=request.path)
            else:
                visit = PageLoadsLogbook.objects.create(user_ip=get_ip(request), url=request.path)
            visit.save()

        return response
