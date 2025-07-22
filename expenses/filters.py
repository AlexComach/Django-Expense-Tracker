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
    def get_current_month_data(cls):
        """Get transactions for the current month"""
        today = date.today()
        first_day = today.replace(day=1)
        
        if today.month == 12:
            last_day = today.replace(year=today.year + 1, month=1, day=1)
        else:
            last_day = today.replace(month=today.month + 1, day=1)
        
        filter_data = {
            'start_date': first_day,
            'end_date': last_day
        }
        
        queryset = Transactions.objects.select_related('category').all()
        return cls(filter_data, queryset=queryset).qs