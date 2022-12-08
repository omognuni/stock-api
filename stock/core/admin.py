from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models

admin.site.register(models.Account)
admin.site.register(models.Invest)
admin.site.register(models.Holding)