from django.core.management.base import BaseCommand, CommandError
import failwhale
    
class Command(BaseCommand):
    
    help = "Update summize searches"
    args = '([name])'
    
    requires_model_validation = False
    
    def handle(self, name=None, *args, **options):
        
        summizes = failwhale.models.Summize.objects.all()
        for summize in summizes:
            failwhale.import_search_results(summize)