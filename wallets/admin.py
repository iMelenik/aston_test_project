from django.contrib import admin

from .models import Wallet


# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'type', 'balance', 'currency']
    list_display_links = ['name']
    search_fields = ['owner', 'name']
    ordering = ['user', 'currency']

    @staticmethod
    def owner(obj):
        return obj.user.user.username


admin.site.register(Wallet, WalletAdmin)
