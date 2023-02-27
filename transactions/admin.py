from django.contrib import admin

from .models import Transaction


# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'transfer_amount', 'commission', 'status']
    list_display_links = ['sender', 'receiver']
    search_fields = ['sender', 'receiver']


admin.site.register(Transaction, TransactionAdmin)
