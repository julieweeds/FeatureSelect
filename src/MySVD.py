__author__ = 'juliewe'

import conf, sys, numpy, math
import scipy.sparse as sparse
from scipy.sparse.linalg import svds as svds
from sklearn.decomposition import ProjectedGradientNMF


def FixNaNs(m):
    #replace nans in numpy.array with 0s as these must be result of underflow in svds routine
    idxs=numpy.nonzero(m==m)[0]
    if len(idxs)==0:
        print "No NaNs found"
        return m
    for i in range(0,len(idxs)):
        m[idxs[i]]=0
    return m



class Vector:

    def __init__(self,entry):
        self.entry=entry
        self.features={}
        self.array=""
        self.rowindex=-1


    def dotproduct(self,avector):
        return self.array.multiply(avector.array).sum()

    def addfeatures(self,list,filteredS):

        while len(list)>0:
            feature=list.pop()
            value=list.pop()
            if feature in filteredS:
                print "Discarded "+self.entry+" "+feature+" "+value
            else:
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

    def outputvector(self,outstream):
        outstream.write(self.entry)
#           print self.entry
        array=self.array.toarray()[0]
      #  print len(array)
        for i in range(len(array)):
#            print i,array[i]
            outstream.write("\t"+"f"+str(i))
            outstream.write("\t"+str(array[i]))
        outstream.write("\n")


class SVD:

    filteredS = ["___FILTERED___"]

    def __init__(self,dir,name,method,factors):
        self.dir=dir
        self.name=name

        self.infile=self.dir+self.name+".events.filtered.strings"
        self.outfile=self.dir+method+str(factors)+"/"+self.name+".events.filtered.strings"
        self.entryfile=self.dir+method+str(factors)+"/"+self.name+".entries.filtered.strings"
        self.featurefile=self.dir+method+str(factors)+"/"+self.name+".features.filtered.strings"
        self.vectordict={}
        self.allfeatures=[]
        self.fk_idx={}
        self.dim=0
        self.fullmatrix=[]  #sparse csc_matrix
        self.reducedmatrix=[]  #numpy matrix
        self.method=method #svd or nmf?
        self.factors=int(factors)
        self.entrytotals={}
        self.featuretotals={}


        self.readfile()
        min = self.makematrix()
        if min<self.factors:
            print "Cannot do SVD with "+str(self.factors)+" factors"
            self.factors=min-1
            print "Reducing to "+str(self.factors)
#        self.allpairsims()
        self.reducedim(self.method,self.factors)
#        self.allpairsims()
        self.calctotals()
        self.output()

    def readfile(self):
        instream = open(self.infile,'r')
        print "Reading "+self.infile
        linesread=0
        for line in instream:
            line=line.rstrip()

            fields=line.split('\t')
            fields.reverse()
            entry = fields.pop()
            if entry in SVD.filteredS:
                print "Discarding line starting "+entry
            else:
                if entry in self.vectordict.keys():
                    print "Error: already have vector for "+entry
                else:
                    self.vectordict[entry]=Vector(entry)
                    #      print "Made entry for "+entry
                self.vectordict[entry].addfeatures(fields,SVD.filteredS)
            linesread+=1
            if linesread%1000==0:
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


    def reducedim(self,method,factors):
        if method=="svd":
            self.reducedim_svd(factors)
        elif method == "nmf":
            self.reducedim_nmf(factors)
        else:
            print "Unknown method of feature reduction"
            exit(1)

    def reducedim_svd(self,factors):
        #print self.fullmatrix
        print "Number of factors is "+str(factors)

        ut,s,vt = svds(self.fullmatrix,factors)

        if numpy.isnan(numpy.min(s)):
            print "Warning: diagonal matrix contains NaNs"
            #s=FixNaNs(s)
            s[numpy.isnan(s)]=0
            if numpy.isnan(numpy.min(s)):
                print "Error: diagonal matrix still contains NaNs, exiting"
                exit(1)

        print "Completed svd routine"

        self.reducedmatrix=numpy.dot(ut,numpy.diag(s))
        print "Computed reduced vector space"

        #remove negative numbers - make equal to zero
        self.reducedmatrix[self.reducedmatrix<0]=0

#        print self.reducedmatrix
        for vector in self.vectordict.values():
            vector.array=sparse.csc_matrix(self.reducedmatrix[vector.rowindex])
        print "Stored individual vectors"

    def reducedim_nmf(self,factors):
        print "Number of factors is "+str(factors)

        model = ProjectedGradientNMF(n_components=factors,init='random',random_state=0)
        self.reducedmatrix= model.fit_transform(self.fullmatrix)  #left factor w (n*k)
        h= model.components_ #right factor h (k*d)

        if self.testing:
            print self.fullmatrix
            print self.reducedmatrix
            print h
            v = numpy.dot(self.reducedmatrix,h)
            print v
        print "Completed NMF routine"
        for vector in self.vectordict.values():
            vector.array=sparse.csc_matrix(self.reducedmatrix[vector.rowindex])
        print "Stored individual vectors"

def calctotals(self):
        for vectorkey in self.vectordict.keys():
            total=self.vectordict[vectorkey].array.sum()
            self.entrytotals[vectorkey]=total
        ftotals=self.reducedmatrix.sum(axis=0)
        print "Calculated row totals"
        for i in range(self.factors):
            label = "f"+str(i)
            total = ftotals[i]
            self.featuretotals[label]=total
        print "Calculated column totals"

    def allpairsims(self):
        for avector in self.vectordict.values():
            avector.display()
            for bvector in self.vectordict.values():
                print avector.entry, bvector.entry, avector.cossim(bvector)


    def output(self):
        print "Writing output files"
        outstream=open(self.outfile,'w')
        for vector in self.vectordict.values():
            vector.outputvector(outstream)
        outstream.close()
        outstream=open(self.entryfile,'w')
        for key in self.entrytotals.keys():
            outstream.write(key+"\t"+str(self.entrytotals[key])+"\n")
        outstream.close()
        outstream=open(self.featurefile,'w')
        for key in self.featuretotals.keys():
            outstream.write(key+"\t"+str(self.featuretotals[key])+"\n")
        outstream.close()
        print "Completed output"

if __name__=="__main__":
    parameters = conf.configure(sys.argv)
    mySVD = SVD(parameters["dir"],parameters["name"],parameters["method"],parameters["factors"])
