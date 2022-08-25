from django.contrib import admin
from donation.models import Description


class DescriptionAdmin(admin.ModelAdmin):

    fields = ['name_item', 'amount_item', 'request_hash_id']
    list_display = ('name_item', 'amount_item', 'request_hash_id')
    readonly_fields = ('request_hash_id',)


admin.site.register(Description, DescriptionAdmin)
