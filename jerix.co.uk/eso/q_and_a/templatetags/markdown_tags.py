import re

from django.template import Library
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import markdown
import bleach
import pygments
from pygments import lexers
from pygments import formatters


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
    s = markdown.markdown(s, safe_mode=False)
    s = bleach.clean(s, safe_tags, safe_attr, strip=True)
    return mark_safe(s)

regex = re.compile(r'<code(.*?)>(.*?)</code>', re.DOTALL)

@register.filter(name='pygmentize')
def pygmentize(value):
    last_end = 0
    to_return = ''
    found = 0
    for match_obj in regex.finditer(value):
        # code_class = match_obj.group(1)
        code_string = match_obj.group(2)
        #         if code_class.find('class') > -1:
        #             language = re.split(r'"|\'', code_class)[1]
        #             lexer = lexers.get_lexer_by_name(language)
        #         else:
        #             try:
        #                 lexer = lexers.guess_lexer(str(code_string))
        #             except ValueError:
        #                 lexer = lexers.PythonLexer()
        #         pygmented_string = pygments.highlight(code_string, lexer, formatters.HtmlFormatter(nowrap=True))
        to_return = (to_return + value[last_end:match_obj.start(0)] +
                    '<code class="default prettyprint">' + code_string + #pygmented_string +
                    '</code>')
        last_end = match_obj.end(2)
        found = found + 1
    to_return = to_return + value[last_end:]
    return mark_safe(to_return)