# Where we define how the admin interface for the app
# Register your models here.
from django.contrib import admin
from .models import UserProfile, DASS21Result, CounselingSession, MentalHealthResource, ProgressNote

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'university', 'created_at')
    list_filter = ('gender', 'year_of_study', 'has_previous_counseling')
    search_fields = ('user__username', 'user__email', 'university')

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