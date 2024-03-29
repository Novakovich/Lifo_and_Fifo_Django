from django.contrib import admin
from donation.models import RequestItem, Description, Donate, Office


@admin.action(description='Mark selected items as used')
def make_used(modeladmin, request, queryset):
    queryset.update(condition='Used')


@admin.action(description='Mark selected items as available')
def make_available(modeladmin, request, queryset):
    queryset.update(state='Available')


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('name_item', 'amount_item', 'donate_uuid_id', 'state', 'condition', 'id', 'office_id')
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
    readonly_fields = ('donate_uuid_id', 'photo')
    actions = [make_used, make_available]


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


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'office_count', 'capacity')


admin.site.register(Office, OfficeAdmin)
