from django.core.management.base import BaseCommand, CommandError
from failwhale import util
from failwhale.models import Account
    
class Command(BaseCommand):
    
    help = "Update account statuses"
    args = '([name])'
    
    requires_model_validation = False
    
    def handle(self, name=None, *args, **options):
        
        accounts = Account.objects.filter(passwd__isnull=False)
        for account in accounts:
            util.import_profile(account)
            util.import_statuses(account)