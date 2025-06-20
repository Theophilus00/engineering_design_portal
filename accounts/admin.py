from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # ✅ What shows in the user list page
    list_display = (
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
        'is_reviewer',
        'date_joined',
        'last_login',
        'view_actions'
    )

    # ✅ Clickable links in list view
    list_display_links = ('email',)

    # ✅ Filters on the right sidebar
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'is_reviewer',
        'date_joined',
    )

    # ✅ Search box
    search_fields = ('email',)

    # ✅ Sorting
    ordering = ('-date_joined',)

    # ✅ Grouped field sections in detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ()}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_reviewer',
                'groups',
                'user_permissions',
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # ✅ Fields to show when adding a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_reviewer',
            ),
        }),
    )

    # ✅ Add a custom action/view column (example: show a badge)
    def view_actions(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            'green' if obj.is_active else 'red',
            'Active' if obj.is_active else 'Inactive'
        )
    view_actions.short_description = 'Status'
