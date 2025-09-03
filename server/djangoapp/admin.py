from django.contrib import admin
from .models import CarMake, CarModel

# Inline for CarModel so we can add/edit CarModels inside CarMake
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of empty CarModel forms displayed by default


# CarMakeAdmin with inline CarModels
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    inlines = [CarModelInline]


# CarModelAdmin for detailed CarModel view
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year', 'price', 'fuel_type', 'transmission', 'dealer_id')
    list_filter = ('type', 'year', 'fuel_type', 'transmission')
    search_fields = ('name', 'car_make__name')  # Allows searching by car model name and car make name


# Register models with their admins
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
