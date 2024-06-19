from django.contrib import admin
from education.models import Training


class TrainingAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    list_filter = ("start_date", "end_date")
    search_fields = ("name", "description")
    date_hierarchy = "start_date"

admin.site.register(Training, TrainingAdmin)
