from django.db import models
from django.utils.text import slugify


# Create your models here.
class Project(models.Model):
    """
    Project model
    Project(id, name, slug, budget)
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField(
        help_text='Amount allocated to this project.'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def budget_left(self):
        """ Budget amount left after expenses """
        expense_list = Expense.objects.filter(project=self)
        total_expense_amount = 0
        for expense in expense_list:
            total_expense_amount += expense.amount

        return self.budget - total_expense_amount

    def total_transactions(self):
        """ Count of total transactions for Project """
        expense_list = Expense.objects.filter(project=self)
        return len(expense_list)


class Category(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name='categories')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Expense(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-amount', )
