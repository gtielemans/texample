from django.core.management.base import BaseCommand,CommandError

import os, glob,md5,cPickle
import optparse
import logging

def build_file_md5s(filelist):
    """Calculate a hash value for each file in filelist

    Returns a dict of filename->md5hash values
    """
    filehash = {}
    for f in filelist:
        d = open(f,'rb').read()
        h = md5.new(d).hexdigest()
        filehash[f] = h
    return filehash


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
        if new_files:
            print "New files:\n%s" % "\n".join(new_files)
        if changed_files:
            print "Changed files:\n%s" % "\n".join(changed_files)
            
        

    def find_changed_files(self):
        """Find new and changed files and return (new, changed) tuple"""
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