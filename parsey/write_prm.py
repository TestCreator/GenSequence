from mako.template import Template

import parse_ranges
import argparse

def skip_new_lines(fi):
    line = fi.readline()
    while line.startswith("\n"):
        line = fi.readline()
    return line, fi

def search_for_parm_decs(fp):
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
    card = []
    parms = []
    
    line = fp.readline()
    while line:
        ## Reading the general column type spec
        if line.startswith("@Vertical"):
            line = fp.readline()
            while not line.startswith("\n"):
                if "multicol" in line:
                    card.append(line)
                else:
                    parms.append(line)
                line = fp.readline()
        
            card = [arg.strip().split(" ")[-1] for arg in card]

        ## Now read the individual column type spec
            line, fp = skip_new_lines(fp)
            for i in range(len(card)): # for as many multicols as there are
                assert (line.strip(":\n") in card), "Uh-oh! This multicol \"{}\" isn't in your @Vertical definition: {}".format(line.strip(":\n"), card)
                line = fp.readline()
                while not line.startswith("\n"):
                    parms.append(line)
                    line = fp.readline()
                line, fp = skip_new_lines(fp)
            break #to stop reading
        line = fp.readline()
    parms = [arg.strip().split(" ")[-1] for arg in parms]

    return parms, card

def format_parm_decs(parm_group):
    """
    % for rang in data['parms']:
    ${rang['parm_varname']} = Parm(${rang['construct_name']}, "one-by-one", Total${rang['parm_rangename']})
    % endfor

    output needs to be list of dicts s.t. each dict has parm_varname, construct_name, and parm_rangename
    """
    the_parms = []
    for parmname in parm_group:
        temp = {}
        temp['parm_varname'] = parmname
        temp['construct_name'] = parmname.lower()
        temp['parm_rangename'] = parmname
        the_parms.append(temp)
    return the_parms

def smart_split(cardioid, parm_pool):
    for parmy in parm_pool:
        if cardioid.startswith(parmy):
            first = parmy
        elif cardioid.endswith(parmy):
            second = parmy
    assert first+second==cardioid, "Uh-oh, I found two parms '{}' and '{}' that don't match your cardioid '{}'".format(first, second, cardioid)
    return first, second

def format_card_decs(card_group, parm_group):
    """
    % for card in data['cards']:
    ${card['card_varname']} = Cardioid(${card['first']}, ${card['second']})
    % endfor

    output needs to be list of dicts s.t. each dict has card_varname, first parm, and second parm
    """
    the_cards = []
    for cardname in card_group:
        #get the cardioid split
        first, second = smart_split(cardname, parm_group)

        temp = {}
        temp['card_varname'] = cardname
        temp['first'] = first
        temp['second'] = second
        the_cards.append(temp)
    return the_cards


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
        PARSED_TOKENS['parms'] = format_parm_decs(parms)
        PARSED_TOKENS['cards'] = format_card_decs(cards, parms)
        serve_template(args.template, args.destination, **PARSED_TOKENS)

