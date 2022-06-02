from django.contrib import admin
from .models import Subscription
# Register your models here.

class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(Subscription, SubscriptionAdmin)