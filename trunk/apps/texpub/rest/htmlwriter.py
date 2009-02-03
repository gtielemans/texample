"""
Code to do the ReST --> HTML generation for the docs.
"""

#Most of the code in this file is based on the ReST documentation writer used
#by the Django project prior to Djano 1.0:
#
#Copyright (c) Django Software Foundation and individual contributors.
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification,
#are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#    
#    2. Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of Django nor the names of its contributors may be used
#       to endorse or promote products derived from this software without
#       specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import re

import smartypants
from docutils import nodes
from docutils.core import publish_parts
from docutils.writers import html4css1


class TeXHTMLWriter(html4css1.Writer):
    """
    HTML writer that adds a "toc" key to the set of doc parts.
    """
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = TeXHTMLTranslator

    def translate(self):
        # build the document
        html4css1.Writer.translate(self)
        self.fnetinfo = self.translator_class.info
        #print self.translator_class.info

        # build the contents
        contents = self.build_contents(self.document)
        contents_doc = self.document.copy()
        contents_doc.children = contents
        contents_visitor = self.translator_class(contents_doc)
        contents_doc.walkabout(contents_visitor)
        self.parts['toc'] = "<ul class='toc'>%s</ul>" % ''.join(contents_visitor.fragment)

    def build_contents(self, node, level=0):
        level += 1
        sections = []
        i = len(node) - 1
        while i >= 0 and isinstance(node[i], nodes.section):
            sections.append(node[i])
            i -= 1
        sections.reverse()
        entries = []
        autonum = 0
        depth = 4   # XXX FIXME
        for section in sections:
            title = section[0]
            entrytext = title
            try:
                reference = nodes.reference('', '', refid=section['ids'][0], *entrytext)
            except IndexError:
                continue
            ref_id = self.document.set_id(reference)
            entry = nodes.paragraph('', '', reference)
            item = nodes.list_item('', entry)
            if level < depth:
                subsects = self.build_contents(section, level)
                item += subsects
            entries.append(item)
        if entries:
            contents = nodes.bullet_list('', *entries)
            return contents
        else:
            return []

class TeXHTMLTranslator(html4css1.HTMLTranslator):
    """
    reST -> HTML translator subclass that fixes up the parts of docutils I don't like.
    """
    
    # Prevent name attributes from being generated
    named_tags = []
    info = {}
    
    def __init__(self, document):
        html4css1.HTMLTranslator.__init__(self, document)
        self._in_literal = 0
        self._in_fnetfield = 0
        self.use_fnet_docinfo = True
        
    def visit_docinfo(self, node):
        if self.use_fnet_docinfo:
            # A quick hack to supress docinfo output
            self.tmpbody = self.body
            self.body = []
            self.in_docinfo = 1
        else:
            html4css1.HTMLTranslator.visit_docinfo(self, node)

    def depart_docinfo(self, node):
        if self.use_fnet_docinfo:
            self.body = self.tmpbody
            self.in_docinfo = None
        else:
            html4css1.HTMLTranslator.depart_docinfo(self, node)
            
        
    def visit_field_name(self, node):
        if self.in_docinfo and self.use_fnet_docinfo:
            self.current_fieldname = node.astext()
            self.info[self.current_fieldname] = 'xx'
        html4css1.HTMLTranslator.visit_field_name(self, node)
   
    def visit_field_body(self, node):
        if self.in_docinfo and self.use_fnet_docinfo:
            self.info[self.current_fieldname] = node.astext()
        html4css1.HTMLTranslator.visit_field_body(self, node)

    def visit_topic(self, node):
        if 'abstract' in node['classes']:
            self.tmpbody2 = self.body
            self.body = []
        else:
            html4css1.HTMLTranslator.visit_topic(self, node)
        
    def depart_topic(self,node):
        if 'abstract' in node['classes']:
            self.info[u'summary']= "".join(self.body[3:])
            self.body = self.tmpbody2
        else:
            html4css1.HTMLTranslator.depart_topic(self, node)
        
    # Remove the default border=1 from <table>    
    def visit_table(self, node):
        self.body.append(self.starttag(node, 'table', CLASS='docutils'))
    
    #
    # Apply smartypants to content when not inside literals
    #
    def visit_literal_block(self, node):
        self._in_literal += 1
        html4css1.HTMLTranslator.visit_literal_block(self, node)

    def visit_option(self, node):
        self._in_literal += 1
        html4css1.HTMLTranslator.visit_option(self, node)
        
    def depart_literal_block(self, node):
        html4css1.HTMLTranslator.depart_literal_block(self, node)
        self._in_literal -= 1
        
    def depart_option(self, node):
        html4css1.HTMLTranslator.depart_option(self, node)
        self._in_literal -= 1
     
    def visit_literal(self, node):
        self._in_literal += 1
        try:
            html4css1.HTMLTranslator.visit_literal(self, node)
        finally:
            self._in_literal -= 1
     
    def encode(self, text):
        text = html4css1.HTMLTranslator.encode(self, text)
        if self._in_literal <= 0:
            text = smartypants.smartyPants(text, "qde")
        return text
    
    #
    # Avoid <blockquote>s around merely indented nodes.
    # Adapted from http://thread.gmane.org/gmane.text.docutils.user/742/focus=804
    #
    
    _suppress_blockquote_child_nodes = (
        nodes.bullet_list, nodes.enumerated_list, nodes.definition_list,
        nodes.literal_block, nodes.doctest_block, nodes.line_block, nodes.table
    )
    def _bq_is_valid(self, node):
        return len(node.children) != 1 or not isinstance(node.children[0], self._suppress_blockquote_child_nodes)
                                        
    def visit_block_quote(self, node):
        if self._bq_is_valid(node):
            html4css1.HTMLTranslator.visit_block_quote(self, node)

    def depart_block_quote(self, node):
        if self._bq_is_valid(node):
            html4css1.HTMLTranslator.depart_block_quote(self, node)
        
    
