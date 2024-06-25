from django.shortcuts import render,redirect
from . import forms
# Create your views here.
def book_Catagories(request):
    if request.method=='POST':
        CatagoriesName=forms.CatagoriesForm(request.POST)
        if CatagoriesName.is_valid():
            CatagoriesName.save()
            return redirect(book_Catagories)
        
    else:
        CatagoriesName=forms.CatagoriesForm()
    return render(request,'./catagories/catagories.html',{'form':CatagoriesName})