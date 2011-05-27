import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
import logging
import os
import sys
import itertools
from google.appengine.ext.webapp.util import run_wsgi_app
from libs import simplejson

logging.getLogger().setLevel(logging.DEBUG)

# Classes that are returned by Controller Actions to specify the result
# of the Action
class ActionResult(object):
    """
    ActionResult is the required parent class of any class that can be returned
    by a controller action to define what view-rendering action should be
    taken.
    """
    def __init__(self, context):
        self.context = context

    def Render(self, context):
        """
        The Render method is called by MVCEngine to create the View that will be
        returned to the client.
        """
        raise NotImplementedError, "Classes inherting from ActionResult must provide a new implementation of Render"

class MVCActionResult(ActionResult):
    """
    A parent class for any ActionResult that refers to components of the MVC
    Framework, controllers, actions and ids.
    """
    def __init__(self, context, controller=None, action=None, id=None):
        super(MVCActionResult, self).__init__(context)
        if controller is None:
            self.controller = context.controller
        else:
            self.controller = controller

        if action is None:
            self.action = context.action
        else:
            self.action = action

        if id is None:
            self.id = context.id
        else:
            self.id = id

class RenderView(MVCActionResult):
    def __init__(self, context, controller=None, action=None, as_string=False, filetype="html"):
        super(RenderView, self).__init__(context, controller=controller, action=action)
        self.filetype = filetype
        self.as_string = as_string

    def Render(self):
        from gaemvclib import mvctemplaterender
        path = "%s/%s.%s" % (self.controller, self.action, self.filetype)

        rendered = mvctemplaterender.render(path, self.context.view_data)
        if self.as_string:
            return rendered
        else:
            self.context.response.out.write(rendered)

class RedirectToAction(MVCActionResult):
    """An Action should return this when the result of the Action is that the
    the client is redirected to any combination of a different controller,
    action, id.  If permanent is true, the client will receive a 301
    status code; otherwise, the redirection will be performed logically by
    the MVC Engine.

    * controller = the name of a controller that will be used to handle the
      request.  If it is not specified, the current controller will be used.
    * action = the name of the action that will be used to handle the request.
      If it is not specified, the current action will be used.
    * id = the id that will be passed to the specified action.  If it is not
      specified, no id will be passed.
    """
    def __init__(self, context, controller=None, action=None, id=None, permanent=False):
        super(RedirectToAction, self).__init__(context, controller=controller, action=action, id=id)
        self.permanent = permanent

    def Render(self):
        url = "/" + self.controller + "/" + self.action
        try:
            url += "/" + self.id
        except:
            pass
        self.context.handler.redirect(url, permanent=self.permanent)

class RedirectToUrl(ActionResult):
    """An Action should return this when the result of the Action is that the
    the client is redirected to a new URL.  If permanent is true, the client
    will receive a 301 status code.

    * url = the complete, fully-qualified URL to which the client will be
      redirected.
    """
    def __init__(self, context, url, permanent=False):
        super(RedirectToUrl, self).__init__(context)
        self.url = url
        self.permanent = permanent

    def Render(self):
        self.context.handler.redirect(self.url, permanent=self.permanent)

class RenderString(ActionResult):
    """An Action can return this when it provides a string that is
    simply returned to the client."""
    def __init__(self, context, content):
        super(RenderString, self).__init__(context)
        self.content = content

    def Render(self):
        self.context.response.out.write(self.content)

class RenderError(ActionResult):
    """An Action should return this when the result of the Action is an
    unhandlable error condition which corresponds to an HTTP Error status
    code, 4** or 5**.

    * status = the HTTP status code to be returned to the client.
    """
    def __init__(self, context, status):
        super(RenderError, self).__init__(context)
        self.status = status

    def Render(self):
        self.context.handler.error(self.status)

class ActionResultSetException(Exception):
    def __init__(self, action_result):
        self.action_result = action_result

class Filter(object):
    """
    Filter is the superclass for any class that wants to participate in the
    the request Call Chain and have the chance to modify the data or
    behavior in some way.
    
    In addition to providing the interface that a filter class must implement,
    this class also provides static methods for declaring that a particular
    filter is to be applied to a particular object.
    
    Filters are either before-filters or after-filters; they either run before
    calls to the object to which are they attached or after calls.
    
    Filters can be applied to individual actions methods, all action methods,
    and entire controllers.
    
    For more information on the Call Chain, see the Call Chain section in the
    documentation file, MVCEngine.html.
    """
    before_all_actions_filters = []
    after_all_actions_filters = []
    before_all_controllers_filters = []
    after_all_controllers_filters = []

    def execute(self, context):
        """
        Any Filter must implement this method.  It is called when the filter's
        position in the Call Chain is reached.  There are  no restrictions on
        what a filter can do, but the only data that it has to operate on is
        the MVCContext object that is passed in.
        
        The execute method should return one of the three values,
        Filter.STOP, Filter.CONTINUE or Filter.ERROR.
        """
        raise NotImplementedError, "Classes that inherit Filter need to provide an implementation of execute"

    STOP = 0
    "Indicates that the Call Chain should end for reasons other than an error."
    CONTINUE = 1
    "Indicates that the Call Chain chain should continue executing."
    ERROR = 2
    "Indicates that Call Chain should end because an error occured."

    @staticmethod
    def before(object, filter):
        """
        Add filter to object such that it is executed before the
        object's behavior is called in the Call Chain.
        """
        if not hasattr(filter, "execute"):
            raise TypeError, "An object that is set to be a filter must implement method 'execute(self, MVCContext)'"
        if not hasattr(object, "before_filters"):
            setattr(object, "before_filters", [])
        object.before_filters.append(filter)

    @staticmethod
    def before_all_actions(filter):
        """
        Add filter to the collection of filters that is executed before all
        actions.
        """
        Filter.before_all_actions_filters.append(filter)

    @staticmethod
    def before_all_controllers(filter):
        """
        Add filter to the collection of filters that is executed before all
        actions.
        """
        Filter.before_all_controllers_filters.append(filter)

    @staticmethod
    def after_all_actions(filter):
        """
        Add filter to the collection of filters that is executed after all
        actions.
        """
        Filter.after_all_actions_filters.append(filter)

    @staticmethod
    def after_all_controllers(filter):
        """
        Add filter to the collection of filters that is executed after all
        actions.
        """
        Filter.after_all_controllers_filters.append(filter)

    @staticmethod
    def after(object, filter):
        """
        Add filter to object such that it is executed after the
        object's behavior is called in the Call Chain.
        """
        if not filter is Filter:
            raise TypeError, "An object that is set to be a filter must inherit from the class Filter."
        if not hasattr(object, "after_filters"):
            setattr(object, "after_filters", [])
        object.after_filters.append(filter)

    @staticmethod
    def run_filter(filter, context):
        filter_instance = filter()
        return filter_instance.execute(context)

    @staticmethod
    def run_before_filters(object, context):
        filter_result = Filter.CONTINUE
        if hasattr(object, "before_filters"):
            for before_filter in getattr(object, "before_filters"):
                filter_result = Filter.run_filter(before_filter, context)
                if filter_result != Filter.CONTINUE:
                    break

        return filter_result

    @staticmethod
    def run_before_action_filters(context):
        filter_result = Filter.CONTINUE
        for before_filter in Filter.before_all_actions_filters:
            filter_result = Filter.run_filter(before_filter, context)
            if isinstance(filter_result, ActionResult):
                pass
            elif filter_result != Filter.CONTINUE:
                break

        return filter_result

    @staticmethod
    def run_before_controllers_filters(context):
        filter_result = Filter.CONTINUE
        for before_filter in Filter.before_all_controllers_filters:
            filter_result = Filter.run_filter(before_filter, context)
            if isinstance(filter_result, ActionResult):
                pass
            elif filter_result != Filter.CONTINUE:
                break

        return filter_result

    @staticmethod
    def run_after_filters(object, context):
        filter_result = Filter.CONTINUE
        if hasattr(object, "after_filters"):
            for after_filter in getattr(object, "after_filters"):
                filter_result = Filter.run_filter(after_filter, context)
                if filter_result != Filter.CONTINUE:
                    break

        return filter_result

    @staticmethod
    def run_after_action_filters(context):
        filter_result = Filter.CONTINUE
        for after_filter in Filter.after_all_actions_filters:
            filter_result = Filter.run_filter(after_filter, context)
            if isinstance(filter_result, ActionResult):
                pass
            elif filter_result != Filter.CONTINUE:
                break

        return filter_result

    @staticmethod
    def run_after_controllers_filters(context):
        filter_result = Filter.CONTINUE
        for after_filter in Filter.after_all_controllers_filters:
            filter_result = Filter.run_filter(after_filter, context)
            if isinstance(filter_result, ActionResult):
                pass
            elif filter_result != Filter.CONTINUE:
                break

        return filter_result

class HttpVerbs(object):
    INVALID = 0
    GET = 1
    POST = 2
    HEAD = 3
    PUT = 4
    DELETE = 5
    TRACE = 6
    OPTIONS = 7

    def __init__(self, verb):
        self.cur_verb = verb

    def is_get(self):
        if self.cur_verb.upper() == 'GET':
            return True
        else:
            return False

    def is_post(self):
        if self.cur_verb.upper() == 'POST':
            return True
        else:
            return False

    def is_head(self):
        if self.cur_verb.upper() == 'HEAD':
            return True
        else:
            return False

    def is_put(self):
        if self.cur_verb.upper() == 'PUT':
            return True
        else:
            return False

    def is_delete(self):
        if self.cur_verb.upper() == 'DELETE':
            return True
        else:
            return False

    def is_trace(self):
        if self.cur_verb.upper() == 'TRACE':
            return True
        else:
            return False

    def is_options(self):
        if self.cur_verb.upper() == 'OPTIONS':
            return True
        else:
            return False

    def verb(self):
        found_verb = HttpVerbs.INVALID
        if self.is_get():
            found_verb = HttpVerbs.GET
        elif self.is_post():
            found_verb = HttpVerbs.POST
        elif self.is_head():
            found_verb = HttpVerbs.HEAD
        elif self.is_put():
            found_verb = HttpVerbs.PUT
        elif self.is_delete():
            found_verb = HttpVerbs.DELETE
        elif self.is_trace():
            found_verb = HttpVerbs.TRACE
        elif self.is_options():
            found_verb = HttpVerbs.OPTIONS

        return found_verb

class MissingIDException(Exception):
    pass

class HTTPError(Exception):
    def __init__(self, code):
        self.code = code

# The Controller class definition
class Controller(object):
    "The class from which all MVCEngine Controllers must inherit."

    action_proxy_registry = {}
    "Stores all action_proxy objects."

    def __init__(self, context=None):
        if context is not None:
            assert isinstance(context, MVCContext)
            self.context = context

    class action_proxy(object):
        """The action proxy class is used by MVCEngine to implement the
        method-overloading capability that is used to implement the
        'responds_to' functionality."""
        def __init__(self, name):
            self.name = name
            self.verb_map = {HttpVerbs.GET: {}, HttpVerbs.POST: {}}

        def register(self, verb, function):
            if function.__name__ in self.verb_map[verb].keys():
                raise TypeError("The action %s is registered with the verb %s twice" % (function.__name__, verb))
            self.verb_map[verb] = function

    @classmethod
    def respond_to(cls, *verbs):
        """Specify which HTTP verb or verbs this action will handle.
        Usage:
        class book_controller(Controller):
        
          @Controller.respond_to(HttpVerbs.GET)
          def new(self):
            # Display the form that is used to create a new book entry
            return RenderView(self.context)
            
          @Controller.respond_to(HttpVerbs.POST)
          def new(self, title, author, isbn, price):
            # Handle the submission of the new book form
            new_book = Book(title, author, isbn, price)
            new_book.put()
            
            return RedirectToAction(self.context, "book", "index")
        """
        def register(function):
            name = function.__name__
            ofclass = function.__module__

            proxy = None
            try:
                proxy = cls.action_proxy_registry[ofclass][name]
            except KeyError:
                pass

            if proxy is None:
                proxy = Controller.action_proxy(name)
                if not cls.action_proxy_registry.has_key(ofclass):
                    cls.action_proxy_registry[ofclass] = {}
                cls.action_proxy_registry[ofclass][name] = proxy

            verb_list = verbs
            if not isinstance(verb_list, list) and not isinstance(verb_list, tuple):
                # Make sure that we have an iterable list
                verb_list = [verb_list]
            for each_verb in verb_list:
                proxy.register(each_verb, function)
            return proxy
        return register

    def expects_id(self, handler=None):
        """
        Declares that the following code requires that an object id
        be supplied, either in the requesting URL or in the request's
        params
        """
        success = True
        try:
            if self.context.id is None or str(self.context.id) == "0" or len(str(self.context.id)) == 0:
                id_try = self.context.request.get("id")
                if id_try == None or len(id_try) == 0:
                    success = False
                else:
                    self.context.id = id_try
        except:
            success = False

        if not success:
            if handler is None:
                # Return Bad Request status code
                self.set_action_result(RenderError(self.context, 400))
            else:
                handler()

    def admin_only(self):
        "Declares that the following code can only be run by a site administrator."
        user = users.get_current_user()
        if not user:
            if self.context.is_get():
                self.set_action_result(RedirectToUrl(self.context, users.create_login_url(self.context.request.uri)))
            else:
                self.set_action_result(RenderError(self.context, 403))
        elif not users.is_current_user_admin():
            self.set_action_result(RenderError(self.context, 403))

    def logged_in_only(self):
        "Declares that the following code can only be run by a logged-in user."
        user = users.get_current_user()
        if not user:
            if self.context.is_get():
                self.set_action_result(RedirectToUrl(self.context, users.create_login_url(self.context.request.uri)))
            self.set_action_result(RenderError(self.context, 403))

    def set_action_result(self, action_result):
        set_exception = ActionResultSetException(action_result)
        raise set_exception

    def __getattribute__(self, name):
        # Need to specially handle attribute access in order to make sure
        # that requests for a method will return a function if request is
        # for an action_proxy. All other attribute accesses are handled
        # normally.
        local_registry = object.__getattribute__(self, "action_proxy_registry")

        try:
            self_class = object.__getattribute__(self, "__class__")
            self_name = object.__getattribute__(self_class, "__name__")

            proxies_for_this_controller = local_registry[self_name]
            if name in proxies_for_this_controller.keys():
                proxy = proxies_for_this_controller[name]
                function = None
                try:
                    local_context = object.__getattribute__(self, "context")
                    function = proxy.verb_map[local_context.verb()]
                except KeyError:
                    # There are no methods registered to handle the given verb,
                    # so None will be returned.
                    pass

                return function
            else:
                # Since the requested attribute is not found in the proxy map, it is a normal
                # attribute lookup
                return object.__getattribute__(self, name)
        except KeyError:
            # The collection of proxy maps did not have an entry for this controller, which is a
            # valid state, as many simple controllers will not use @Controller.respond_to at all,
            # so treat it as a normal attribute lookup.
            return object.__getattribute__(self, name)

    # Request validation methods
    def is_not_empty(self, param, failure_message="Can not be empty"):
        """Validation method that checks that the given request parameter
        is not missing and has a value that is not the empty string.
        """
        valid = True

        try:
            value = self.context.request.params[param]

            if value is None or ((isinstance(value, unicode) or isinstance(value, str)) and len(value) == 0):
                self.context.validation_errors[param] = failure_message
                self.context.valid = False
                valid = False
        except KeyError:
            self.context.validation_errors[param] = failure_message
            self.context.valid = False
            valid = False

        return valid

    def is_checked(self, param, failure_message="Must be checked"):
        """Validation method that checks that the given request parameter,
        which is expected to come from a checkbox input field, is the
        value 'on', meaning that the checkbox is checked.
        """
        valid = True

        try:
            value = self.context.request.params[param]
            if value is None or len(value) == 0:
                self.context.validation_errors[param] = failure_message
                self.context.valid = False
                valid = False
        except KeyError:
            self.context.validation_errors[param] = failure_message
            self.context.valid = False
            valid = False

        return valid

    def is_numeric(self, param, failure_message="Must be a numeric value"):
        """Validation method that checks that the given request parameter has
        a numeric value. An empty or missing value does not trigger this
        validator; the controller should use is_not_empty to confirm that the
        input is not empty."""

        valid = True

        try:
            value = self.context.request.params[param]
            try:
                int_value = int(value)
            except ValueError:
                # The input is not numeric.
                self.context.validation_errors[param] = failure_message
                self.context.valid = False
                valid = False
        except KeyError:
            # An empty or missing value certainly isn't numeric, but we
            # don't want to go duplicating the validation that is already
            # performed by a separate validtor.
            pass

        return valid

    def redisplay_if_invalid(self, controller=None, action=None, repopulate=None):
        if not self.context.valid:
            self.context["validation_errors"] = self.context.validation_errors
            if repopulate is not None and len(repopulate) > 0:
                for each_repopulate in repopulate:
                    try:
                        self.context[each_repopulate] = self.context.request.params[each_repopulate]
                    except KeyError:
                        # Nothing to do here, it is possible that validation failed because
                        # a parameter was not provided.
                        pass

            self.set_action_result(RenderView(self.context, controller=controller, action=action))

class MVCContext(HttpVerbs):
    """An MVCContext object contains all of the data that is required to and
    available for processing a request. It is passed to every method call
    that is involved in the Call Chain, and each method is free to read from
    and write to the context in whatever way is appropriate to it performing
    its work."""

    import UserDict

    class FlashCollection(UserDict.DictMixin):
        """A collection used for handling a dictionary of values that is passed
        across requests with a cookie."""

        def __init__(self, input_flash=None):
            """input_flash can be provided to parse a FlashCollection from an
            incoming request."""
            self.__values_out = {}
            self.__values_in = {}

            if input_flash is not None:
                import base64
                import pickle

                decoded_flash = base64.b64decode(input_flash)
                self.__values_in = pickle.loads(decoded_flash)
                logging.debug("input_flash = %s" % str(self.__values_in))

        def __getitem__(self, key):
            if key in self.__values_in:
                return self.__values_in[key]
            else:
                return None

        def __setitem__(self, key, value):
            self.__values_out[key] = value

        def __contains__(self, key):
            return key in self.__values_in

        def input_keys(self):
            "List of keys in the dictionary for the Flash object that was received from the request."
            keys = None
            if self.__values_in is not None:
                keys = self.__values_in.keys()

            return keys

        def output_keys(self):
            "List of keys in the dictionary for the Flash object that will be sent with the response."
            keys = None
            if self.__values_out is not None:
                keys = self.__values_out.keys()

            return keys

        def serialize(self):
            import base64
            import pickle

            pickled_flash = pickle.dumps(self.__values_out)
            return base64.b64encode(pickled_flash)

        def as_cookie(self, domain):
            from Cookie import SimpleCookie
            cookie = SimpleCookie()
            if len(self.__values_out) > 0:
                cookie["flash"] = self.serialize()
                cookie["flash"]["expires"] = 86400 # Expire 24 hours from now
                cookie["flash"]["path"] = "/"
            else:
                # Since nothing has been stored in the output value list, all we want to do
                # is to expire the Flash cookie that is already stored on the client, as the
                # Flash is valid only for one request.
                cookie["flash"] = ""
                cookie["flash"]["expires"] = -360 # Expire 3 minutes ago.
                cookie["flash"]["path"] = "/"


            output = cookie.output(header='')

            return output


    def __init__(self, request_handler, request_url, router, view_data):
        self.handler = request_handler
        self.request = request_handler.request
        self.response = request_handler.response
        self.request_url = request_url
        self.router = router
        self.view_data = view_data
        self.params = self.request.params
        self.get = self.request.get
        self.validation_errors = {}
        self.valid = True

        try:
            self.flash = MVCContext.FlashCollection(self.request.cookies["flash"])
            self.view_data["flash"] = self.flash
        except KeyError:
            self.flash = MVCContext.FlashCollection()

        routes = router.resolve(request_url)
        logging.debug(request_url)
        logging.debug(simplejson.JSONEncoder().encode(routes))
        if routes is not None:
            self.controller = routes['controller']
            self.action = routes['action']
            self.id = None
            if routes.has_key('id'):
                import urllib
                self.id = urllib.unquote(routes['id'])

            # This might not still be needed. Save it until I know that it's not

            # Add all of the route data into the view data so it can be used by templates
            for routing_key in routes.keys():
                self.view_data[routing_key] = routes[routing_key]
                if not hasattr(self, routing_key):
                    setattr(self, routing_key, routes[routing_key])
        else:
            fake_flash = {"error": "I couldn't find what you were asking for, but here is the glorious home page!"}
            self.view_data["flash"] = fake_flash
            self.controller = "home"
            self.action = "index"
            # Even though id will not be used, other methods may expect it to be there, so create it.
            self.id = None

        HttpVerbs.__init__(self, request_handler.request.method)

    def __getitem__(self, index):
        """Retreive a value, using dictionary-like subscripts, from the
        request's view_data, the collection of values that is passed
        to the view."""
        return self.view_data[index]

    def __setitem__(self, index, value):
        """Set a value, using dictionary-like subscripts, from the
        request's view_data, the collection of values that is passed
        tothe view."""
        self.view_data[index] = value

    def __len__(self):
        """Return the size of the view_data collection when the len()
        function is used on the MVCContext object."""
        return len(self.view_data)

def dynamic_param_list(method, inputs):
    """
    This function builds an array of values that can be used to
    dynamically provide parameters to a method that has a signature that
    is not known in advance.

    Parameters:
    * method: a bound or unbound function
    * inputs: a dictionary of values that can be used to provide
      values for method's parameters.

    Example:
    class mathfuncs(object):
        def add_numbers(self, a, b, c, d, e=10):
            return a + b + c + d + e

    foo = mathfuncs()
    
    ones = {"a" : 1, "b" : 2, "c": 3, "d": 4, "e": 5}
    fives = {"a" : 5, "b" : 10, "c": 15, "d": 20}
    ones_inputs = dynamic_param_list(foo.add_numbers, ones)
    fives_inputs = dynamic_param_list(foo.add_numbers, fives)

    print("by ones: %d" % foo.add_numbers(*ones_inputs))
    print("by fives: %d" % foo.add_numbers(*fives_inputs))

    Comments:
    The inputs dictionary is expected to have keys that match up
    to the names of method's parameters.
    
    The matching logic will never try to assign a value to the
    parameter named self, as that should be supplied by Python.

    If one of the method's parameters has a default value and the
    inputs dictionary does not have a matching key, the default
    value is provided.

    Any method parameter that does not have a matching key in the
    inputs dictionary and does not have a default value will get
    set to None. If this is a valid condition, your method must check for
    None.
    """
    from inspect import getargspec

    method_signature = getargspec(method)
    param_names = method_signature[0]
    default_values = method_signature[3]
    params = []
    input_keys = inputs.keys()
    # If any of method's parameters has default values, we need
    # to know the index of the first one that does.
    param_with_default_loc = -1
    if default_values is not None and len(default_values) > 0:
        param_slice_index = len(default_values) * -1
        param_with_default = param_names[param_slice_index:][0]
        param_with_default_loc = param_names.index(param_with_default)

    for each_param in param_names:
        if each_param != "self":
            if each_param in input_keys:
                # The method parameter does match a value in the
                # inputs dictionary.
                params.append(inputs[each_param])
            else:
                # No match, so we will either supply the parameter's
                # default value or None.
                if param_with_default_loc != -1:
                    param_loc = param_names.index(each_param)
                    if  param_loc >= param_with_default_loc:
                        # Find the correct value in the tuple of default values
                        # and and use it.
                        def_value = default_values[param_loc - param_with_default_loc]
                        params.append(def_value)
                    else:
                        # No default value, set to None
                        params.append(None)
                else:
                    # There are no default values for any of method's
                    # parameters, so set this one to None.
                    params.append(None)
    return params

# The MVC Engine class definition
class MVCEngine(webapp.RequestHandler):

    @staticmethod
    def __classForName(name, *args, **kw):
        ns = kw.get('namespace', globals())
        return ns[name](*args)

    __app_class = None

    @staticmethod
    def __load_app_class():
        """Each application can have a special file, app/app.py, which defines
        functions that are called at various stages in the processing of a
        request. This function is responsible for locating and loading the class.
        """
        try:
            app_module = __import__('app')
            __appClass = MVCEngine.__classForName('App', namespace=app_module.__dict__)

            return __appClass
        except ImportError:
            logging.info("Could not find app/app.py")
        except AttributeError:
            logging.info("Could not find app class")
    
    @staticmethod     
    def append_paths():
        from django.conf import settings
        if settings.ROOTDIR : 
            root = settings.ROOTDIR
        else:
            root = __file__
        
        # self inject to the search path, so that apps can just 'from MVCEngine import ...'
        sys.path.append(os.path.dirname(__file__))
        
        paths = [
            # for gaemvclib use __file__ as it should be always next to MVCEngine.py
            os.path.join(os.path.dirname(__file__), 'gaemvclib'),
            os.path.join(os.path.dirname(root), 'app', 'tags'),
            os.path.join(os.path.dirname(root), 'app', 'controllers'),
            os.path.join(os.path.dirname(root), 'app', 'common'),
            os.path.join(os.path.dirname(root), 'app', 'models'),
            os.path.join(os.path.dirname(root), 'app')
        ]
        
        for path in paths:
            if os.path.exists(path):
                # Don't add paths that don't exist. It is entirely possible that
                # the models directory might not exists, as some AppEngine
                # applications might not use them
                sys.path.append(path)

    def __init__(self):
        MVCEngine.append_paths()
         
        # Load the app class, so we can use it where needed.
        self.app_class = MVCEngine.__load_app_class()

        # Create the Router object and load routes from the app class.
        from gaemvclib.mvcrouter import Router
        self.router = Router()
        self.app_class.routes(self.router)

    def handle_request(self, url):
        """
        """
        import traceback

        def continue_chain(result):
            """continue_chain analyzes the values returned by filters that are
            run in processing the Call Chain. Any filter is able to declare that
            processing of Call Chain should cease and that a response is to be
            immediately returned. A Filter must return the value Filter.CONTINUE
            in order for the Call Chain is continue processing.
            """
            do_continue = False
            if result is None or isinstance(result, int) and result == Filter.CONTINUE:
                do_continue = True

            return do_continue

        urlPath = self.request.path.split("/")
        lastWord = urlPath[len(urlPath)-1]
        if(lastWord.rfind(".") != -1):
            lastWord = lastWord[0:lastWord.rfind(".")]
        urlPath[len(urlPath)-1] = lastWord
        context = MVCContext(self, "/".join(urlPath) , self.router, {})

        # Load controller
        controller_name = context.controller + "_controller"

        controller = None
        #try:
        controller = __import__(controller_name,globals(),locals())
        #except ImportError:
        #    logging.error("controller not found "+controller_name)
        #    pass

        if controller is not None:
            # Run the load method from app.py.
            self.app_class.load(context)

            # Call-chain step 1: Run filters that happen before all controllers
            action_result = Filter.run_before_controllers_filters(context)

            if continue_chain(action_result):
                # Instantiate controller class
                controllerClass = MVCEngine.__classForName(controller_name, namespace=controller.__dict__)
                controllerClass.context = context

                actionMethod = None
                # Get action
                try:
                    actionMethod = getattr(controllerClass, context.action)
                except AttributeError:
                    # The requested method does not exist in the controller. This error condition is handled
                    # below, so just eat the exception.
                    pass

                # Run action        
                try:
                    if actionMethod != None:
                        # Call-chain step 2: Run before filters specific to this Controller
                        action_result = Filter.run_before_filters(controllerClass, context)
                        if continue_chain(action_result):
                            # Call-chain step 3: Run filters that happen before all Actions
                            action_result = Filter.run_before_action_filters(context)
                            if continue_chain(action_result):
                                # Call-chain step 4: Run before filters specific to this Action
                                action_result = Filter.run_before_filters(actionMethod, context)
                                if continue_chain(action_result):
                                    # Give dynamic_param_list a dictionary that combines the
                                    # routing data and request params
                                    param_data = dict(context.view_data)
                                    param_data.update(self.request.params)

                                    parameters = dynamic_param_list(actionMethod, param_data)
                                    # We need to check whether actionMethod holds a bound
                                    # or unbound method. If it is unbound, it is still
                                    # actually a method of a class, and when it is called,
                                    # it will expect to have the first parameter be an
                                    # instance of its parent class, which is held in
                                    # controllerClass.
                                    # An action may appear to be an unbound method if it is
                                    # coming from an action_proxy which is the case when the
                                    # Controller.respond_to decorator is used.
                                    from inspect import ismethod
                                    if not ismethod(actionMethod):
                                        parameters.insert(0, controllerClass)

                                    # The parameter list is ready, so now we can actually
                                    # call the action method.
                                    # Call-chain step 5: Run the Action 
                                    action_result = actionMethod(*parameters)

                                    # assert isinstance(action_result, ActionResult), "An action method must return an object that inherits from ActionResult"

                                    # Call-chain step 6: Run after filters specific to this Action
                                    after_action_filter_result = Filter.run_after_filters(actionMethod, context)
                                    if continue_chain(after_action_filter_result):
                                        # Call-chain step 7: Run after filters that happen after all Actions
                                        after_all_actions_filters_result = Filter.run_after_action_filters(context)
                                        if continue_chain(after_all_actions_filters_result):
                                            # Call-chain step 8: Run after filters specific to this Controller
                                            after_controller_filters_result = Filter.run_after_filters(controllerClass, context)
                                            if continue_chain(after_controller_filters_result):
                                                # Call-chain step 9: Run after filters that happen after all Controllers
                                                after_all_controllers_filters_result = Filter.run_after_controllers_filters(context)

                                                # Running the after_all_controllers filters is currently the last step in the call chain.
                                                # If another stage were added, it would happen here
                                                if isinstance(after_all_controllers_filters_result, ActionResult):
                                                    action_result = after_all_controllers_filters_result
                                            elif isinstance(after_controller_filters_result, ActionResult):
                                                action_result = after_controller_filters_result
                                        elif isinstance(after_all_actions_filters_result, ActionResult):
                                            action_result = after_all_actions_filters_result
                                    elif isinstance(after_action_filter_result, ActionResult):
                                        action_result = after_action_filter_result

                    else:
                        # The requested action was not found.
                        if hasattr(self.app_class, "missing_action"):
                            result = self.app_class.missing_action(context)
                            if isinstance(result, ActionResult):
                                action_result = result
                            else:
                                action_result = RenderError(context, 404)
                        else:
                            action_result = RenderError(context, 404)
                except HTTPError:
                    pass
                except ActionResultSetException, raised_result:
                    action_result = raised_result.action_result
                except:
                    traceback.print_exc()
                    logging.debug("DEBUG: Caught an exception while executing action %s." % context.action)
                    self.error(404)
                    return
        else:
            # The requested controller does not exist. By default, return a 
            if hasattr(self.app_class, "missing_controller"):
                result = self.app_class.missing_controller(context)
                if isinstance(result, ActionResult):
                    action_result = result
                else:
                    action_result = RenderError(context, 404)
            else:
                action_result = RenderError(context, 404)


        context.response.headers.add_header("Set-Cookie", context.flash.as_cookie(context.request.environ['SERVER_NAME']))
        action_result.Render()
        # All done

    def get(self, *args):
        self.handle_request(args)

    def post(self, *args):
        self.handle_request(args)

    def put(self, *args):
        self.handle_request(args)

    def delete(self, *args):
        self.handle_request(args)

    def head(self, *args):
        self.handle_request(args)

    def trace(self, *args):
        self.handle_request(args)

    def options(self, *args):
        self.handle_request(args)
    
    @staticmethod
    def createApplication(additionalAppRoutes = [], debug = True):
    
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    
        from django.conf import settings
        views_path = os.path.join(os.path.dirname(settings.ROOTDIR), 'app', 'views')
        settings.TEMPLATE_LOADERS = (('gaemvclib.mvctemplateloader.MvcTemplateLoader', views_path), 'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
    
        # The improved routing mechanism comes from the google-app-engine-oil project
        # (http://code.google.com/p/google-app-engine-oil/) via David Case, who contributed
        # the idea and a very helpful inital implementation.
        # Routes are defined in app/app.py in the routes() function.
        return webapp.WSGIApplication( itertools.chain(additionalAppRoutes,[(r'.*', MVCEngine)]), debug=debug )
