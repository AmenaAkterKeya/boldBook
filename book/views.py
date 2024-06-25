from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView,View
from .forms import BookForm,ReviewForm
from .models import Book,Borrow,Review
from transactions.models import Transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView
from transactions.views import send_transaction_email

@method_decorator(login_required, name='dispatch')
class AddPostCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'sellbook.html'
    success_url = reverse_lazy('myView')

    def form_valid(self, form):
        form.instance.accounts = self.request.user
        return super().form_valid(form)

@login_required
def selling_profile_view(request):
    user_books = Book.objects.filter(accounts=request.user)
    data = {'user_books': user_books}
    return render(request, 'sellingProfile.html', data)

class BookDetailView(DetailView):
    model = Book
    template_name = 'bookDetails.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'
    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        post = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = post
            new_review.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object 
        reviews = post.reviews.all()
        review_form = ReviewForm()
        
        context['reviews'] = reviews
        context['review_form'] = review_form
        return context 

class BorrowBookView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        borrow = Borrow(user=request.user, book=book, amount=book.price)
        borrow.save()

        account = request.user.account
        account.balance -= borrow.amount
        account.save()
     
        balance_after_transaction = account.balance
        Transaction.objects.create(
            account=account,
            amount=-borrow.amount,
            balance_after_transaction=balance_after_transaction,
            timestamp=borrow.borrow_date,
            transaction_type='1'  
        )

        messages.success(request, f'You have successfully borrowed {book.title}.')
        
        send_transaction_email(self.request.user,{book.title}, "Borrow Message", "borrow_email.html")
        return redirect('borrow_history')  


class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        borrow = get_object_or_404(Borrow, pk=book_id, user=request.user, return_date__isnull=True)
        borrow.return_date = timezone.now()
        borrow.save()
        account = request.user.account
        account.balance += borrow.amount
        account.save(update_fields=['balance'])
     
        Transaction.objects.create(
            account=account,
            amount=borrow.amount,
            balance_after_transaction=account.balance,
            timestamp=borrow.return_date,
            transaction_type='2'  
        )

        messages.success(request, f'You have successfully returned {borrow.book.title}.')
        
        return redirect('borrow_history')  



class BorrowHistoryView(LoginRequiredMixin, ListView):
    model = Borrow
    template_name = 'borrow_history.html'
    context_object_name = 'borrows'

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user).order_by('-borrow_date')
    
    
@login_required
def review_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            rating = form.cleaned_data['rating']
            body = form.cleaned_data['body']
            Review.objects.create(user=request.user, book=book, name=name, rating=rating, body=body)
            
            messages.success(request, 'Your review has been successfully submitted.')
            return redirect('detail_book', book_id=book_id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews.html', {'form': form, 'book': book})