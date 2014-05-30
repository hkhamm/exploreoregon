from django.contrib import admin
from app_log.models import AppLog

model_admin_cls = admin.ModelAdmin
try:
    from client_admin.admin import ClientModelAdmin
    model_admin_cls = ClientModelAdmin
except ImportError:
    pass


class AppLogAdmin(model_admin_cls):
    list_display = ('who','what','when','where','info','ip_address')
    list_filter = ('what','when','where')
    search_fields = ('who','what','where','info','ip_address')


admin.site.register(AppLog, AppLogAdmin)