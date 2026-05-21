from django.contrib import admin
from django.utils import timezone
from .models import Department, DoctorProfile, SlotTemplate, Slot
from datetime import datetime

# -------------------------------------------------------------------
# Department
# -------------------------------------------------------------------
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# -------------------------------------------------------------------
# DoctorProfile
# -------------------------------------------------------------------
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'experience_years', 'consultation_fee')
    list_filter = ('department',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    raw_id_fields = ('user',)   # if user count is large
    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('Professional', {'fields': ('department', 'experience_years', 'qualifications')}),
        ('Financial', {'fields': ('consultation_fee',)}),
        ('Media', {'fields': ('profile_picture',)}),
    )

# -------------------------------------------------------------------
# SlotTemplate (recurring rule)
# -------------------------------------------------------------------
class SlotTemplateInline(admin.TabularInline):
    model = SlotTemplate
    extra = 1
    fields = ('day_of_week', 'start_time', 'end_time', 'slot_quota', 'is_active')
    ordering = ('day_of_week', 'start_time')

@admin.register(SlotTemplate)
class SlotTemplateAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time', 'slot_quota', 'is_active')
    list_filter = ('day_of_week', 'is_active', 'doctor__department')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name')
    list_editable = ('slot_quota', 'is_active')
    ordering = ('doctor', 'day_of_week', 'start_time')

# -------------------------------------------------------------------
# Slot (concrete instances)
# from django.contrib import admin


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = (
        'doctor',
        'display_start_local',
        'display_end_local',
        'no_of_quota_remaining',
        'is_available',
    )
    list_filter = (
        'doctor__department',
        'doctor',
        ('date', admin.DateFieldListFilter),
    )
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name')
    list_editable = ('no_of_quota_remaining',)
    ordering = ('date', 'start_time')
    date_hierarchy = 'date'

    def display_start_local(self, obj):
        """Combine date and start_time, then convert to local timezone."""
        naive_dt = datetime.combine(obj.date, obj.start_time)
        # Make aware in UTC? Actually naive datetime is interpreted as local time if USE_TZ=True.
        # Safer: Assume naive datetime is in settings.TIME_ZONE.
        # Using make_aware with is_dst=None.
        aware_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())
        local_dt = timezone.localtime(aware_dt)
        return local_dt.strftime("%Y-%m-%d %H:%M")
    display_start_local.short_description = "Start Time (Local)"

    def display_end_local(self, obj):
        naive_dt = datetime.combine(obj.date, obj.end_time)
        aware_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())
        local_dt = timezone.localtime(aware_dt)
        return local_dt.strftime("%H:%M")
    display_end_local.short_description = "End Time (Local)"

    def is_available(self, obj):
        return obj.no_of_quota_remaining > 0
    is_available.boolean = True
    is_available.short_description = "Available"