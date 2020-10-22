from django import forms

from .models import Category, MonthCategory

class MonthCategoryForm(forms.ModelForm):
    class Meta:
        model = MonthCategory
        fields = ['category', 'category_budget']

    def __init__(self, user, *args, **kwargs):
        super(MonthCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)