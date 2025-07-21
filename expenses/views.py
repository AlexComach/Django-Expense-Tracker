from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .models import Transactions
from expenses.filters import TransactionFilter
from .forms import TransactionForm 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


cache.clear()

def home(request):
    return render(request, "expenses/home.html")


@login_required
def profile(request):
    return render(request, "expenses/profile.html")


@login_required
def dashboard(request):
    return render(request, "expenses/dashboard.html")


@login_required
def transactions(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transactions.objects.filter(user=request.user).order_by('-date')
    )

    if request.method == 'POST':
        add_form = TransactionForm(request.POST)
        if add_form.is_valid():
            transaction = add_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transactions')
    else:
        add_form = TransactionForm()

    paginator = Paginator(transaction_filter.qs, 20)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  

    context = {
        'filter': transaction_filter,
        'transactions': page_obj,  
        'add_form': add_form,
    }
    return render(request, 'expenses/transactions.html', context)

