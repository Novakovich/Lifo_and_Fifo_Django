from django.contrib import admin
from donation.models import RequestItem, Description


@admin.action(description='Mark selected items as used')
def make_used(modeladmin, request, queryset):
    queryset.update(condition='Used')


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('name_item', 'amount_item', 'request_hash_id', 'state', 'condition', )
    search_fields = ['request_hash_id__exact']
    list_filter = ('state',)
    fieldsets = (
        ('Main info', {
            'fields': ('name_item',)
        }),
        ('Additional info', {
            'fields': ('amount_item', 'request_hash_id', 'state', 'condition',)
        }),
    )
    readonly_fields = ('request_hash_id',)
    actions = [make_used]


admin.site.register(Description, DescriptionAdmin)


class RequestItemAdmin(admin.ModelAdmin):
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


admin.site.register(RequestItem, RequestItemAdmin)
