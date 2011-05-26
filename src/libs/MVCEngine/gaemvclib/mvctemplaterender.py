import django.template
import django.template.loader
from django.template.context import Context

def render(template_path, template_dict, debug=False):
  """Renders the template at the given path with the given dict of values.

  Example usage:
    render("templates/index.html", {"name": "Bret", "values": [1, 2, 3]})

  Args:
    template_path: path to a Django template
    template_dict: dictionary of values to apply to the template
  """
  t = load(template_path, debug)
  return t.render(Context(template_dict))


template_cache = {}
def load(path, debug=False):
  """Loads the Django template from the given path.

  It is better to use this function than to construct a Template using the
  class below because Django requires you to load the template with a method
  if you want imports and extends to work in the template.
  """
  #abspath = os.path.abspath(path)

  if not debug:
    template = template_cache.get(path, None)
  else:
    template = None

  if not template:
    new_settings = {
        'TEMPLATE_DEBUG': debug,
        'DEBUG': debug,
        }
    old_settings = _swap_settings(new_settings)
    try:
      template = django.template.loader.get_template(path)
    finally:
      _swap_settings(old_settings)

    if not debug:
      template_cache[path] = template

    def wrap_render(context, orig_render=template.render):
      URLNode = django.template.defaulttags.URLNode
      save_urlnode_render = URLNode.render
      old_settings = _swap_settings(new_settings)
      try:
        URLNode.render = _urlnode_render_replacement
        return orig_render(context)
      finally:
        _swap_settings(old_settings)
        URLNode.render = save_urlnode_render

    template.render = wrap_render

  return template


def _swap_settings(new):
  """Swap in selected Django settings, returning old settings.

  Example:
    save = _swap_settings({'X': 1, 'Y': 2})
    try:
      ...new settings for X and Y are in effect here...
    finally:
      _swap_settings(save)

  Args:
    new: A dict containing settings to change; the keys should
      be setting names and the values settings values.

  Returns:
    Another dict structured the same was as the argument containing
    the original settings.  Original settings that were not set at all
    are returned as None, and will be restored as None by the
    'finally' clause in the example above.  This shouldn't matter; we
    can't delete settings that are given as None, since None is also a
    legitimate value for some settings.  Creating a separate flag value
    for 'unset' settings seems overkill as there is no known use case.
  """
  settings = django.conf.settings
  old = {}
  for key, value in new.iteritems():
    old[key] = getattr(settings, key, None)
    setattr(settings, key, value)
  return old

def _urlnode_render_replacement(self, context):
  """Replacement for django's {% url %} block.

  This version uses WSGIApplication's url mapping to create urls.

  Examples:

  <a href="{% url MyPageHandler "overview" %}">
  {% url MyPageHandler implicit_args=False %}
  {% url MyPageHandler "calendar" %}
  {% url MyPageHandler "jsmith","calendar" %}
  """
  args = [arg.resolve(context) for arg in self.args]
  try:
    app = webapp.WSGIApplication.active_instance
    handler = app.get_registered_handler_by_name(self.view_name)
    return handler.get_url(implicit_args=True, *args)
  except webapp.NoUrlFoundError:
    return ''
