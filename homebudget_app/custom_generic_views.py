from django.core.exceptions import FieldDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .models import Month


class MonthCreateView(CreateView):
    template_name = 'homebudget_app/mybudget_forms.html'

    def get(self, request, *args, **kwargs):
        """Extends parent class get() method with model instance ownership verification"""
        get_object_or_404(Month, pk=kwargs['pk'], slug=kwargs['slug'],
                          user=request.user)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object._meta.get_field('month')
            self.object.month = get_object_or_404(Month, pk=self.kwargs['pk'], slug=self.kwargs['slug'],
                                                  user=self.request.user)
            self.object.save()
        except FieldDoesNotExist:
            pass
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homebudget_app:month', kwargs={'pk': self.kwargs['pk'],
                                                            'slug': self.kwargs['slug']})


class MonthUpdateView(UpdateView):
    template_name = 'homebudget_app/mybudget_forms.html'

    def get_success_url(self):
        return reverse_lazy('homebudget_app:month', kwargs={'pk': self.kwargs['pk'],
                                                            'slug': self.kwargs['slug']})

