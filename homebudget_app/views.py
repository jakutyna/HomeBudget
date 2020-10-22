from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from .custom_generic_views import MonthCreateView, MonthUpdateView
from .forms import MonthCategoryForm
from .functions.functions import month_first_last_day
from .models import Category, Expense, Month, MonthBudget, MonthCategory


class MyBudgetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        months = Month.objects.filter(user=request.user).order_by('-month_beginning_date')
        categories = Category.objects.filter(user=request.user).order_by('name')
        ctx = {
            'months': months,
            'categories': categories,
        }
        return render(request, 'homebudget_app/mybudget.html', ctx)


class AddMonthView(LoginRequiredMixin, CreateView):
    model = Month
    fields = ['month_name', 'year']
    template_name = 'homebudget_app/mybudget_forms.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        year = self.object.year
        month = self.object.month_name
        first_last_day = month_first_last_day(year, month)
        self.object.month_beginning_date = first_last_day[0]
        self.object.month_end_date = first_last_day[1]
        self.object.slug = '{}-{}'.format(self.object.get_month_name_display().lower(), year)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homebudget_app:month', kwargs={'pk': self.object.pk,
                                                            'slug': self.object.slug})


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'homebudget_app/mybudget_forms.html'
    success_url = reverse_lazy('homebudget_app:mybudget')

    # TODO: add CategoryView and update success_url

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = self.object.name.lower()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MonthView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        month = get_object_or_404(Month, pk=kwargs['pk'], slug=kwargs['slug'], user=request.user)
        month_budget = month.monthbudget if hasattr(month, 'monthbudget') else None
        month_categories = month.monthcategory_set.all()

        category_expenses_list_with_none_values = [
            month_category.expense_set.all().aggregate(Sum('expense_amount'))['expense_amount__sum'] for
            month_category in month_categories
        ]

        category_expenses_list = [0 if val is None else val for val in category_expenses_list_with_none_values]

        total_expenses = 0

        for month_category in month_categories:
            expenses_sum = month_category.expense_set.all().aggregate(Sum('expense_amount'))['expense_amount__sum']
            if expenses_sum is None:
                expenses_sum = 0
            month_category.category_expenses = expenses_sum
            month_category.category_budget_left = (None if month_category.category_budget is None else
                                                   month_category.category_budget - expenses_sum)
            total_expenses += expenses_sum

        total_difference = None if month_budget is None else month_budget.budget - total_expenses
        total_sum_and_diff = (total_expenses, total_difference)

        ctx = {
            'month': month,
            'month_budget': month_budget,
            'month_categories': month_categories,
            'category_expenses_list': category_expenses_list,
            'total_sum_and_diff': total_sum_and_diff,
        }
        return render(request, 'homebudget_app/month.html', ctx)


class AddMonthBudgetView(LoginRequiredMixin, MonthCreateView):
    model = MonthBudget
    fields = ['budget']


class UpdateMonthBudgetView(LoginRequiredMixin, MonthUpdateView):
    model = MonthBudget
    fields = ['budget']

    def get_object(self):
        month = get_object_or_404(Month, pk=self.kwargs.get(self.pk_url_kwarg),
                                  slug=self.kwargs.get(self.slug_url_kwarg),
                                  user=self.request.user)
        return self.model.objects.get(pk=month.monthbudget.pk)


class AddMonthCategoryView(LoginRequiredMixin, MonthCreateView):
    form_class = MonthCategoryForm

    def get_form_kwargs(self):
        form_kwargs = super(AddMonthCategoryView, self).get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs


class AddExpenseView(LoginRequiredMixin, MonthCreateView):
    model = Expense
    fields = ['name', 'expense_amount', 'description']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        month = get_object_or_404(Month, pk=self.kwargs['pk'], slug=self.kwargs['slug'],
                                  user=self.request.user)
        self.object.month_category = get_object_or_404(MonthCategory, pk=self.kwargs['mc_pk'], month=month)
        self.object.save()
        return super().form_valid(form)
