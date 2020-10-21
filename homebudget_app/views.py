import calendar, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

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
    template_name = 'homebudget_app/add_month.html'

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
    template_name = 'homebudget_app/add_category.html'
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
        month_budget = hasattr(month,'monthbudget')
        # try:
        #     month_budget = month.monthbudget
        # except ObjectDoesNotExist:
        #     month_budget = None
        month_categories = month.monthcategory_set.all()
        ctx = {
            'month': month,
            'month_budget': str(month_budget),
            'month_categories': month_categories,
        }
        return render(request, 'homebudget_app/month.html', ctx)
