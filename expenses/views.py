from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .models import Transactions
from expenses.filters import TransactionFilter
from .forms import TransactionForm 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import plotly.express as px
import pandas as pd
from .filters import TransactionFilter
import calendar
from django.utils import timezone
from django.db.models import Sum
from django.http import HttpResponse
from .forms import UserProfileForm 

cache.clear()

def home(request):
    return render(request, "expenses/home.html")

@login_required
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            form = UserProfileForm(instance=user)
            
            if request.headers.get('HX-Request'):
                return render(request, "expenses/_profile_form.html", {"form": form})
            else:
                return redirect('profile')
        else:
            if request.headers.get('HX-Request'):
                return render(request, "expenses/_profile_form.html", {"form": form})
    
    form = UserProfileForm(instance=user)
    return render(request, "expenses/profile.html", {"form": form})




@login_required
def dashboard(request):
    current_month_data = TransactionFilter.get_current_month_expenses(request.user)
    
    print(f"Found {current_month_data.count()} transactions")
    print("Transaction dates:", list(current_month_data.values_list('date', flat=True)))
    
    df = pd.DataFrame(current_month_data.values('amount', 'category__name'))
    df = df.rename(columns={'category__name': 'category'})
    
    now = timezone.now()
    month_name = calendar.month_name[now.month]
    
    total_spent = current_month_data.aggregate(total=Sum('amount'))['total'] or 0
    total_earned = 0  
    budget_remaining = 2000 - total_spent  
    recent_transactions = Transactions.objects.filter(user=request.user).order_by('-date')[:3]
    
    if df.empty:
        chart = "<p>No transactions found for this month.</p>"
    else:
        print("DataFrame:", df)
        
        fig = px.pie(df, values='amount', names='category',
                    title=f'Expenses for {month_name} {now.year}', 
                    hole=.3)
        
        chart = fig.to_html()
    
    context = {
        'chart': chart,
        'total_spent': total_spent,
        'total_earned': total_earned,
        'budget_remaining': budget_remaining,
        'month_name': month_name,
        'recent_transactions': recent_transactions, 
    }
    return render(request, "expenses/dashboard.html", context)


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

