__author__ = 'Julie'

def configure(args):

    parameters={}
    #defaults

    parameters["at_home"]=True
    parameters["local"]=False
    parameters["on_apollo"]=False

    for arg in args:
        if arg=="at_home":
            parameters["at_home"]=True


    parameters["infile"]="../data/toyvectors"



    return parameters
