from django.contrib import admin

from .models import ConnectiveTag, ConnectiveTaggedItem

# Register your models here.

admin.site.register(ConnectiveTag)
admin.site.register(ConnectiveTaggedItem)
