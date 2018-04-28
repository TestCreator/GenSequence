from mako.template import Template
from mako.runtime import Context
import io

mytemplate = Template("% for entry in info['key1']:\n hello, ${entry['name']}, you are age ${entry['age']}! \n % endfor")
buf = io.StringIO()
l = {"key1": [{"name": "jack", "age": 10}, {"name": "annie", "age": 8}]}
ctx = Context(buf, info=l)
mytemplate.render_context(ctx)
print(buf.getvalue())