from django.contrib import admin
from .models import Certificate,Badge,StudentBadge
# Register your models here.

admin.site.register(Certificate)
admin.site.register(Badge)
admin.site.register(StudentBadge)