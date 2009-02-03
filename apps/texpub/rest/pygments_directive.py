from docutils import nodes
from docutils.parsers.rst.directives import register_directive

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from fnet.dotlexer import DOTLexer
from fnet.sketchlexer import SketchLexer

pygments_formatter = HtmlFormatter()
# Initialize the Pygments directive
def pygments_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    try:
        if arguments:
            lexer = get_lexer_by_name(arguments[0])
        else:
            raise ValueError
    except ValueError:
        # no lexer found - use the text one instead of an exception
        if arguments:
            lang = arguments[0]
        else:
            lang = 'text'
        if lang=='dot':
            lexer = DOTLexer()
        if lang=='sketch':
            lexer = SketchLexer()
        else:
            lexer = get_lexer_by_name('text')
    parsed = highlight(u'\n'.join(content), lexer, pygments_formatter)
    return [nodes.raw('', parsed, format='html')]
pygments_directive.arguments = (0, 1, 1)
pygments_directive.content = 1

def register():
    register_directive('sourcecode', pygments_directive)