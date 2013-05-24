__author__ = 'Julie'

import conf, sys, numpy
import scipy.sparse as sparse
from sparsesvd import sparsesvd


class Vector:

    def __init__(self,entry):
        self.entry=entry
        self.features={}
        self.array=""

    def addfeatures(self,list):

        while len(list)>0:
            feature=list.pop()
            value=list.pop()
            if feature in self.features.keys():
                print "Error: already have "+feature+" for "+self.entry
            else:
                self.features[feature]=value



class SVD:

    def __init__(self,infile):
        self.infile=infile
        self.vectordict={}
        self.allfeatures=[]
        self.fk_idx={}
        self.dim=0


        self.readfile()
        self.makematrix()

    def readfile(self):
        instream = open(self.infile,'r')
        print "Reading "+self.infile
        linesread=0
        for line in instream:
            line=line.rstrip()
            fields=line.split('\t')
            fields.reverse()
            entry = fields.pop()
            if entry in self.vectordict.keys():
                print "Error: already have vector for "+entry
            else:
                self.vectordict[entry]=Vector(entry)
            self.vectordict[entry].addfeatures(fields)
            linesread+=1
            if linesread%10==0:
                print "Read "+str(linesread)+" lines"
        instream.close()


    def listfeatures(self):
        for vector in self.vectordict.values():
            for feature in vector.features.keys():
                if feature in self.allfeatures:
                    #ignore
                    ignore = True
                else:
                    self.allfeatures.append(feature)

    def makematrix(self):
        self.listfeatures()#self.allfeatures now contains a list of the features in the vectors
        self.allfeatures.sort()
        for i in range(len(self.allfeatures)):
            self.fk_idx[self.allfeatures[i]] = i

        self.dim=len(self.fk_idx)
        print "Dimensionality is "+str(self.dim)
       # print self.fk_idx
        self.makearrays()

    def makearrays(self):
        #convert vector which stores dictionary of features into sparse array based on fk_idx

        for vector in self.vectordict.values():
            temparray=numpy.zeros(self.dim)
            for feature in vector.features.keys():
                col = self.fk_idx[feature]
                score = vector.features[feature]
                temparray[col]=score
            vector.array = sparse.csr_matrix(temparray)


if __name__=="__main__":
    parameters = conf.configure(sys.argv)
    mySVD = SVD(parameters["infile"])
