from django.contrib import admin

# Register your models here.
from user.models import Members


@admin.register(Members)
class Members(admin.ModelAdmin):
    pass
