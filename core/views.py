from django.shortcuts import render, get_object_or_404
from book.models import Book
from catagories.models import Catagories

# Create your views here.
def home(request, catagory_slug=None):
    categories = Catagories.objects.all()
    data = Book.objects.all()

    if catagory_slug is not None:
        cat = get_object_or_404(Catagories, slug=catagory_slug)
        data = Book.objects.filter(catagories=cat)
    
    return render(request, 'home.html', {'data': data, 'categories': categories})
