from django.template import Library
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import markdown
import bleach

safe_tags = [
            'b', 'blockquote', 'code', 'del', 'dd', 'dl', 'dt', 'em', 'h1',
            'h2', 'h3', 'i', 'kbd', 'li', 'ol', 'p', 'pre', 's', 'sup', 'sub',
            'strong', 'strike', 'ul'
]

safe_attr = {
    'a': ['href', 'rel', 'title'],
    'img': ['src', 'alt', 'title', 'width', 'height']
}

register = Library()

@register.filter('markdown')
@stringfilter
def markdown_tag(s):
    print s
    s = markdown.markdown(s, safe_mode=False)
    print s
    s = bleach.clean(s, safe_tags, safe_attr, strip=True)
    print s
    return mark_safe(s)