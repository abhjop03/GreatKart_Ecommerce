from django.contrib import admin
from .models import Account

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active', 'is_superadmin')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('date_joined', 'last_login', 'password')
    filter_horizontal = ()
    list_display_links = ('email', 'first_name', 'last_name', 'username')
    list_select_related = ()
    ordering = ('-date_joined',)
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)

