from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name',
                    'is_staff', 'is_superuser', 'password')
    search_fields = ('username',)
    empty_value_display = '-пусто-'


# admin.site.register(User, UserAdmin)
