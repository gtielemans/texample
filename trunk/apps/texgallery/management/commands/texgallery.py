from django.core.management.base import BaseCommand,CommandError

import os, glob,md5,cPickle
import optparse
import logging
import re
import codecs
from django.template.defaultfilters import slugify


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

class CodeProcessor(object):
    """
    A class for extracting and processing meta information from source files.
    """
    def __init__(self):
        self.cmnts_re = re.compile(r"(\s*\\begin{comment}.*?\\end{comment})\s*",re.DOTALL | re.MULTILINE)
        self.crop_re = re.compile(r"(\s*%%%<.*?%%%>\s*)", re.DOTALL | re.MULTILINE)
        self.tags_re = re.compile(r"^\s*:Tags: (.*?)$", re.MULTILINE)
        self.spes_re =re.compile(r"^\s*:(.*?):(.*?)$", re.MULTILINE)

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
        d = re.sub(self.tags_re,'\n', d)
        d = d.replace('\\begin{preview}','')
        d = d.replace('\\end{preview}','')
        return re.sub(self.crop_re,'\n',d)
        
    def extract_meta_data(self,data):
        """Extracts meta data and returns a key=value dict"""
        m = self.spes_re.findall(data)
        d = {}
        for key, val in m:
            d[key.strip().lower()] = val.strip()
        return d
    
    def process(self,filename):
        """Processes source file and return a dictionary"""
        try:
            data = codecs.open(filename,encoding='utf8').read()
        except (IOError, OSError):
            logging.exception('Failed to load %s',filename)
            
        comments = self.extract_comment(data)
        data = self.remove_extra_markup(data)
        metadata = self.extract_meta_data(comments)
        #logging.debug(metadata)
        #extract necessary info
        info = {}
        info['title'] = metadata.get('title','')
        info['slug'] = metadata.get('slug',None)\
                        or slugify(metadata.get('title',''))
        info['content_html'] = self.format_content()
        logging.debug(info)
        
        

    
                    

class Command(BaseCommand):
    help == "Perform various TeXgallery administration tasks"
    EXAMPLES_DIR = []
    MD5FILE = ''
    def handle(self, *args, **options):
        from django.conf import settings
        # initialize settings
        if hasattr(settings,'TEXGALLERY_EXAMPLES_DIR'):
            self.EXAMPLES_DIR = settings.TEXGALLERY_EXAMPLES_DIR
        else:
            raise CommandError('No examples dir')
        
        if hasattr(settings,'TEXGALLERY_MD5FILE'):
            self.MD5FILE = settings.TEXGALLERY_MD5FILE
        else:
            raise CommandError('No MD5 file')
        
        # no options. Check for new and changed files
        new_files, changed_files = self.find_changed_files()
        fp = CodeProcessor()
        if new_files:
            print "New files:\n%s" % "\n".join(new_files)
            for f in new_files:
                fp.process(f)
        if changed_files:
            print "Changed files:\n%s" % "\n".join(changed_files)
            
        

    def find_changed_files(self):
        """Finds new and changed files and return a (new, changed) tuple"""
        # build a list of all available examples
        filelist = []
        for exdir in self.EXAMPLES_DIR:
            os.chdir(exdir)
            for f in glob.glob("*.tex"):
                filelist.append(os.path.join(exdir,f))
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
        return (new_files, changed_files)            