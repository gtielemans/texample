"""Template tags for splitting lists into columns.


Original source:
http://www.djangosnippets.org/snippets/889/
http://herself.movielady.net/2008/07/16/split-list-to-columns-django-template-tag/

"""



from django.template import Library, Node
     
register = Library()

class SplitListNode(Node):
    def __init__(self, list, cols, new_list):
        self.list, self.cols, self.new_list = list, cols, new_list

    def split_seq(self, list, cols=2):
        start = 0 
        for i in xrange(cols): 
            stop = start + len(list[i::cols]) 
            yield list[start:stop] 
            start = stop

    def render(self, context):
        context[self.new_list] = self.split_seq(context[self.list], int(self.cols))
        return ''



def list_to_columns(parser, token):
    """Parse template tag: {% list_to_colums list as new_list 2 %}"""
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "list_to_columns list as new_list 2"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to the list_to_columns tag must be 'as'"
    return SplitListNode(bits[1], bits[4], bits[3])

class QSplitListNode(Node):
    """A variant of SplitListNode for querysets.
    
    Forces the evaluation of the queryset prior to splitting the list. This
    reduces the number of 
    """
    def __init__(self, tlist, cols, new_list):
        self.tlist, self.cols, self.new_list = tlist, cols, new_list

    def split_seq(self, tlist, cols=2):
        start = 0
        # Force evaluation of queryset to save some hits on the database
        nlist = list(tlist)
        for i in xrange(cols): 
            stop = start + len(nlist[i::cols]) 
            yield nlist[start:stop] 
            start = stop

    def render(self, context):
        context[self.new_list] = self.split_seq(context[self.tlist], int(self.cols))
        return ''



def qlist_to_columns(parser, token):
    """Parse template tag: {% list_to_colums list as new_list 2 %}"""
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "list_to_columns list as new_list 2"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to the list_to_columns tag must be 'as'"
    return QSplitListNode(bits[1], bits[4], bits[3])

    
list_to_columns = register.tag(list_to_columns)
qlist_to_columns = register.tag(qlist_to_columns)