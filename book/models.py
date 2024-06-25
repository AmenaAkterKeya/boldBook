from django.db import models
# Create your models here.
from catagories.models import Catagories
from django.contrib.auth.models import User
from django.utils import timezone
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    quantity = models.PositiveIntegerField()
    catagories = models.ManyToManyField(Catagories)
    image = models.ImageField(upload_to='media/uploads/', blank = True, null = True)
    accounts = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_by')
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)  

    def __str__(self):
        return f'{self.user.username} borrowed {self.book.title}'
    
   

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank = True, null = True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=30)
    body = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user.username} for {self.book.title}"