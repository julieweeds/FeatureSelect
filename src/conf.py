__author__ = 'Julie'

def configure(args):

    parameters={}
    #defaults

    parameters["at_home"]=True
    parameters["local"]=False
    parameters["on_apollo"]=False
    parameters["reduction"]=1
    parameters["testing"]=False
    parameters["factors"]=1000

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

    parameters["parent"]="../data/"
    if parameters["on_apollo"]:

        parameters["parent"]="/mnt/lustre/scratch/inf/juliewe/FeatureExtractionToolkit/Byblo-2.2.0/"

    if parameters["testing"]:
        parameters["file"]="toyvectors2"
        parameters["factors"]=3
    else:
        parameters["file"]="giga_t100f100_nouns_deps/vectors"
    parameters["infile"]=parameters["parent"]+parameters["file"]



    return parameters
