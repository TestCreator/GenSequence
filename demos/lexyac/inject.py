from mako.template import Template
from mako.lookup import TemplateLookup

from test import b

#mytemplate = Template(filename='template')
#print(mytemplate.render(b))


mylookup = TemplateLookup(directories=['/Users/jamiezimmerman/Documents/GenSequence/demos/lexyac'], module_directory='/Users/jamiezimmerman/Documents/GenSequence/demos/lexyac')

def serve_template(templatename, *args, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    print(mytemplate.render(**kwargs))

serve_template("/info.txt", **b)