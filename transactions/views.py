from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from django.db.models import Sum
from .forms import DepositForm
from .models import Transaction
from accounts.models import UserBankAccount

def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {'user': user, 'amount': amount})
    email = EmailMultiAlternatives(subject, '', to=[user.email])
    email.attach_alternative(message, "text/html")
    email.send()

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': self.title})
        return context

class DepositMoneyView(LoginRequiredMixin, CreateView):
    form_class = DepositForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_report')
    title = 'Deposit'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        try:
            user_account = self.request.user.account
        except UserBankAccount.DoesNotExist:
            user_account = UserBankAccount.objects.create(user=self.request.user, balance=0)
        user_account.balance += amount
        user_account.save(update_fields=['balance'])
        
        transaction = form.save(commit=False)
        transaction.account = user_account
        transaction.balance_after_transaction = user_account.balance
        transaction.save()

     
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        
        send_transaction_email(self.request.user, amount, "Deposit Message", "transactions/deposit_email.html")

        return super().form_valid(form)


class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0 
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
