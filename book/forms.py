from django import forms
from .models import Book,Borrow,Review
from catagories.models import Catagories  

from catagories.models import Catagories  

class BookForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Catagories.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'}),
        required=False,
    )
    class Meta:
        model = Book
        fields = ['title', 'description', 'price', 'quantity', 'categories', 'image', 'accounts']


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['book', 'amount']

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=Review.RATING_CHOICES, widget=forms.Select(attrs={
        'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500',
    }))

    class Meta:
        model = Review
        fields = ['name', 'rating', 'body']
    