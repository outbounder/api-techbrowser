from google.appengine.ext.webapp.template import create_template_register
import logging
from django.template import Node, TemplateSyntaxError, resolve_variable, VariableDoesNotExist

register = create_template_register()

def split_and_keep_quotes(to_split):
    """This is an alternative to shlex.split() that will preserve quoted strings without
    removing the quotes."""
    import shlex
    
    splitter = shlex.shlex(to_split)
    tokens = []
    
    try:
        while True:
            tokens.append(splitter.next())
    except StopIteration:
        pass
    
    return tokens

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


class text_input_node(Node):
    def __init__(self, name, validated, parameters):
        self.name = name
        self.validated = validated
        self.parameters = parameters
        
    def render(self, context):
        value = ""
        try:
            value = resolve_variable(self.name, context)
        except VariableDoesNotExist:
            pass
                
        node_text = "<input type='text' name='%s'" % self.name
        for each_param in self.parameters:
            node_text += " %s" % each_param
        if value is not None and len(value) > 0:
            node_text += " value='%s'" % value
        node_text += "/>"
                
        return node_text

@register.tag
def text_input(parser, token):
    raw_parameters = token.split_contents()
    
    name = raw_parameters[1]
    validated = False
    parameters = []
    
    for each_param in raw_parameters[2:]:
        # Are we dealing with a name/value pair?
        try:
            n,v = each_param.split("=")
            name_lowered = n.lower().strip()
            if name_lowered == "name":
                raise TemplateSyntaxError, "Specify the name of the input field as the first parameter"
            parameters.append(each_param)
        except ValueError:
            # This parameter is atomic
            lowered = each_param.lower().strip()
            if lowered == "validated":
                validated = True
            else:
                parameters.append(each_param)
    
    return text_input_node(name, validated, parameters)

class checkbox_input_node(Node):
    def __init__(self, name, validated, checked, parameters):
        self.name = name
        self.validated = validated
        self.checked = checked
        self.parameters = parameters
        
    def render(self, context):
        value = ""
        try:
            value = resolve_variable_or_string(self.name, context)
        except VariableDoesNotExist:
            pass
        
        node_text = "<input type='checkbox' name='%s'" % self.name
        if self.checked or (value is not None and len(value) > 0) :
            node_text += " CHECKED"
            
        for each_param in self.parameters:
            node_text += " %s" % each_param
        node_text += "/>"
                
        return node_text

@register.tag
def checkbox_input(parser, token):
    raw_parameters = token.split_contents()
    
    name = raw_parameters[1]
    validated = False
    checked = False
    parameters = []
    
    for each_param in raw_parameters[2:]:
        # Are we dealing with a name/value pair?
        try:
            n,v = each_param.split("=")
            name_lowered = n.lower().strip()
            if name_lowered == "name":
                raise TemplateSyntaxError, "Specify the name of the input field as the first parameter"
            elif name_lowered == "checked":
                checked = True
            else:
                parameters.append(each_param)
        except ValueError:
            # This parameter is atomic
            lowered = each_param.lower().strip()
            if lowered == "validated":
                validated = True
            else:
                parameters.append(each_param)
    
    return checkbox_input_node(name, validated, checked, parameters)

class validation_error_node(Node):
    def __init__(self, name, spanclass):
        self.name = name
        self.spanclass = spanclass
        
    def render(self, context):
        error = None
        try:
            error = resolve_variable("validation_errors.%s" % self.name, context)
        except VariableDoesNotExist:
            pass
        
        node_text = ""
        
        if error:
            node_text = "<span class='%s'>%s</span>" % (self.spanclass, error)
        
        return node_text

@register.tag
def validation_error(parser, token):
    raw_parameters = token.split_contents()
    
    name = raw_parameters[1]
    spanclass = "failed_validation"
    
    if len(raw_parameters) == 3:
        spanclass = raw_parameters[2]
    elif len(raw_parameters) > 3:
        raise TemplateSyntaxError, "node takes 2 parameters; %d provided" % len(raw_parameters)
    
    return validation_error_node(name, spanclass)
