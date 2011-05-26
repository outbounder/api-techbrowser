import google.appengine.ext.webapp.template
import logging
from django.template import Node, TemplateSyntaxError, resolve_variable, VariableDoesNotExist

register = google.appengine.ext.webapp.template.create_template_register()

def resolve_variable_or_string(s, context):
    """s may be a variable or a quoted string.

    If s is a quoted string, unquote it and return it.  If s is a variable, 
    resolve it and return it.
    """
    if len(s) > 0:
        if not s[0] in ("'", '"'):
            value = s
            try:
                value = resolve_variable(s, context)
            except VariableDoesNotExist:
                pass
            return value
        if s[-1] == s[0]:
            s = s[:-1]                  # Strip trailing quote, if any.
            s = s[1:]                   # Strip starting quote.
    return s

def resolve_string(s):
    """s may be a variable or a quoted string.

    If s is a quoted string, unquote it and return it.  If s is a variable, 
    resolve it and return it.
    """
    if len(s) > 0:
        if s[-1] == s[0]:
            s = s[:-1]                  # Strip trailing quote, if any.
            s = s[1:]                   # Strip starting quote.
    return s

def make_mvc_url(controller, action, id):
    url = "/%s/%s" % (controller, action)
    if id is not None and len(id) > 0:
        url += "/%s" % id
        
    return url

def make_anchor(link_text, link):
    return "<a href='%s'>%s</a>" % (link, link_text)

class anchor_node(Node):
    def __init__(self, link_text, controller, action, id, params, unless_current=True):
        self.link_text = link_text
        self.controller = controller
        self.action = action
        self.id = id
        self.params = params
        self.unless_current = unless_current
        
    def render(self, context):
        return_value = ""
        requested_url = make_mvc_url(self.controller, self.action, self.id)
        
        if self.unless_current:
            # Create a link only if the link the we are creating is for a
            # page that is not currently being displayed. Determine the
            # page that is currently being displayed by retrieving the
            # controller, action and id variables from the current context
            # these value are set by MVCEngine.
            current_controller = resolve_variable_or_string("controller", context)
            current_action = resolve_variable_or_string("action", context)
            current_id = resolve_variable_or_string("id", context)
            current_url = make_mvc_url(current_controller, current_action, current_id)
            
            if requested_url == current_url:
                return_value = "<span>%s</span>" % self.link_text
            else:
                return_value = make_anchor(self.link_text, requested_url)
        else:
            # Since unless_current is false, we are going to create the link no matter
            # what.
            return_value = make_anchor(self.link_text, requested_url)
            
        return return_value
        
@register.tag
def link_to_unless_current(parser, token):
    """Create an HTML anchor tag for the given controller, action, id and
    parameters with the text given in link_text. If the link being created
    is for the page that is currently being displayed, just display link_text
    in a span instead of an anchor."""
    try:
        import shlex
        tag, link_text, controller, action, id, params = shlex.split(str(token.contents))
    except ValueError:
        raise TemplateSyntaxError("link_to_unless_current tag requires 5 arguments")
    
    return anchor_node(link_text, controller, action, id, params)


class pagination_control(Node):
    def __init__(self, collection, url_format, prev_text, next_text):
        self.collection = collection
        self.url_format = url_format
        self.prev_text = prev_text
        self.next_text = next_text

        self.url_format = url_format
        self.collection_name = collection
        
    def _class_for(self, is_current=False):
        the_class = "%s_page" % self.collection_name
        if is_current:
            the_class += "_current"
            
        return the_class

    def _make_anchor(self, context, anchor_text, page_number):
        url_format = resolve_variable_or_string(self.url_format, context)
        href = url_format % page_number
        anchor = "<a class=\"paginator_page %s\" href=\"%s\">%s</a>" % (self._class_for(), href, anchor_text)
        
        return anchor

    def render(self, context):
        paged_collection = resolve_variable(self.collection, context)
        
        result = ""
        
        if hasattr(paged_collection, "page_count"):
            control_id = resolve_string(self.collection) + "_paginator"
            result = "<div id=\"%s\" class=\"paginator_control\">" % control_id
            
            previous_page_text = resolve_string(self.prev_text)

            if paged_collection.previous_page > 0:
                result += self._make_anchor(context, previous_page_text, paged_collection.previous_page)
            else:
                result += "<span class=\"paginator_inactive %s\">%s</span>" % (self._class_for(is_current=True), previous_page_text)
                
            for each_page in xrange(1, paged_collection.page_count + 1):
                if each_page == paged_collection.current_page:
                    result += "<span class=\"paginator_curr_page %s\">%d</span>" % (self._class_for(is_current=True), each_page)
                else:
                    result += self._make_anchor(context, str(each_page), each_page)
            
            next_page_text = resolve_string(self.next_text)
            if paged_collection.next_page > 0:
                result += self._make_anchor(context, next_page_text, paged_collection.next_page)
            else:
                result += "<span class=\"paginator_inactive %s\">%s</span>" % (self._class_for(is_current=True), next_page_text)
            
        
            result += "</div>"
        
        return result
            
#@register.tag
def page_control_for(parser, token):
    try:
        import shlex
        tag, collection, url_format, prev_text, next_text = shlex.split(str(token.contents))
    except ValueError:
        raise TemplateSyntaxError("page_control_for requires 1 argument")
    
    return pagination_control(collection, url_format, prev_text, next_text)
page_control_for = register.tag(page_control_for)

def cached_block(parser, token):
    """
    Define a block that can be overridden by child templates.
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError, "'%s' tag takes only one argument" % bits[0]
    block_name = bits[1]
    # Keep track of the names of BlockNodes found in this template, so we can
    # check for duplication.
    try:
        if block_name in parser.__loaded_blocks:
            raise TemplateSyntaxError, "'%s' tag with name '%s' appears more than once" % (bits[0], block_name)
        parser.__loaded_blocks.append(block_name)
    except AttributeError: # parser.__loaded_blocks isn't a list yet
        parser.__loaded_blocks = [block_name]
    nodelist = parser.parse(('endblock', 'endblock %s' % block_name))
    parser.delete_first_token()
    return BlockNode(block_name, nodelist)
