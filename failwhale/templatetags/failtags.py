from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string
from failwhale.models import Summize
import re

register = template.Library()

AT_RE = re.compile(r'@(?P<screen_name>[\w_]+)')
HASH_RE = re.compile(r'#(?P<tag>[\w_]+)')

@register.simple_tag
def summize(name):
    results = Summize.objects.get(name=name).statuses.all()
    return render_to_string('failwhale/templatetags/summize.html', {"results": results})

@register.filter
@stringfilter
def tweetile(text):
    
    def repl_at(match):
        screen_name = match.group('screen_name')
        return '<a href="http://twitter.com/%s">@%s</a>' % (screen_name, screen_name)
        
    def repl_hash(match):
        tag = match.group('tag')
        return '<a href="http://search.twitter.com/search?q=%s">@%s</a>' % ("%23" + tag, tag)
        
    text = AT_RE.sub(repl_at, text)
    text = HASH_RE.sub(repl_hash, text)
    
    return text