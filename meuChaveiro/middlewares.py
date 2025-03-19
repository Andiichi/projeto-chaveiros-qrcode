from django.conf import settings

class SeparateAdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            settings.SESSION_COOKIE_NAME = 'session_admin'
        else:
            settings.SESSION_COOKIE_NAME = 'session_user'
        
        response = self.get_response(request)
        return response