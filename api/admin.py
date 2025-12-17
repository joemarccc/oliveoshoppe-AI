from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Plant

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'display_image', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('display_image',)
    fields = ('name', 'description', 'price', 'image', 'display_image')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Product Image'

    class Media:
        css = {
            'all': ('admin/css/custom.css',)
        }

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'image_preview', 'created_at', 'updated_at')
    list_filter = ('stock', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('image_preview',)
    ordering = ('name',)

    def image_preview(self, obj):
        try:
            if obj.image_src:
                return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover;" />', obj.image_src)
        except Exception:
            pass
        return "No image"
    image_preview.short_description = 'Image Preview' 