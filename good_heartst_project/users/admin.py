from django.contrib import admin

from .models import MyUser


@admin.register(MyUser)
class AdminUser(admin.ModelAdmin):
    list_display = ('username',
                    'role',
                    'email',
                    'phone_number',
                    )
    search_fields = ('usermane',)