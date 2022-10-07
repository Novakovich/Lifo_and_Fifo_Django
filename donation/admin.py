from django.contrib import admin
from donation.models import RequestItem, Description, Donate


@admin.action(description='Mark selected items as used')
def make_used(modeladmin, request, queryset):
    queryset.update(condition='Used')


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('name_item', 'amount_item', 'donate_uuid_id', 'state', 'condition', 'id', 'photo', 'office_id')
    search_fields = ['donate_uuid__exact']
    list_filter = ('state',)
    fieldsets = (
        ('Main info', {
            'fields': ('name_item',)
        }),
        ('Additional info', {
            'fields': ('amount_item', 'donate_uuid', 'state', 'condition', 'photo', 'office', 'place')
        }),
    )
    readonly_fields = ('donate_uuid_id',)
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


class DescriptionInline(admin.TabularInline):
    model = Description


class DonateAdmin(admin.ModelAdmin):
    list_display = ('donate_amount', 'id')
    fields = ('donate_amount', )
    readonly_fields = ('id',)
    inlines = [DescriptionInline]


admin.site.register(Donate, DonateAdmin)
