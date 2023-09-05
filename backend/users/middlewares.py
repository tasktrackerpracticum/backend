from django.utils.timezone import now

from users.models import User


class SetLastVisitMiddleware:
    """Set current time to requested user in last_login field."""

    def __init__(self, get_response):
        """Init."""
        self.get_response = get_response

    def __call__(self, request):
        """Set current time to requested user in last_login field."""
        if request.user.is_authenticated:
            User.objects.filter(pk=request.user.pk).update(last_login=now())
        response = self.get_response(request)
        return response
