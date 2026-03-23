from django.contrib import admin

from doctors.models import SportDoctor


@admin.register(SportDoctor)
class SportDoctorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "vat_number", "is_active")
    list_filter = ("is_active",)
    search_fields = ("first_name", "last_name", "vat_number")
