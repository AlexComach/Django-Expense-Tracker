from django import forms
from .models import Transactions, UserProfile
from django.contrib.auth.models import User

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['type', 'amount', 'description', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, disabled=True)
    email = forms.EmailField(disabled=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    birth_date = forms.DateField(
    required=False,
    widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control',
        'placeholder': 'Select date'
    })
    )
    
    class Meta:
        model = UserProfile
        fields = ['location', 'phone_number', 'birth_date']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields = {
            'username': self.fields['username'],
            'email': self.fields['email'],
            'first_name': self.fields['first_name'],
            'last_name': self.fields['last_name'],
            'location': self.fields['location'],
            'phone_number': self.fields['phone_number'],
            'birth_date': self.fields['birth_date'],
        }
        
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        
        self.fields['username'].help_text = None
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.save()
            profile.save()
        return profile