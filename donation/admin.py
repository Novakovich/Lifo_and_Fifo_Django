from django.contrib import admin
from donation.models import Description


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('name_item', 'amount_item', 'request_hash_id', 'condition')
    fieldsets = (
        ('Main info', {
            'fields': ('name_item',)
        }),
        ('Additional info', {
            'fields': ('amount_item', 'request_hash_id', 'condition')
        }),
    )
    readonly_fields = ('request_hash_id',)


admin.site.register(Description, DescriptionAdmin)
