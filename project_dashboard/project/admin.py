from django.contrib import admin

from .models import Project, Expense, Category


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('name', 'slug'), 'budget')
        }),
    )
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'budget')
    list_filter = ('name',)

admin.site.register(Project, ProjectAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project')
    list_filter = ('name', 'project')

admin.site.register(Category, CategoryAdmin)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'project', 'amount')
    list_filter = ('project', 'title', 'category')

admin.site.register(Expense, ExpenseAdmin)
