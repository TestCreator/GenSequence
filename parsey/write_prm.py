from mako.template import Template

import parse_ranges
import argparse
from functools import reduce # lambda reduction of range lists

#####
#
#
#
#####


#####
# SCRUB_DOWN
# removes all comment from the open incoming file
#
#####
def scrub_down(filenam):
    f_in = open(filenam, 'r')
    g = f_in.readlines()
    f_in.close()
    for i in range(len(g)):
        x = g[i]
        x = x.split("#")[0]
        x = x if x.endswith("\n") else x+'\n'
        g[i] = x
    f_in = open("NO-COMMENTS-"+filenam, 'w')
    for line in g:
        f_in.write(line)
    f_in.close()

#####
# SKIP_NEW_LINES
# fi - an open file
# this function will keep reading the file at the open position by skipping new lines
#####
def skip_new_lines(fi):
    line = fi.readline()
    while line.startswith("\n"):
        line = fi.readline()
    return line, fi

#####
# SEARCH_FOR_PARM_DECS
# fp - an open file
# scans the file looking for the @Vertical section and column definitions. just looking for the parm and card definitions
#####
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

    return parms, card, line, fp


#####
# PROCESS_RANGES
# input is a string representing the pairs of or lists of or single range object names
# turns the input into a list of tuples of range objects for (cardioid), 
# or a list of ranges (for _cardioid) or a single range (for _cardioid)
# MAKES THEM TEMPLATE READY!!!
# x =
# card
# [['Micro', 'Shallow'], ['Great', 'Deep'], ['Feelable', 'Mid']] => [('Micro', 'Shallow'), ('Great', 'Deep'), ('Feelable', 'Mid')]
# [['North', 'East']] => [(North,East)]
# parm
# [['Micro']] => Micro
# [['Micro'], ['Feelable'], ['Great']] => ['Micro', 'Feelable', 'Great']
#####
def process_ranges(rangecross):
    x = [y.strip().split("*") for y in rangecross.split(",")]
    if len(x[0]) > 1: #card spec
        x = [tuple(y) for y in x]
    elif len(x[0]) == 1: #parm spec
        x = reduce(lambda a,b: a+b, x)

    x = "".join(list(filter(lambda y: y != "'", str(x))))
    return x
    

####################
# SEARCH_FOR_CARDIOID_SPECS
# fp - an open file has been left open just before the start of the card points!!
# scans the file looking for the args to cardioid functions, both parms and cards
# Cardioid cardioid
# % for card in data['special_card']:
# ${card['card_varname']}.setFavorites(card['favs'])
# ${card['card_varname']}.setNonFavorites(card['nonfavs'])
# % endfor
# Parm _cardioid
# % for parm in data['special_parm']:
# ${parm['parm_varname']}.setFavorites(${parm['fav']})
# ${parm['parm_varname']}.setNonFavorites(${parm['nonfav']})
# % endfor
#
# return 1 tuple of 2 lists
# 1 list is list of dict, each dict has parm_varname, favs, nonfavs
# other list is list of dict, each has card_varname, favs, nonfavs
#####

#Mags~_cardioid: #TODO the pairwise test vectors need to cover the opposite case
#        favorites: Micro
#        occasional:
#        outliers: Great

#MagsDepths~cardioid:
#        favorites: Micro*Shallow, Great*Deep, Feelable*Mid
#        occasional:
#        not: Micro*Deep, Great*Shallow, Feelable*Deep, Feelable*Shallow

def search_for_cardioid_specs(header, fp, searchtimes):
    card_specs = []
    parm_specs = []
    line = header
    for i in range(searchtimes):
        if "~" in line:
            # begin processing subsection
            dummy = dict()
            
            favoritesLine = fp.readline().lstrip().split(":")[1].strip()
            occasionalLine = fp.readline() #doesn't matter anyway, just skip over
            nonfavoritesLine = fp.readline().lstrip().split(":")[1].strip()

            dummy['favs'] = process_ranges(favoritesLine)
            dummy['nonfavs'] = process_ranges(nonfavoritesLine)

            temp = line.rstrip(": \n").split("~")
            if temp[1] == "_cardioid":
                dummy['parm_varname'] = temp[0]
                parm_specs.append(dummy)
            elif temp[1] == "cardioid":
                dummy['card_varname'] = temp[0]
                card_specs.append(dummy)

            line, fp = skip_new_lines(fp)

    return card_specs, parm_specs




#####
# FORMAT_PARM_DECS
#
#
#####
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


#####
# SMART_SPLIT
#
#
#####
def smart_split(cardioid, parm_pool):
    for parmy in parm_pool:
        if cardioid.startswith(parmy):
            first = parmy
        elif cardioid.endswith(parmy):
            second = parmy
    assert first+second==cardioid, "Uh-oh, I found two parms '{}' and '{}' that don't match your cardioid '{}'".format(first, second, cardioid)
    return first, second


#####
# FORMAT_CARD_DECS
# takes in a list of cardoid objects,
# figures out the composite parm objects
# and generates the data structure that gets rendered into the mako template
#####
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



#####
# PARTITION_PARMS
# figure out which parms are in a multicol, and which are not!
#
#####
def partition_parms(parms_list, cards_list):
    parms_partition = set(parms_list)
    cards_partition = set()
    for card in cards_list:
        cards_partition.add(card)
        first, second = smart_split(card, parms_list)
        parms_partition -= set([first, second])
    return list(parms_partition), list(cards_partition)



#####
# SERVE_TEMPLATE
# does the writing!! the output is the executable
#
#####
def serve_template(tempname, dest, **kwargs):
    mytemplate = Template(filename=tempname)
    print(mytemplate.render(data=kwargs), file=dest)


def cli():
    """Get arguments from command line"""
    parser = argparse.ArgumentParser(description="Preprocessor")
    parser.add_argument("-s", "--source", help="prm source file describing whatcha want!")
    parser.add_argument("-t", "--template", help="Template name blueprint")
    parser.add_argument("-d", "--destination", help="Destination output filename", type=argparse.FileType('w'))
    args = parser.parse_args()
    return args


if __name__=="__main__":
        args = cli()
        scrub_down(args.source)
        source = open("NO-COMMENTS-"+args.source, 'r')
        
        #get the ranges
        PARSED_TOKENS = parse_ranges.establish_parses(source, parse_ranges.parser)

        parms, cards, curLinePointer, file_reader = search_for_parm_decs(source)
        print(cards)
        PARSED_TOKENS['parms'] = format_parm_decs(parms)
        PARSED_TOKENS['cards'] = format_card_decs(cards, parms)

        card_specs, parm_specs = search_for_cardioid_specs(curLinePointer, file_reader, len(parms)+len(cards))
        PARSED_TOKENS['special_card'] = card_specs
        PARSED_TOKENS['special_parm'] = parm_specs

        print(PARSED_TOKENS['cards'])
        parmys, cardys = partition_parms(parms, cards)
        print(cardys)
        PARSED_TOKENS['est_parms'] = format_parm_decs(parmys)
        PARSED_TOKENS['est_cards'] = format_card_decs(cardys, parms)


        serve_template(args.template, args.destination, **PARSED_TOKENS)
        
        

