from django import forms
from .models import Transactions

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['type', 'amount', 'description', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }