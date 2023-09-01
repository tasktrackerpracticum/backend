from django.utils.timezone import now

from users.models import User


class SetLastVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            User.objects.filter(pk=request.user.pk)[0].update(last_login=now())
        response = self.get_response(request)
        return response
