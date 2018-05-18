from django.contrib import admin

from .models import ProcessGroup, KnowledgeArea, Process


# Register your models here.
class ProcessGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class KnowledgeAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class ProcessAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'slug', 'process_group', 'knowledge_area']
    list_filter = ('process_group', 'knowledge_area')
    search_fields = ['name', 'process_group', 'knowledge_area']
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(ProcessGroup, ProcessGroupAdmin)
admin.site.register(KnowledgeArea, KnowledgeAreaAdmin)
admin.site.register(Process, ProcessAdmin)

