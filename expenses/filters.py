import django_filters 
from django.forms import DateInput
from expenses.models import Transactions
from django.utils import timezone
from datetime import date

class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        choices=Transactions.TRANSACTION_TYPES,
        field_name='type',
        lookup_expr='iexact',
        empty_label='Any',
        label='Transaction Type'
    )

    category = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains',
        label='Category (contains)'
    )

    min_amount = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='gte',
        label='Min Amount'
    )

    max_amount = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='lte',
        label='Max Amount'
    )

    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Start Date',
        widget=DateInput(attrs={'type': 'date'})
    )

    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='End Date',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Transactions
        fields = [] 

    @classmethod
    def get_current_month_expenses(cls, user):
        today = date.today()
        
        queryset = Transactions.objects.select_related('category').filter(
            user=user, 
            type='Expense',
            date__year=today.year,
            date__month=today.month
        )
        
        return cls({}, queryset=queryset).qs