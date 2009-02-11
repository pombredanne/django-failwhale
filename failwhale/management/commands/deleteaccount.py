from django.core.management.base import BaseCommand, CommandError
import failwhale
    
class Command(BaseCommand):
    
    help = "Delete a registered Twitter account"
    args = '[username]'
    
    requires_model_validation = False
    
    def handle(self, username=None, *args, **options):
        
        if not username:
            raise CommandError('Usage is register_twit %s' % self.args)
        
        failwhale.delete_account(username)