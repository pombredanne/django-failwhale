STATUS = 0
FRIEND_STATUS = 1
DIRECT_MESSAGE = 2
SEARCH_RESULT = 3

from django.utils import simplejson
from failwhale.models import Account, Status, Summize, Timeline
import datetime
import email
import failwhale
import twitter
import urllib, urllib2

SEARCH_URL = "http://search.twitter.com/search.json"

def load_account(username):
    try:
        return Account.objects.get(username=username)
    except Account.DoesNotExist:
        return create_account(username, check_if_exists=False)

def create_account(username, password=None, check_if_exists=True):
    if check_if_exists:
        assert Account.objects.filter(username=username).count() == 0
    accnt = Account()
    accnt.username = username
    accnt.password = password
    if password:
        import_profile(accnt)
    return accnt

def delete_account(username):
    try:
        Account.objects.get(username=username).delete()
    except Account.DoesNotExist:
        pass

def import_profile(accnt, save=True):
    client = twitter.Api(username=accnt.username, password=accnt.password)
    user = client.GetUser(accnt.username)
    accnt.twitter_id = user.id
    accnt.full_name = user.name
    accnt.location = user.location
    accnt.description = user.description
    accnt.avatar_url = user.profile_image_url
    accnt.url = user.url
    if save:
        accnt.save()

def import_search_results(summize, since_id=None):
    
    params = {'q': summize.query}
    if since_id:
        params['since_id'] = since_id
    url = "%s?%s" % (SEARCH_URL, urllib.urlencode(params))
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'django-failwhale')]
    response = opener.open(url)
    content = response.read()
    response.close()
    
    json = simplejson.loads(content)
    results = json['results']
    
    for result in results:
        
        to_user = load_account(result['from_user'])
        
        if not to_user.avatar_url == result['profile_image_url']:
            to_user.avatar_url = result['profile_image_url']
            to_user.save()
            
        time_tuple = email.utils.parsedate(result['created_at'])
        created_at = datetime.datetime(*time_tuple[0:7])
        
        try:
            s = Status.objects.get(pk=result['id'])
        except Status.DoesNotExist:
            s = Status.objects.create(
                id=result['id'],
                sender=to_user,
                message=result['text'],
                timestamp=created_at,
            )
            
        if summize.statuses.filter(timeline__status=s, timeline__discriminator=failwhale.SEARCH_RESULT).count() == 0:
        
            t = Timeline.objects.create(
                owner=summize,
                status=s,
                discriminator=failwhale.SEARCH_RESULT,
            )
