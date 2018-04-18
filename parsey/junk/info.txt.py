# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1524029548.340488
_enable_loop = True
_template_filename = '/Users/jamiezimmerman/Documents/GenSequence/parsey/prm-blueprints/info.txt'
_template_uri = '/info.txt'
_source_encoding = 'ascii'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        Rangeobj = context.get('Rangeobj', UNDEFINED)
        varname = context.get('varname', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(str(varname))
        __M_writer(' = ')
        __M_writer(str(Rangeobj))
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"uri": "/info.txt", "line_map": {"16": 0, "32": 26, "23": 1, "24": 1, "25": 1, "26": 1}, "filename": "/Users/jamiezimmerman/Documents/GenSequence/parsey/prm-blueprints/info.txt", "source_encoding": "ascii"}
__M_END_METADATA
"""
