

from app_log.models import AppLog


def log(*args, **kwargs):
    return AppLog.objects.log(*args, **kwargs)

def log_request(*args, **kwargs):
    return AppLog.objects.log_request(*args, **kwargs)