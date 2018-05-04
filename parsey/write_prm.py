from mako.template import Template

import parse_ranges
import argparse

def search_for_parm_decs(in_file):
    """
    Mags = Parm("magnitudes", "one-by-one", TotalMags)
    Lats = Parm("latitudes", "one-by-one", TotalLats)
    Longs = Parm("longitudes", "one-by-one", TotalLongs)
    Depths = Parm("depths", "one-by-one", TotalDepths)  
    MagsDepths = Cardioid(Mags, Depths)

    Should return tuple of lists
    parm_list => ['Lats', 'Longs', "Mags", "Depths"]
    card_list => ["MagsDepths"]
    """
    parm_list = []
    card_list = []

    found_vertical
    for line in in_file:
        if line.startswith("multicol"):
            new_cardioid = line.split(" ")[-1]
            card_list.append(new_cardioid)
        elif line.startswith("col"):
            new_parm = line.split(" ")[-1]
            parm_list.append(new_parm)

    return parm_list, card_list

def format_parm_decs(parms, cards):
    """
    % for rang in data['parms']:
    ${rang['parm_varname']} = Parm(${rang['construct_name']}, "one-by-one", Total${rang['parm_varname']})
    % endfor

    % for card in data['cards']:
    ${card['card_varname']} = Cardioid(${card['first']}, ${card['seconds']})
    % endfor
    """

    return 

def serve_template(tempname, dest, **kwargs):
    mytemplate = Template(filename=tempname)
    print(mytemplate.render(data=kwargs), file=dest)


def cli():
    """Get arguments from command line"""
    parser = argparse.ArgumentParser(description="Preprocessor")
    parser.add_argument("-s", "--source", help="prm source file describing whatcha want!", type=argparse.FileType('r'))
    parser.add_argument("-t", "--template", help="Template name blueprint")
    parser.add_argument("-d", "--destination", help="Destination output filename", type=argparse.FileType('w'))
    args = parser.parse_args()
    return args


if __name__=="__main__":
        args = cli()
        #get the ranges
        PARSED_TOKENS = parse_ranges.establish_parses(args.source, parse_ranges.parser)
        print(PARSED_TOKENS)

        parms, cards = search_for_parm_decs(args.source)
        PARSED_TOKENS['parms'] = format_parm_decs(parms, cards)
        serve_template(args.template, args.destination, **PARSED_TOKENS)

