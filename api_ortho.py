#!/usr/bin/env python

import os
import subprocess
import argparse

parser = argparse.ArgumentParser(
    description = "Identifies putative orthologs for multi-domain proteins.",
    epilog = """This program requires all the requisite programs and files
    to be installed and in the system path. Based on RBH and domain criterion,
    this program will identify putatively homologous (orthologs and homologs)
    in a given list of databases.""")
parser.add_argument('queries', nargs='+', help='list of queries')
parser.add_argument('databases', nargs='+', help='list of databases')
args = parser.parse_args()

curdir = os.getcwd()

for query in args.queries:
    for database in args.databases:
        q = query.strip('.fa')
        d = database.strip('.fa')
        blast_fmt = "6 qacc sacc evalue"
        fblast_out = q + '_' + d + '_' + 'fblast.txt'
        #blast_options = "-evalue 0.05"
        subprocess.call(["blastp", "-query", os.path.join(curdir,query), "-db",\
                os.path.join(curdir,database), "-out", fblast_out,\
                "-outfmt", blast_fmt, "-evalue", str(0.05)])

        with open(os.path.join(curdir,fblast_out),'U') as i:
            hit_dict = {}
            prevline = ''
            for curline in i:
                curlist = curline.strip('\n').split('\t')
                try:
                    prevlist = prevline.strip('\n').split('\t')
                except:
                    pass
                if curlist[0] == prevlist[0] and curlist[1] == curlist[2]:
                    pass
                else:
                    facc = curlist[0]
                    fhit = curlist[1]
                    feval = curlist[2]

                    if facc not in hit_dict.keys():
                        hit_dict[facc] = []
                        hit_dict[facc].append([fhit,feval])
                    else:
                        hit_dict[facc].append([fhit,feval])
                prevline = curline

print hit_dict
