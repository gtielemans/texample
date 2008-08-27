"""
Various utilities for publishing
"""

from BeautifulSoup import BeautifulSoup
import re

def build_toc(text):
    """Build a table of contents and return it as an unordred nested list"""
    soup = BeautifulSoup(text)
    headings = soup.findAll(re.compile(r'h\d'))
    toc = u'<ul class="toc">\n'
    current_level = 2
    first = True
    for heading in headings:
        level = int(heading.name[-1])
        if level == 1:
            # skip <h1>
            continue

        heading_title = heading.renderContents()
        heading_id = heading.get('id',None)
        if not heading_id:
            heading_id = slugify(striptags(heading_title))
            heading['id'] = heading_id
        if level == current_level:
            if first:
                toc += u'<li><a href="#%s">%s</a>' % (heading_id,heading_title)
                first = False
            else:
                toc += u'</li>\n<li><a href="#%s">%s</a>' % (heading_id,heading_title)
        elif level > current_level:
            toc += u'<ul>\n<li><a href="#%s">%s</a>' % (heading_id,heading_title)
        elif level < current_level:
            toc += u'</li></ul></li><li><a href="#%s">%s</a>' % (heading_id,heading_title)

        current_level = level
    toc += u'</li></ul>\n'
    
    return toc