from django.conf import settings
from django.contrib import admin
from .models import UserProfile

User = settings.AUTH_USER_MODEL


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_display_links = ['user']

    # class UserInLine(admin.TabularInline):
    #     model = User
    #     extra = 0
    #
    # inlines = [UserInLine]


admin.site.register(UserProfile, UserProfileAdmin)


