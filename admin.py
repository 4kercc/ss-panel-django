from django.contrib import admin

from .models import User, Flow, In, Out


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'port', 'password', 'setup_date', 'end_date')
    list_display_links = ('user',)
    list_filter = ('status',)

    
class FlowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'bandwidth')
    list_display_links = ('user',)
    
    
class InAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'user', 'num', 'memo')
    list_display_links = ('user',)


class OutAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'log', 'num', 'memo')
    list_display_links = ('log',)


admin.site.register(User, UserAdmin)
admin.site.register(Flow, FlowAdmin)
admin.site.register(In, InAdmin)
admin.site.register(Out, OutAdmin)
