# -*- coding: utf-8 -*-

import os
import sys
import logging as log
try:
    import Image
except:
    from PIL import Image
    
# utiltiy functions

#def resize_image(imgfilename,source_dpi=400.0, dest_dpi=100.0,maxsize = FIGSIZE):
#    im = Image.open(imgfilename)
#    w,h = im.size
#    scale = dest_dpi/source_dpi
#    nw = int(w*scale)
#    nh = int(h*scale)
#    newsize = (nw, nh)
#    if nw > maxsize[0] or nh > maxsize[1]:
#        newsize = maxsize
#    im.thumbnail(newsize, Image.ANTIALIAS)
#    dest = 'm'+imgfilename
#    im.save(dest, "PNG", optimize=True)
#    return dest


def make_image_grid(imagelist, xdim, ydim):
    """Place images in a grid"""
    w, h = FIGSIZE
    cellw = int(w/xdim)
    cellh = int(h/ydim)
    cellsize = cellw, cellh
    gridimg = Image.new('RGB',FIGSIZE,(255,255,255))
    log.debug('Cellsize: %s',cellsize)
    if (xdim*ydim) <> len(imagelist):
        log.warning('Grid dimension %s,%s does not with number of images: %s',xdim,ydim,len(imagelist))
    x = 0
    y = 0
    for img in imagelist:
        img.thumbnail(cellsize,Image.ANTIALIAS)
        nw, nh = img.size
        if cellh > nh:
            yextra = (cellh-nh)/2.0
        else:
            yextra = 0
        gridimg.paste(img,(x*cellw,y*cellh+int(yextra)))
        log.warning('x: %s  y: %s',x,y)
        if x < (xdim-1):
            x +=1
        else:
            x = 0
            y += 1
    return gridimg

def create_pdf(texfile,use_pdftex=True):
    dirname, filename = os.path.split(texfile)
    cwd = os.getcwd()
    os.chdir(dirname)
    if not os.path.splitext(filename)[1]:
        fn = os.path.basename(filename)+'.tex'
    else:
        fn = os.path.basename(filename)
    if sys.platform=='win32':
        syscmd = 'texify --pdf --clean %s' % (fn)
    else:
        syscmd = 'pdflatex -halt-on-error -interaction nonstopmode %s' % (fn)
    err = runcmd(syscmd)
    os.chdir(cwd)
    return err

def runcmd(syscmd):
    #err = os.system(syscmd)
    sres = os.popen(syscmd)
    resdata =  sres.read()
    err = sres.close()
    if err:
        log.warning('Failed to run command:\n%s',syscmd)
        log.debug('Output:\n%s',resdata)
    return err

class TeXWriter(object):
    """\
    Compiles a TeX source file and creates a PDF, PNGs and thumbnails
    """
    THUMBSIZE = 200,200
    FIGSIZE = 500,500
    def __init__(self, tex_source, slug='', page=None, grid=None):
        pass
        self.tex_source = tex_source
        if slug:
            self.slug = slug
        else:
            self.slug = 'tmp'
        self.page = page
        self.grid = grid
        self.images = {}
            
    def make_pdf(self):
        err = create_pdf(self.texfn_path)
        if not err:
            self.pdf_path = os.path.splitext(self.texfn_path)[0]+'.pdf'
            
    def make_image(self):
        gscmd = "%(cmdname)s -dNOPAUSE -r%(dpi)i -dGraphicsAlphaBits=4 -dTextAlphaBits=4 -sDEVICE=png16m -sOutputFile=%(output)s -dBATCH %(input)s"
        gsopts = dict(dpi=400)
        if sys.platform=='win32':
            gsopts["cmdname"] = "gswin32c"
        else:
            gsopts = "gs"
        
        if not (self.page or self.grid):
            img_path = os.path.splitext(self.texfn_path)[0]+'.png'
            gsopts['input'] = self.pdf_path
            gsopts['output'] = img_path
            err = runcmd(gscmd % gsopts)
            if not err:
                self.img_path = img_path
        # generate thumbnail
        if self.grid:
            #im = gridimg.copy()
            pass
        else:
            im = Image.open(self.img_path)
        im.thumbnail(self.THUMBSIZE, Image.ANTIALIAS)
        self.images['thumb'] = im
        im = Image.open(self.img_path)
        im.thumbnail(self.FIGSIZE, Image.ANTIALIAS)
        self.images['fig'] = im
        
        
    
    def process(self):
        # create a temporary directory
        self.dest_dir = r'd:\latex\tmp2'
        self.tex_fn = self.slug + '.tex'
        self.texfn_path = os.path.join(self.dest_dir, self.tex_fn)
        f = open(self.texfn_path,'w')
        # write tex file
        f.write(self.tex_source)
        f.close()
        # compile tex source
        err = self.make_pdf()
        if err:
            return False
        # generate PNGs
        err = self.make_image()
        # clean up
        
    def clean_up(self):
        pass
        
        
        
    

def make_img(c, fullfilename, name,data, page=None, grid=None):
        filename = os.path.splitext(fullfilename)[0]
        dest = os.path.normpath(os.path.join(MEDIA_DIR,'TEX',name+'.tex'))
        ##copyifnewer(name+'.tex', dest)
        f = open(dest,'w')
        f.write(data)
        f.close()
        if SKIP_PDF:
            return
        if data.find('remember picture') > -1 or data.find('GNUPLOT') > -1:
            os.system('pdflatex --shell-escape %s' % filename)
        os.system('mppdf %s' % filename)
        if not (page or grid):
            os.system('mpng %s.pdf %s' % (filename, filename))
            imgfilename = filename
        else:
            if not page:
                page = "1"
            os.system('mpng %s.pdf %s%%i' % (filename, filename))
            imgfilename = filename+page
            files = glob.glob('%s[0-9].png' % filename)
            imlist = [Image.open(f) for f in files]
            if grid:
                xdim,ydim = grid
                gridimg = make_image_grid(imlist,xdim,ydim)
            else:
                w,h = imlist[0].size
                panorama = Image.new('RGB',(w*len(imlist),h),(255,255,255))
                for i in range(len(imlist)):
                    panorama.paste(imlist[i],(i*w,0))
                panorama.thumbnail(FIGSIZE, Image.ANTIALIAS)

        #dest = os.path.normpath(os.path.join(MEDIA_DIR,'DOT',file+'.txt'))
        #copyifnewer(file, dest)
        dest = os.path.normpath(os.path.join(MEDIA_DIR,'PDF',name+'.pdf'))
        copyifnewer(filename+'.pdf', dest)

        # generate thumbnail
        if grid:
            im = gridimg.copy()
        else:
            im = Image.open(imgfilename+'.png')
        im.thumbnail(THUMBSIZE, Image.ANTIALIAS)
        dest = os.path.normpath(os.path.join(MEDIA_DIR,'thumbs',name+'.jpg'))
        im.save(dest, "JPEG", quality=95)
        im = Image.open(imgfilename+'.png')
        im.thumbnail(FIGSIZE, Image.ANTIALIAS)
        dest = os.path.normpath(os.path.join(MEDIA_DIR,'PNG',name+'.png'))
        if grid:
            im = gridimg
        elif page:
            tmpim = Image.new('RGB',(im.size[0],im.size[1]+panorama.size[1]))
            tmpim.paste(im,(0,0))
            tmpim.paste(panorama,(0,im.size[1]))
            im = tmpim

        im.save(dest, "PNG", optimize=True)
        
if __name__ == '__main__':
    source = r"""
\documentclass{article}
\usepackage[usenames,dvipsnames,pdftex]{xcolor}
\usepackage{tikz,ifthen}
%%%<
\usepackage{verbatim}
\usepackage[active,tightpage]{preview}
\PreviewEnvironment{tikzpicture}
\setlength\PreviewBorder{5pt}%
%%%>
\begin{document}
\newcounter{density}
\setcounter{density}{20}
\begin{tikzpicture}
    \def\couleur{MidnightBlue}
    \path[coordinate] (0,0)  coordinate(A)
                ++( 60:12cm) coordinate(B)
                ++(-60:12cm) coordinate(C);
    \draw[fill=\couleur!\thedensity] (A) -- (B) -- (C) -- cycle;
    \foreach \x in {1,...,15}{%
        \pgfmathsetcounter{density}{\thedensity+10}
        \setcounter{density}{\thedensity}
        \path[coordinate] coordinate(X) at (A){};
        \path[coordinate] (A) -- (B) coordinate[pos=.15](A)
                            -- (C) coordinate[pos=.15](B)
                            -- (X) coordinate[pos=.15](C);
        \draw[fill=\couleur!\thedensity] (A)--(B)--(C)--cycle;
    }
\end{tikzpicture}
\end{document}
    """
    writer = TeXWriter(source, slug='test')
    writer.process()
    