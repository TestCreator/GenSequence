from mako.template import Template

from parse_ranges import info

import argparse


def serve_template(tempname, dest, **kwargs):
    mytemplate = Template(filename=tempname)
    print(mytemplate.render(data=kwargs), file=dest)


def cli():
    """Get arguments from command line"""
    parser = argparse.ArgumentParser(description="Preprocessor")
    parser.add_argument("-t", "--template", help="Template name blueprint")
    parser.add_argument("-d", "--destination", help="Destination output filename", type=argparse.FileType('w'))
    args = parser.parse_args()
    return args


if __name__=="__main__":
        args = cli()
        print(info)
        serve_template(args.template, args.destination, **info)