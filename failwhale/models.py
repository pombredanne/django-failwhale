from django.db import models
import datetime
import failwhale

# account and search models

class Syncable(models.Model):

    related_statuses = models.ManyToManyField('Status', through='Timeline')

    last_update = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    next_update = models.DateTimeField(blank=True, null=True)
    ttl = models.IntegerField(default=5)

class Account(Syncable):
    
    username = models.CharField(max_length=32)
    passwd = models.CharField(max_length=32, blank=True, null=True)
    
    # profile
    twitter_id = models.IntegerField(blank=True, null=True)
    full_name = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=180, blank=True)
    url = models.URLField(verify_exists=False, blank=True, null=True)
    avatar_url = models.URLField(verify_exists=False, blank=True, null=True)
    is_protected = models.BooleanField(default=False)
    friend_count = models.IntegerField(default=-1)
    
    def __unicode__(self):
        return self.username
    
    def _get_password(self):
        return self.passwd
    
    def _set_password(self, password):
        self.passwd = password
        self.save()
        
    password = property(_get_password, _set_password)
    
    def statuses(self):
        return self.related_statuses.filter(timeline__discriminator=failwhale.STATUS)
    def friend_statuses(self):
        return self.related_statuses.filter(timeline__discriminator=failwhale.FRIEND_STATUS)
    def direct_messages(self):
        return self.related_statuses.filter(timeline__discriminator=failwhale.DIRECT_MESSAGE)

class Summize(Syncable):
    name = models.CharField(max_length=128, blank=True)
    query = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name
    
    def save(self):
        if not self.name:
            self.name = self.query
        super(Summize, self).save()
    
# tweet models

class Status(models.Model):
    sender = models.ForeignKey(Account, related_name="nigh_related_statuses")
    recipient = models.ForeignKey(Account, related_name="received_dms", blank=True, null=True)
    message = models.CharField(max_length=180)
    timestamp = models.DateTimeField()
    
    class Meta:
        ordering = ('-timestamp',)
    
    def __unicode__(self):
        return "%s: %s" % (self.sender.username, self.message)
    
    def is_dm(self):
        return not self.recipient == None
        
    def timestamp_est(self):
        return self.timestamp - datetime.timedelta(0, 60 * 60 * 5) # off five hours

# timeline model

TIMELINE_TYPES = (
    (failwhale.STATUS, 'status'),
    (failwhale.FRIEND_STATUS, 'friend status'),
    (failwhale.DIRECT_MESSAGE, 'direct message'),
    (failwhale.SEARCH_RESULT, 'search result'),
)

class Timeline(models.Model):
    discriminator = models.IntegerField(choices=TIMELINE_TYPES)
    owner = models.ForeignKey(Syncable, related_name="timeline")
    status = models.ForeignKey(Status, related_name="timeline")
    
    class Meta:
        unique_together = ('discriminator','owner','status')