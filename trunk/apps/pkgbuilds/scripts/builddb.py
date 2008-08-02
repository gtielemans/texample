# set up the django environment
import os,sys,glob,datetime,time,zipfile,difflib,itertools
import re

import os.path as opath

from itertools import izip
os.environ["DJANGO_SETTINGS_MODULE"] = 'texample.settings'

BUILDS_DIR = "d:/pgfbuilds"
BASE_DIR = opath.dirname(__file__)

DIR_PREFIX = 'pgf/builds/'

def get_zips():
    """Return a list of zip builds"""
    cwd = os.getcwd()
    os.chdir(BUILDS_DIR)
    filelist = [opath.join(BUILDS_DIR,fn) for fn in glob.glob("*_TDS.zip")]
    os.chdir(cwd)
    filelist.sort()
    return filelist


def get_diff(fromdata,todata,stripws=True):
    d = difflib.ndiff(fromdata,todata)
    dlines = []
    for line in d:
        if line.startswith('+ '):
            if stripws:
                dlines.append(line[2:].strip())
            else:
                dlines.append(line[2:])
        else:
            break
    if stripws:
        return "\n".join(dlines)
    else:
        return "".join(dlines)

def hide_email(text):
    return re.sub("[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}", "...",text)

def nsplit(seq, n=2):
    """Split a sequence into pieces of length n

    If the lengt of the sequence isn't a multiple of n, the rest is discareded.
    Note that nsplit will strings into individual characters.

    Examples:
    >>> nsplit('aabbcc')
    [('a', 'a'), ('b', 'b'), ('c', 'c')]
    >>> nsplit('aabbcc',n=3)
    [('a', 'a', 'b'), ('b', 'c', 'c')]

    # Note that cc is discarded
    >>> nsplit('aabbcc',n=4)
    [('a', 'a', 'b', 'b')]
    """
    return [xy for xy in izip(*[iter(seq)]*n)]

# Code snippet from Python Cookbook, 2nd Edition by David Ascher, Alex Martelli
# and Anna Ravenscroft; O'Reilly 2005
def windows(iterable, length=2, overlap=0,padding=True):
    it = iter(iterable)
    results = list(itertools.islice(it, length))
    while len(results) == length:
        yield results
        results = results[length-overlap:]
        results.extend(itertools.islice(it, length-overlap))
    if padding and results:
        results.extend(itertools.repeat(None, length-len(results)))
        yield results


from pkgbuilds.models import Build
from texample import settings as djangosettings



if __name__ == '__main__':
    zips = get_zips()
    basefn = opath.join(BASE_DIR,'ChangeLog.base')
    basechangelog = open(basefn,'rb').readlines()
    
    prev_changelog = ['']
    for fn in zips:
        fd = datetime.datetime.fromtimestamp((opath.getctime(fn)))
        # ugly hack to remove second from timestamp
        file_date = datetime.datetime(fd.year,fd.month,fd.day,fd.hour,fd.minute)
        build,created = Build.objects.get_or_create(build_date=file_date)

        if created:
            build.zip_path = u"%s" % (opath.join(DIR_PREFIX,opath.basename(fn)))
            slug = 'a'
            try:
                slug = chr(ord(Build.objects.get(build_date=file_date,slug=slug)[0])+1)
            except:
                pass
            build.slug=slug
            z = zipfile.ZipFile(fn,'r')
            changelog = z.read('doc/generic/pgf/ChangeLog')
            changeloglines = changelog.splitlines(True)
            changelog = get_diff(basechangelog,changeloglines,stripws=False)
            #print changelog.splitlines(True)
            build.changelog = hide_email(changelog)
            # look for documentation
            docfn = "pgfmanualCVS%s-%02d-%02d.pdf" % (fd.year,fd.month,fd.day)
            if opath.exists(opath.normpath(opath.join(BUILDS_DIR,docfn))):
                build.doc_path = opath.join(DIR_PREFIX,docfn)
            build.save()
            print build
            z.close()

    builds = Build.objects.all().order_by('build_date')
    for a,b in windows(builds,2,1,False):
        if not b.changes.strip():
            a_lines = a.changelog.splitlines(True)
            b_lines = b.changelog.splitlines(True)
            changes = get_diff(a_lines,b_lines)
            b.changes = changes
            b.save()







