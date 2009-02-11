from django.core.management.base import BaseCommand, CommandError
import failwhale
    
class Command(BaseCommand):
    
    help = "Register a Twitter account"
    args = '[username] ([password])'
    
    requires_model_validation = False
    
    def handle(self, username=None, password=None, *args, **options):
        
        if not username:
            raise CommandError('Usage is register_twit %s' % self.args)
        
        failwhale.create_account(username, password)