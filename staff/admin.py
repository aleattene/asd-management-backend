from django.contrib import admin

from staff.models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "fiscal_code", "user", "is_active")
    list_filter = ("is_active",)
    search_fields = ("first_name", "last_name", "fiscal_code")
