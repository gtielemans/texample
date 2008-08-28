"""
Various utilities for publishing
"""

from BeautifulSoup import BeautifulSoup
import re
import os, datetime

from django.template.defaultfilters import slugify,striptags

def build_toc(text_or_tagsoup, toc_css_class="toc"):
    """Build a table of contents and return it as an unordred nested list"""
    if isinstance(text_or_tagsoup,BeautifulSoup):
        soup = text_or_tagsoup
    else:
        soup = BeautifulSoup(text_or_tagsoup)
    headings = soup.findAll(re.compile(r'h\d'))
    toc = u'<ul class="%s">\n' % toc_css_class
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
    
    return toc, soup

def copy_if_newer(source, dest):
    """Copy source to dest if dest is older than source or doesn't exists
    
    If the dest directory does not exist it will be created. 
    """
    copy = False
    # Check that dest exists. Create dir if necessary
    if os.path.exists(dest):
        # get source's and dest's timpestamps
        source_ts = os.path.getmtime(source)
        dest_ts = os.path.getmtime(dest)
        # compare timestamps
        if source_ts > dest_ts: copy = True
    else:
        copy = True
        dir = os.path.dirname(dest)
        if dir != '' and not os.path.exists(dir):
            os.makedirs(dir)
    # copy source to dest
    if copy:
        shutil.copy2(source, dest)


def iso_to_datetime(isodate):
    """Convert an isodate formatted string to a datetime object"""
    try:
        year,month, day = map(int,isodate.split('-'))
        return datetime(year, month, day)
    except:
        return None

# Read text
# Convert to html
# Extract title, toc, related links, metadata
# Should return
# 'title'
# 'Author'
# 'slug'
# '

