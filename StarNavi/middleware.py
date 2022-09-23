from django.utils import timezone


class UpdateLastUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        exclude_paths = ['/auth/activity/']
        if request.path not in exclude_paths:
            user = request.user
            if user.is_authenticated:
                user.last_activity = timezone.now()
                user.save()
        return None
