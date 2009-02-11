from django import forms
from django.contrib import admin
from failwhale.models import Account, Summize

# account

class AccountAdminForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['passwd']
    
class AccountAdmin(admin.ModelAdmin):
    form = AccountAdminForm
    list_display = ['username']
    list_display_links = ['username']

admin.site.register(Account, AccountAdmin)
admin.site.register(Summize)
