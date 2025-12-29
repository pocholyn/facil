from django.contrib import admin
from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('area_venta', 'anno', 'mes', 'plan')
    list_filter = ('area_venta', 'anno', 'mes')
    search_fields = ('area_venta__nombre',)
    ordering = ('-anno', '-mes', 'area_venta')
