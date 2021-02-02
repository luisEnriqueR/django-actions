# Django
from django.contrib import admin

# Models
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
