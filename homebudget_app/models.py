from django.db import models
from django.contrib.auth.models import User


class Month(models.Model):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    MONTH_NAME_CHOICES = (
        (JANUARY, "January"),
        (FEBRUARY, "February"),
        (MARCH, "March"),
        (APRIL, "April"),
        (MAY, "May"),
        (JUNE, "June"),
        (JULY, "July"),
        (AUGUST, "August"),
        (SEPTEMBER, "September"),
        (OCTOBER, "October"),
        (NOVEMBER, "November"),
        (DECEMBER, "December")
    )

    month_name = models.IntegerField(choices=MONTH_NAME_CHOICES)
    year = models.IntegerField()
    month_beginning_date = models.DateField()
    month_end_date = models.DateField()
    slug = models.SlugField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def name(self):
        return "{} {}".format(self.get_month_name_display(), self.year)

    def __str__(self):
        return self.name


class MonthBudget(models.Model):
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    month = models.OneToOneField(Month, on_delete=models.CASCADE)

    @property
    def name(self):
        return "{} {}".format(self.month.name, 'budget')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    months = models.ManyToManyField(Month, through='MonthCategory')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class MonthCategory(models.Model):
    category_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @property
    def name(self):
        return "{} - {}".format(self.month.name, self.category.name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Month categories"


class Expense(models.Model):
    name = models.CharField(max_length=128)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    month_category = models.ForeignKey(MonthCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
