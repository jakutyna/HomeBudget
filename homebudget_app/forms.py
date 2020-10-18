from django import forms

from .models import Month

class AddMonthForm(forms.ModelForm):
    class Meta:
        model = Month
        fields = ['month_name', 'year']