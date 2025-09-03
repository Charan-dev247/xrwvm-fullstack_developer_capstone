from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# Car Make Model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100, default='Unknown')  # Optional extra field
    founded_year = models.IntegerField(
        validators=[
            MinValueValidator(1800),
            MaxValueValidator(now().year)
        ],
        default=2000
    )

    def __str__(self):
        return self.name  # Displays name in admin panel
        

# Car Model Model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship
    dealer_id = models.IntegerField(null=True, blank=True)  # Refers to dealer in Cloudant DB
    name = models.CharField(max_length=100)

    # Car Type Choices
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')

    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2023)
        ],
        default=2023
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Optional field
    fuel_type = models.CharField(max_length=20, default='Petrol')  # Optional
    transmission = models.CharField(max_length=20, default='Manual')  # Optional

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
