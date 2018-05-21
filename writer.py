import csv
""" 
Didn't want to find max/min of all the data points, so write in a csv so Excel can do the work for me
"""

def get_info():
        the_stuff = []
        with open("demos/orbits/solarsystem.txt") as solarfile:
                lines = solarfile.readlines()
                for line in lines:
                        if not line.startswith("#") and not line.startswith("\n"):
                                record = line.strip("\n").split(" ")
                                name, mass, x, y, z, v1, v2, v3, diam, color = tuple(record[0:10])
                                the_stuff.append([name, mass, x, y, z, v1, v2, v3, diam, color])
        return the_stuff



def process():
        with open("{}.csv".format("small_orbits_data"), 'w', newline='') as concretefile:
                fieldnames = ["name", "mass", "x1", "y1", "z1", "v1", "v2", "v3", "diam", "color"]
                writer = csv.DictWriter(concretefile, fieldnames=fieldnames)
                writer.writeheader()

                the_data = get_info()

                for line in the_data:
                        row = dict(zip(fieldnames, line))
                        writer.writerow(row)

process()