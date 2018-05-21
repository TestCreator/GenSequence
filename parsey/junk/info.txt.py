# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1524534289.06853
_enable_loop = True
_template_filename = '/Users/jamiezimmerman/Documents/GenSequence/parsey/prm-blueprints/info.txt'
_template_uri = '/info.txt'
_source_encoding = 'ascii'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        info = context.get('info', UNDEFINED)
        __M_writer = context.writer()
        for decl in info['key1']:
            __M_writer(str(decl['varname']))
            __M_writer(' = ')
            __M_writer(str(decl['Rangeobj']))
            __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"16": 0, "32": 26, "22": 1, "23": 2, "24": 2, "25": 2, "26": 2}, "uri": "/info.txt", "filename": "/Users/jamiezimmerman/Documents/GenSequence/parsey/prm-blueprints/info.txt"}
__M_END_METADATA
"""
