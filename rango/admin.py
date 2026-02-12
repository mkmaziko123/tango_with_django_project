from django.contrib import admin
from rango.models import Page, Category

# Define PageAdmin first
class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'url')  # Fields to display in admin
admin.site.register(Category)
admin.site.register(Page, PageAdmin)  
