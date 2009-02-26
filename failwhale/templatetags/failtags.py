from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string
from failwhale.models import Summize
import re

register = template.Library()

AT_RE = re.compile(r'@(?P<screen_name>[\w_]+)')
HASH_RE = re.compile(r'#(?P<tag>[\w_]+)')
HTTP_RE = re.compile(r'(?P<url>http://[\w_/\.]+)')

@register.simple_tag
def summize(name, count=5):
    results = Summize.objects.get(name=name).related_statuses.all()[:count]
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
    
    def repl_http(match):
        url = match.group('url')
        return '<a href="%s">%s</a>' % (url, url)
        
    text = HTTP_RE.sub(repl_http, text)
    text = AT_RE.sub(repl_at, text)
    text = HASH_RE.sub(repl_hash, text)
    
    return text