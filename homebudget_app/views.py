import calendar, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .functions.functions import month_first_last_day
from .forms import AddMonthForm
from .models import Category, Month


class MyBudgetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        months = Month.objects.filter(user=request.user).order_by('-month_beginning_date')
        categories = Category.objects.filter(user=request.user).order_by('name')
        ctx = {
            'months': months,
            'categories': categories,
        }
        return render(request, 'homebudget_app/mybudget.html', ctx)


class MonthView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'homebudget_app/month.html')


class AddMonthView(LoginRequiredMixin, CreateView):
    form_class = AddMonthForm
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
        return reverse_lazy('homebudget_app:month', kwargs={'month_slug': self.object.slug})
