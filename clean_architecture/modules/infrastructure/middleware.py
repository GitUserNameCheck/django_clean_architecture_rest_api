from django.contrib.auth.decorators import login_required
from django.utils.decorators import decorator_from_middleware
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [
            reverse('login'), 
            reverse('register')
        ]

        exempt_paths = ['/admin/']

        if not request.user.is_authenticated:
            if not any(request.path.startswith(url) for url in exempt_urls) and \
               not any(request.path.startswith(path) for path in exempt_paths):
                return redirect(reverse('login') + f"?next={request.path}")

        response = self.get_response(request)
        return response