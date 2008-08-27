from pygments.lexer import RegexLexer, bygroups, using
from pygments.token import *
from pygments.lexers.text import TexLexer
import re

class SketchLexer(RegexLexer):
    name = 'Sketch'
    aliases = ['sketch']
    filenames = ['*.sk']
    #flags = re.DOTALL
    tokens = {
        'root': [
            (r'[^\S\n]+', Text),
            (r'%.*?\n', Comment),
            (r'[]{}:(),;[]', Punctuation),
            (r"[-+/*^.']", Operator),
            (r'special\s*',Keyword.Reserved,'special'),
            (r'(picturebox|curve|def|dots|frame|'
             r'global|input|line|polygon|put|repeat|set|sweep|then)\b',Keyword),
            (r'(atan2|cos|inverse|perspective|project|rotate|scale|'
             r'sin|special|sqrt|translate|unit|view)\b',Keyword.Reserved),
            ('[a-zA-Z_][a-zA-Z0-9]*', Name),
            (r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?', Number),
            (r'\d+', Number),
            (r'.*\n', Text),
        ],
        'special': [
        (r'(?P<delim>\w|[|$])(.|\s)*?(?P=delim)',using(TexLexer),
             '#pop'),

        ]
    }




if __name__ == '__main__':
    from pygments import highlight
    from pygments.formatters import HtmlFormatter, RawTokenFormatter
    code=r"""
% Vector cross product
def O (0,0,0) % origin
def theta 60 % angle between U and V
def U 2*[1,0,0]
def V rotate(theta)*[U]
% Define styles
% The use of the [lay=under] option forces the code to be outputted
% at the beginning of the generated code. The default behavior is to
% output special at the end.
special |\tikzstyle{vector}=[-latex',very thick]
            \tikzstyle{angle}=[->,shorten >=1pt]|[lay=under]


def scene {
    def u (O)+[U]
    def v (O)+[V]
    def w (O)+[U]*[V]
    line[line style=vector] (O)(u)
    line[line style=vector] (O)(v)
    line[line style=vector] (O)(w)
    special |\path #1 node[below] {$\vec{u}$}
                   #2 node[below] {$\vec{v}$}
                   #3 node[above] {$\vec{u}\times\vec{v}$};|(u)(v)(w)
    % Annotate theta angle. Sketch currently does not support
    % curves. Use a curve path instead, with appropriate computed
    % startpoint, midpoint and endpoint.
    def s (O) + 0.5*[U]
    def m rotate(theta/2)*(s)
    def e rotate(theta)*(s)
    special |\draw[angle] #1..controls #2.. node[midway,below] {$\theta$}#3;|
        (s)(m)(e)
}

put { view((2,0.5,2),(O),[0,0,1]) } {scene}
global { language tikz }
"""
    print highlight(code, SketchLexer(),HtmlFormatter())
    f = open('d:\pycode\experiments\sketch.html','w')
    highlight(code, SketchLexer(), HtmlFormatter(full=True,style='colorful'),f)
    f.close()
    
    