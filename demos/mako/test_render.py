from mako.template import Template
from mako.lookup import TemplateLookup
from mako.runtime import Context
import io

from parse_ranges import info

mylookup = TemplateLookup(directories=['/Users/jamiezimmerman/Documents/GenSequence/parsey/prm-blueprints'])

def serve_template(templatename, *args, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    buf = io.StringIO()
    ctx = Context(buf, info=kwargs)
    mytemplate.render_context(ctx)
    print(buf.getvalue())

serve_template("/masterTemplate", **info)