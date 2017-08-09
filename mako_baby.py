from mako.template import Template

template = Template("hello world!, your name is ${name}")
print(template.render(name="Jack"))

def render_config(template_string, template_variable_dict):
	return Template(template_string).render(**template_variable_dict)

t = render_config("hello there ${name}!", {"name": "Joe"})
print(t)

