from django.core.management.base import BaseCommand, CommandError
from failwhale import util
from failwhale.models import Summize
    
class Command(BaseCommand):
    
    help = "Update summize searches"
    args = '([name])'
    
    requires_model_validation = False
    
    def handle(self, name=None, *args, **options):
        
        summizes = Summize.objects.all()
        for summize in summizes:
            util.import_search_results(summize)