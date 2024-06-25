from django.db import models
from django.contrib.auth.models import User
from book.models import Book
from django.utils import timezone

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)  

    def __str__(self):
        return f'{self.user.username} borrowed {self.book.title}'
