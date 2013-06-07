__author__ = 'Julie'

import re

def configure(args):

    factorPATT=re.compile('f=(.*)')

    parameters={}
    #defaults

    parameters["at_home"]=False
    parameters["local"]=False
    parameters["on_apollo"]=True
    parameters["reduction"]=2
    parameters["testing"]=False
    parameters["factors"]=1000
    parameters["method"]="svd"

    for arg in args:
        if arg=="at_home":
            parameters["at_home"]=True
            parameters["local"]=False
            parameters["on_apollo"]=False
        if arg=="on_apollo":
            parameters["on_apollo"]=True
            parameters["local"]=False
            parameters["at_home"]=False
        if arg=="testing":
            parameters["testing"]=True
        if arg=="nmf":
            parameters["method"]="nmf"
        if arg=="svd":
            parameters["method"]="svd"
        matchobj=factorPATT.match(arg)
        if matchobj:
            parameters["factors"]=matchobj.group(1)


    if parameters["on_apollo"]:

        parameters["parent"]="/mnt/lustre/scratch/inf/juliewe/FeatureExtractionToolkit/Byblo-2.2.0/"

    if parameters["testing"]:
        parameters["parent"]="../data/"
        parameters["dir"]=parameters["parent"]+"./"
        parameters["file"]="toyvectors2"
        parameters["name"]="toyvectors2"
        #parameters["factors"]=3
    else:
        parameters["name"]="gigaword_t100"
        parameters["dir"]=parameters["parent"]+"giga_t100f100_nouns_deps/"
    #parameters["infile"]=parameters["dir"]+parameters["name"]+".events.filtered.strings"



    return parameters
