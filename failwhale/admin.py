from django import forms
from django.contrib import admin
from failwhale.models import Account, Status, Summize, Timeline

# account

class TimelineInline(admin.TabularInline):
    model = Timeline

class SummizeAdmin(admin.ModelAdmin):
    inlines = (TimelineInline,)
    
class AccountAdminForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['passwd']
    
class AccountAdmin(admin.ModelAdmin):
    form = AccountAdminForm
    list_display = ['username']
    list_display_links = ['username']

admin.site.register(Account, AccountAdmin)
admin.site.register(Summize, SummizeAdmin)
