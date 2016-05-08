from django.contrib import admin
from .models import competition, work, city, Comment, profile, work_for_competition# Register your models here.

class CAdmin(admin.TabularInline):
    model = work_for_competition


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo', 'begin_date', 'final_date', 'status', 'city']
    empty_value_display = '-empty-'
    list_filter = ('name', 'begin_date', 'final_date')
    search_fields = ('name', )
    date_hierarchy = 'begin_date'
    ordering = ['begin_date', 'final_date', 'name']
    inlines = [CAdmin]
class WorkAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'updated', 'photo', 'slug','author']
    list_filter = ('name', 'created','author')
    search_fields = ('name', 'created')
    date_hierarchy = 'created'
    ordering = ['name', 'created','author']
    prepopulated_fields = {'slug': ('name',)}
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'competition', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'facility', 'photo')
    list_filter = ('facility',)


class WFCAdmin(admin.ModelAdmin):
    list_display = ('work_name', 'competition', 'place',)
    list_filter = ('competition', 'place',)
    # list_select_related = True
    # radio_fields = {'students':admin.VERTICAL}
admin.site.register(competition, CompetitionAdmin)
admin.site.register(work, WorkAdmin)
admin.site.register(city)
admin.site.register(Comment, CommentAdmin)
admin.site.register(profile, ProfileAdmin)
admin.site.register(work_for_competition, WFCAdmin)