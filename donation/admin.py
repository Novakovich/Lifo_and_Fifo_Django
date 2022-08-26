from django.contrib import admin
from donation.models import Description, RequestItem, DonateItem


class DonateItemAdmin(admin.ModelAdmin):
    list_display = ('name_item', 'amount_item', 'request_hash_id', 'state',)
    search_fields = ['request_hash_id__exact']
    list_filter = ('state',)
    fieldsets = (
        ('Main info', {
            'fields': ('name_item',)
        }),
        ('Additional info', {
            'fields': ('amount_item', 'request_hash_id', 'state',)
        }),
    )
    readonly_fields = ('request_hash_id',)


admin.site.register(DonateItem, DonateItemAdmin)
