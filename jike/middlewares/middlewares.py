from django.contrib.sessions.models import Session
from accounts.models import UsersIP


class EduLikeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_anonymous:
            request_ip = get_client_ip(request)
            user_ip_query = UsersIP.objects.filter(user=request.user)
            if user_ip_query.exists():
                user_ip = user_ip_query.first()
                if user_ip.ip != request_ip:
                    sessions = Session.objects.filter(session_key=user_ip.session_id)
                    if sessions.exists():
                        sessions.delete()
                user_ip_query.delete()
            new_user_ip = UsersIP.objects.create(
                session_id=request.session.session_key,
                user=request.user,
                ip=request_ip
            )
            new_user_ip.save()

        response = self.get_response(request)

        return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
