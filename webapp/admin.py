from django.contrib import admin
from webapp.models import CodeUrl, CodeHistory


class CodeUrlAdmin(admin.ModelAdmin):
    list_display = ['uri', 'lang', 'code']

admin.site.register(CodeUrl, CodeUrlAdmin)

class CodeHistoryAdmin(admin.ModelAdmin):
    list_display = ['uri', 'lang', 'code']

admin.site.register(CodeHistory, CodeHistoryAdmin)
