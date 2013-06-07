__author__ = 'Julie'

import conf, sys, numpy, math
import scipy.sparse as sparse
from scipy.sparse.linalg import svds as svds

def writetestdata():
    #print math.pow(8,0.5)
    matrix = [["apple","a",2,"b",0,"c",8,"d",6,"e",0],["banana","a",1,"b",6,"c",0,"d",1,"e",7],["orange","a",5,"b",0,"c",7,"d",4,"e",0],["grape","a",7,"b",0,"c",8,"d",5,"e",0],["peach","a",0,"b",10,"c",0,"d",0,"e",7]]
    file="../data/5x5test"
    outstream=open(file,'w')
    for row in matrix:
        for item in row:
            outstream.write(str(item)+"\t")
        outstream.write("\n")
    outstream.close()
    return file


class Vector:

    def __init__(self,entry):
        self.entry=entry
        self.features={}
        self.array=""
        self.rowindex=-1

    def dotproduct(self,avector):
        return self.array.multiply(avector.array).sum()

    def addfeatures(self,list):

        while len(list)>0:
            feature=list.pop()
            value=list.pop()
            if feature in self.features.keys():
                print "Error: already have "+feature+" for "+self.entry
            else:
                self.features[feature]=value

    def length(self):
        return math.pow(self.dotproduct(self),0.5)

    def cossim(self,avector):

        den = self.length()*avector.length()
        num = self.dotproduct(avector)

        sim = num/den
        return sim
    def display(self):
        print self.entry
        print self.rowindex
        print self.array

class SVD:

    def __init__(self,infile,reduction):
        self.infile=infile
        self.vectordict={}
        self.allfeatures=[]
        self.fk_idx={}
        self.dim=0
        self.fullmatrix=[]
        self.reducedmatrix=[]
        self.reduction=reduction


        self.readfile()
        min = self.makematrix()
        self.allpairsims()
        self.reducedim(min -self.reduction)
        self.allpairsims()

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
          #      print "Made entry for "+entry
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
    #    print self.allfeatures
        self.allfeatures.sort()
        for i in range(len(self.allfeatures)):
            self.fk_idx[self.allfeatures[i]] = i

        self.dim=len(self.fk_idx)
        print "Dimensionality is "+str(self.dim)
       # print self.fk_idx
        self.makearrays()
        if len(self.vectordict.keys()) < self.dim :
            return len(self.vectordict.keys())
        else:
            return self.dim


    def makearrays(self):
        #convert vector which stores dictionary of features into sparse array based on fk_idx

        rows=[]
        cols=[]
        data=[]
        #thisrow=[]
        rowpointer=0

        for vector in self.vectordict.values():
            vector.rowindex=rowpointer
            temparray=numpy.zeros(self.dim)
            for feature in vector.features.keys():
                col = int(self.fk_idx[feature])
                score = float(vector.features[feature])
                temparray[col]=score
                rows.append(rowpointer)
                cols.append(col)
                data.append(score)

            vector.array = sparse.csc_matrix(temparray)
            rowpointer+=1
        #print rows
        #print cols
        #print data

        self.fullmatrix = sparse.csc_matrix((numpy.array(data),(numpy.array(rows),numpy.array(cols))))
        #print self.fullmatrix.todense()



    def reducedim(self,factors):
        #print self.fullmatrix
        print "Number of factors is "+str(factors)

        ut,s,vt = svds(self.fullmatrix,factors)
        print "Singular matrix is "
        print numpy.diag(s)

        self.reducedmatrix=numpy.dot(ut,numpy.diag(s))
        #print "Left singular vector matrix u is "
        #print ut
        #print "Right singular vector matrix vt is "
        #print vt
        print "Reduced dimensionality matrix is "
        print self.reducedmatrix
        for vector in self.vectordict.values():
            vector.array=sparse.csc_matrix(self.reducedmatrix[vector.rowindex])


    def allpairsims(self):
        for avector in self.vectordict.values():
            avector.display()
            for bvector in self.vectordict.values():
                print avector.entry, bvector.entry, avector.cossim(bvector)


if __name__=="__main__":
    parameters = conf.configure(sys.argv)
    mySVD = SVD(writetestdata(),parameters["reduction"])
