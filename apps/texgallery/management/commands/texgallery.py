# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand,CommandError

import os, glob,md5,cPickle
import optparse
import logging
import re
import codecs
from django.template.defaultfilters import slugify
from texpub.rest import TeXHTMLWriter
from django.conf import settings
from texpub.texwriter import TeXWriter
import pygments
from BeautifulSoup import BeautifulSoup
from texpub.texwriter import TeXWriter
import urlparse
import shutil

def build_file_md5s(filelist):
    """Calculates a hash value for each file in filelist

    Returns a dict of filename->md5hash values
    """
    filehash = {}
    for f in filelist:
        d = open(f,'rb').read()
        h = md5.new(d).hexdigest()
        filehash[f] = h
    return filehash

def copyifnewer(source, dest):
    """Copy source to dest if dest is older than source or doesn't exists"""
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

def restructuredtext(text):
    from docutils.core import publish_parts
    docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
    writer = TeXHTMLWriter()
    docutils_settings['initial_header_level'] = 2
    parts = publish_parts(source=text, writer=writer,
        settings_overrides=docutils_settings)
    return parts["fragment"]


class CodeProcessor(object):
    """
    A class for extracting and processing meta information from source files.
    """
    def __init__(self, media_url=''):
        self.cmnts_re = re.compile(r"(\s*\\begin{comment}.*?\\end{comment})\s*",re.DOTALL | re.MULTILINE)
        self.crop_re = re.compile(r"(\s*%%%<.*?%%%>\s*)", re.DOTALL | re.MULTILINE)
        self.tags_re = re.compile(r"^\s*:Tags: (.*?)$", re.MULTILINE)
        self.spes_re =re.compile(r"^\s*:(.*?):(.*?)$", re.MULTILINE)
        self.media_url = media_url

    def extract_comment(self,data):
        """Extracts comment and meta section from source"""
        comments = re.findall(r"\\begin{comment}(.*?)\\end{comment}", data, re.DOTALL)
        if comments:
            return comments[0]
        else:
            return ""
        
    def remove_extra_markup(self,data):
        """Removes unnecessary markup"""
        d =  re.sub(self.cmnts_re,'\n',data)
        #d = re.sub(self.tags_re,'\n', d)
        d = d.replace('\\begin{preview}','')
        d = d.replace('\\end{preview}','')
        return re.sub(self.crop_re,'\n',d)
        
    def remove_extra_comments(self,data):
        return re.sub(self.tags_re,'\n', data)
        
    def extract_meta_data(self,data):
        """Extracts meta data and returns a key=value dict"""
        m = self.spes_re.findall(data)
        d = {}
        for key, val in m:
            d[key.strip().lower()] = val.strip()
        return d
    
    def create_content_html(self,content):
        """Creates a HTML version of the content/decription"""
        content_html = restructuredtext(content)
        return content_html
        
    def highlight_code(self,code):
        """Returns a syntax highlighted HTML version of the code"""
        return pygments.highlight(code, pygments.lexers.TexLexer(),
            pygments.formatters.HtmlFormatter(encoding='utf-8'))
     
    def process_locallinks(self, text_or_tagsoup):
        if isinstance(text_or_tagsoup,BeautifulSoup):
            soup = text_or_tagsoup
        else:
            soup = BeautifulSoup(text_or_tagsoup)
        local_src = soup.findAll(src=re.compile(r'^(?!http:).*?'))
        local_href = soup.findAll(href=re.compile(r'^(?!http:).*?'))
        local_links = []
        for src in local_src:
            src_l = src['src']
            src['src'] = self.media_url + src_l
            local_links.append(src_l)
        for href in local_href:
            href_l = href['href']
            href['href'] = self.media_url + href_l
            local_links.append(href_l)
        
        return soup, local_links
        
    def process(self,filename):
        """Processes source file and return a dictionary"""
        try:
            data = codecs.open(filename,encoding='utf8').read()
        except:
            logging.exception('Failed to load %s',filename)
            return {}
            
        comments = self.extract_comment(data)
        data = self.remove_extra_markup(data)
        metadata = self.extract_meta_data(comments)
        #logging.debug(metadata)
        #extract necessary info
        info = {}
        info['title'] = metadata.get('title','')
        info['slug'] = metadata.get('slug',None)\
                        or slugify(metadata.get('title',''))
        content_html = self.create_content_html(self.remove_extra_comments(comments))
        soup, local_links = self.process_locallinks(content_html)
        info['content_html'] = str(soup)
        info['code_html'] = self.highlight_code(data)
        info['code_tex'] = data
        grid = metadata.get('grid')
        if grid:
            try:
                xdim, ydim = map(int,grid.split('x'))
                info['grid'] = (xdim, ydim)
            except:
                log.warning('Failed to parse grid metadata %s', grid)
                info['grid'] = None
        else:
            info['grid'] = None
        page = metadata.get('page')
        if page:
            try:
                info['page'] = page
            except:
                log.warning('Invalid page: %s', page)
                info['page'] = "1"
        else:
            info['page'] = "1"
        return info
    

        
class Command(BaseCommand):
    help == "Perform various TeXgallery administration tasks"
    EXAMPLES_DIR = []
    MD5FILE = ''
    FILEPATTERN = '*.tex'
    SOURCE_PREFIX = 'TEX'
    PDF_PREFIX = 'PDF'
    PNG_PREFIX = 'PNG'
    THUMBS_PREFIX = 'thumbs'
    option_list = BaseCommand.option_list + (
        optparse.make_option('--forcehashupdate',
            action='store_true', dest='force_hashupdate', default=False,
            help='Update hash db without processing modified files'),
        optparse.make_option('-a','--add', dest='add_filename',
            help='Add file'),
        optparse.make_option('--addall',
            action='store_true', dest='add_all', default=False,
            help='Add all new examples'),
        optparse.make_option('--skippdf',
            action='store_true', dest='skip_pdf', default=False,
            help='Skip creation of PDF and images'),
        optparse.make_option('--updateall',
            action='store_true', dest='update_all', default=False,
            help='Update all modified examples'),
    )
    def handle(self, *args, **options):
        from django.conf import settings
        #from texgallery.models import ExampleEntry
        # initialize settings
        if hasattr(settings,'TEXGALLERY_EXAMPLES_DIR'):
            self.EXAMPLES_DIR = settings.TEXGALLERY_EXAMPLES_DIR
        else:
            raise CommandError('No examples dir')
        
        if hasattr(settings,'TEXGALLERY_MD5FILE'):
            self.MD5FILE = settings.TEXGALLERY_MD5FILE
        else:
            raise CommandError('No MD5 file')
        
        
        if hasattr(settings,'TEXGALLERY_MEDIA_DIR'):
            self.MEDIA_DIR = settings.TEXGALLERY_MEDIA_DIR
        else:
            raise CommandError('No media dir')
            #pass
        
        self.media_url = urlparse.urljoin(getattr(settings,'MEDIA_URL',''),
            getattr(settings,'TEXGALLERY_MEDIA_PREFIX',''))
        
        # no options. Check for new and changed files
        new_files, changed_files = self.find_changed_files()
        force_hashupdate = options.get('force_hashupdate')
        add_all = options.get('add_all')
        update_all = options.get('update_all')
        self.skip_pdf = options.get('skip_pdf')
        if force_hashupdate:
            print "Force hash"
            self.stored_hashes = self.hashes
            self.write_hashdb()
            return
            pass
        
        if add_all:
            for f in new_files:
                self.add_example(f)
            self.write_hashdb()
            return
        
        if update_all:
            for f in changed_files:
                self.add_example(f)
            self.write_hashdb()
            return
        
        fp = CodeProcessor(media_url=self.media_url)
        if new_files:
            print "New files:\n" 
            for f in new_files:
                info = fp.process(f)
                ##pp = TeXWriter(open(f).read())
                ##pp.process()
                if len(info.keys()) == 0:
                    continue
                print "Filename: %s\nTitle: %s\nSlug: %s\n----" %\
                    (f,info['title'],info['slug'])
                #print info['content_html']
                
        if changed_files:
            print "Changed files:\n%s" % "\n".join(changed_files)
    
    def write_hashdb(self):
        if self.stored_hashes:
            f = open(self.MD5FILE,'w')
            cPickle.dump(self.stored_hashes, f)
            f.close()
            logging.info('Wrote hash db %s',self.MD5FILE)
         
    def add_example(self, filepath):
        fp = CodeProcessor(media_url=self.media_url)
        # get information about example
        info = fp.process(filepath)
        source_code = open(filepath).read()
        print "Processing %s" % info['title']
        print "Slug: %s" % info['slug']
        # create PDF and images
        if not self.skip_pdf:
            try:
                texwriter = TeXWriter(source_code, slug=info['slug'], grid=info['grid'], page=info['page'])
                err = texwriter.process()
                if err:
                    logging.error('Failed to compile %s', filepath)
                    return
            except:
                logging.error('Failed to compile %s', filepath)
                return
            # save tex-file to dest
            dest_tex_fn = os.path.join(self.MEDIA_DIR,'TEX',info['slug']+'.tex')
            dest_tex_file = open(dest_tex_fn,'w')
            dest_tex_file.write(source_code)
            dest_tex_file.close()
            #print dest_tex_fn
            #print info['code_tex'][1:1000]
            # save png
            dest_png_fn = os.path.join(self.MEDIA_DIR,'PNG',info['slug']+'.png')
            texwriter.images['fig'].save(dest_png_fn, "PNG", optimize=True)
            # save pdf
            dest_pdf_fn = os.path.join(self.MEDIA_DIR,'PDF',info['slug']+'.pdf')
            copyifnewer(texwriter.pdf_path, dest_pdf_fn)
            # save thumb
            dest_thumb_fn = os.path.join(self.MEDIA_DIR,'thumbs',info['slug']+'.jpg')
            texwriter.images['thumb'].save(dest_thumb_fn, "JPEG", quality=80)
            logging.info('PDF and images created for %s', info['slug'])
        self.update_db(info)
        # update hash db
        self.stored_hashes[filepath] = self.hashes[filepath]
        
        
    def update_db(self, info):
        """Add example to db"""
        from django.db.models import get_model
        ExampleEntry = get_model('texgallery','ExampleEntry')
        #from texgallery.models import ExampleEntry
        example, created = ExampleEntry.objects.get_or_create(slug=info['slug'])
        #mediaentry.__dict__.update(entry)
        example.title = info['title']
        example.slug = info['slug']
        
        example.content = info['code_html']
        example.description = info['content_html']
        
        example.save()
        logging.info('%s written to db', info['slug'])
        
        

    def find_changed_files(self):
        """Finds new and changed files and return a (new, changed) tuple"""
        # build a list of all available examples
        filelist = []
        cwd = os.getcwd()
        for exdir in self.EXAMPLES_DIR:
            os.chdir(exdir)
            for f in glob.glob(self.FILEPATTERN):
                filelist.append(os.path.join(exdir,f))
        os.chdir(cwd)
        # generate hash values
        hashes = build_file_md5s(filelist)
        
        # load md5 database
        try:
            f = open(self.MD5FILE,'r')
            stored_hashes = cPickle.load(f)
            f.close()
        except:
            logging.exception('Failed lo load hash file %s',self.MD5FILE)
            stored_hashes = {}
        
        changed_files = []
        new_files = []
        
        for fn, h in hashes.items():
            if stored_hashes.get(fn):
                if not stored_hashes[fn] == h:
                    changed_files.append(fn)
            else:
                new_files.append(fn)
        
        # compare current examples with stored list
        logging.info('New files %s',new_files)
        logging.info('Changed files %s',changed_files)
        self.hashes = hashes
        self.stored_hashes = stored_hashes
        return (new_files, changed_files)            