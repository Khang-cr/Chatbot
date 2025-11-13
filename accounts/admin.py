# Where we define how the admin interface for the app
# Register your models here.
from django.contrib import admin
from .models import UserProfile, DASS21Result, CounselingSession, MentalHealthResource, ProgressNote

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'verification_status', 'age', 'university', 'created_at')
    list_filter = ('user_type', 'verification_status', 'gender')
    search_fields = ('user__username', 'user__email', 'university')
    
    # admin approve/reject therapist
    actions = ['approve_therapist', 'reject_therapist']
    
    def approve_therapist(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(user_type='therapist').update(
            verification_status='approved',
            verified_at=timezone.now()
        )
        self.message_user(request, f'{updated} therapist(s) approved.')
    approve_therapist.short_description = 'Approve selected therapists'
    
    def reject_therapist(self, request, queryset):
        updated = queryset.filter(user_type='therapist').update(
            verification_status='rejected'
        )
        self.message_user(request, f'{updated} therapist(s) rejected.')
    reject_therapist.short_description = 'Reject selected therapists'

@admin.register(DASS21Result)
class DASS21ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_date', 'depression_level', 'anxiety_level', 'stress_level')
    list_filter = ('depression_level', 'anxiety_level', 'stress_level', 'test_date')
    search_fields = ('user__username',)
    readonly_fields = ('test_date',)

@admin.register(CounselingSession)
class CounselingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_date', 'counselor_name', 'session_type', 'duration_minutes')
    list_filter = ('session_type', 'session_date')
    search_fields = ('user__username', 'counselor_name')

@admin.register(MentalHealthResource)
class MentalHealthResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'for_depression', 'for_anxiety', 'for_stress', 'is_active')
    list_filter = ('resource_type', 'for_depression', 'for_anxiety', 'for_stress', 'is_active')
    search_fields = ('title', 'description')

@admin.register(ProgressNote)
class ProgressNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood_rating', 'sleep_hours', 'exercise_done')
    list_filter = ('mood_rating', 'exercise_done', 'date')
    search_fields = ('user__username',)