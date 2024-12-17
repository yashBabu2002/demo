from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    author = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_year = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
    
