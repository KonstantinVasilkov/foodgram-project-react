from django.contrib import admin

from .models import Subscribe, User

EMPTY_VALUE = '<-EMPTY->'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User model representation in admin panel"""
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
    )
    list_filter = ('email', 'username',)
    empty_value_display = EMPTY_VALUE


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Subscribe model representation in admin panel"""
    list_display = ('id', 'user', 'author')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = EMPTY_VALUE
