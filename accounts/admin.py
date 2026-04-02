from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "profile_image", "phone", "address")


admin.site.register(models.User, UserAdmin)
