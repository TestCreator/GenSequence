from mako.template import Template
from mako.lookup import TemplateLookup

from parse_ranges import PARSED_TOKENS

#mytemplate = Template(filename='template')
#print(mytemplate.render(b))


mylookup = TemplateLookup(directories=['/Users/jamiezimmerman/Documents/GenSequence/parsey/prm-blueprints'], 
        module_directory='/Users/jamiezimmerman/Documents/GenSequence/parsey/junk')

def serve_template(templatename, *args, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    print(mytemplate.render(**kwargs))

serve_template("/info.txt", **PARSED_TOKENS)