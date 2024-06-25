# library/urls.py

from django.urls import path
from .views import (
    BookDetailView,
    review_book,
    BorrowBookView,
    ReturnBookView,
    BorrowHistoryView,
    AddPostCreateView,
    selling_profile_view,
)

urlpatterns = [
    path('add/', AddPostCreateView.as_view(), name='sellbook'),
    path('myView/', selling_profile_view, name='myView'),
    path('details/<int:book_id>/', BookDetailView.as_view(), name='detail_book'),
    path('borrow/<int:book_id>/', BorrowBookView.as_view(), name='borrow_book'),
    path('return/<int:book_id>/', ReturnBookView.as_view(), name='return_book'),
    path('history/', BorrowHistoryView.as_view(), name='borrow_history'),
    path('add_review/<int:book_id>/', review_book, name='add_review'),
]
