from django import forms
from .models import Transactions
from django.contrib.auth.models import User

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['type', 'amount', 'description', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
        self.fields['username'].help_text = None
