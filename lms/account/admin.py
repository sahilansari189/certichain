from django.contrib import admin
from .models import AllowedEmail, UserInfo, BulkAllowedEmail
# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'verification_code', 'verification_code_created_at', 'verification_code_expires_at', 'verification_code_used_at')
    list_filter = ('is_verified', 'verification_code_expires_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-verification_code_expires_at',)

admin.site.register(AllowedEmail)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(BulkAllowedEmail)

