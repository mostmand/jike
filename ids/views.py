import datetime
# Create your views here.
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from ids.models import ddos, bruteForce
from jike.settings import DDOS_H, DDOS_N, BRUTE_FORCE_N


@csrf_exempt
def log_ddos(request):
    current_ip = get_client_ip(request)
    current_browser = get_client_browser(request)
    ddos_row = ddos.objects.create(ip=current_ip, browser=current_browser, pub_date=timezone.now())
    ddos_row.save()

    delta = datetime.timedelta(seconds=DDOS_H)
    if ddos.objects.filter(ip=current_ip, pub_date__gte=timezone.now()-delta).count() > DDOS_N:
        print("ddos detected from " + current_ip)

    log_brute_force(request)


def log_brute_force(request):
    if not request.user.is_authenticated:
        current_ip = get_client_ip(request)
        current_browser = get_client_browser(request)
        row = bruteForce.objects.create(ip=current_ip, browser=current_browser, pub_date=timezone.now())
        row.save()
        if bruteForce.objects.filter(ip=current_ip).count() > BRUTE_FORCE_N:
            print("brute force detected from " + current_ip)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_browser(request):
    return "Chrome"
