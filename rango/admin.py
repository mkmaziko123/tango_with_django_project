from django.contrib import admin

# Register your models here.
from django.contrib import admin
from rango.models import Page, Category

class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'url')  # The three fields in order
    admin.site.register(Category)
    admin.site.register(Page, PageAdmin)

