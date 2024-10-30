from django.contrib import admin
from .models import VolunteerProfile, Task, Reward

@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_hours', 'rank')
    search_fields = ('user__username',)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('total_hours',)
        return ()

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'hours_reward',  'is_completed', 'created_at')
    list_filter = ('is_completed',)
    search_fields = ('title', 'assigned_to__username')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('title', 'required_hours')
    search_fields = ('title',)