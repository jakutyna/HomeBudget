from django.contrib import admin

from .models import Month, MonthBudget, Category, MonthCategory, Expense


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ('name', 'month_beginning_date', 'month_end_date', 'user')


@admin.register(MonthBudget)
class MonthBudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget', 'user')

    def user(self, obj):
        return obj.month.user


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


@admin.register(MonthCategory)
class MonthCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_budget', 'user')

    def user(self, obj):
        return obj.month.user


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'expense_amount', 'month_category', 'user')

    def user(self, obj):
        return obj.month_category.month.user
