from pygments.lexer import RegexLexer, bygroups, using
from pygments.token import *
from pygments.lexers.text import TexLexer
import re

class DOTLexer(RegexLexer):
    name = 'DOT'
    aliases = ['dot']
    filenames = ['*.dot']
    #flags = re.DOTALL
    #flags = re.MULTILINE | re.DOTALL
    tokens = {
        'root': [
            
            (r'[^\S\n]+', Text),
            #(r'//.*?\n', Comment),
            #(r'/\*.*?\*/', Comment),
            (r'/(\\\n)?/(\n|(.|\n)*?[^\\]\n)', Comment),
            (r'/(\\\n)?[*](.|\n)*?[*](\\\n)?/', Comment),
            #(r'[]{}:(),;[]', Punctuation),
            (r'(node|edge|graph|digraph|subgraph|strict)\b',Keyword),
            #(r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?', Number),
            #(r'\d+', Number),
            (r'.*\n', Text),
        ],
    }


if __name__ == '__main__':
    from pygments import highlight
    from pygments.formatters import HtmlFormatter, RawTokenFormatter
    code=r"""
   //comment
   /* mulitline
   comment */
digraph G {
        a_1 [texlbl="$\frac{\gamma}{2x^2+y^3}$"];
        a_1 -> a_2 -> a_3 -> a_1
        node [texmode="math"]; //comment
        a_1 -> b_1 -> b_2 -> a_3;
        b_1 [label="\\frac{\\gamma}{x^2}"];
        node [texmode="verbatim"]
        b_4 [label="\\beta"]
        a_3 -> b_4 -> a_1;
    }
"""
    print highlight(code, DOTLexer(),HtmlFormatter())
   
    