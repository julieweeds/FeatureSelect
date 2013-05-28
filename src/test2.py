__author__ = 'juliewe'

#use scipy.sparse.linalg.svds for svd

import numpy
from scipy.sparse import csc_matrix as csc_matrix
from scipy.sparse.linalg import svds as svds

#a=200
#b=100
#factors=50
#mat = numpy.random.rand(a,b)
#print "Created random matrix "+str(a)+"x"+str(b)
#smat=csc_matrix(mat)
#print "Converted to csc format"

#ut,s,vt = svds(smat,factors)
#print "Performed svd with "+str(factors)+ " factors"

mat2 = numpy.matrix([[3.0,1.0,1.0],[-1.0,3.0,1.0],[6.0,2.0,2.0]])
#print "Created matrix"
smat2 = csc_matrix(mat2)
#print "Converted to csc format"
ut,s,vt = svds(smat2,2)
#print "Performed svd"
#print ut
#print s
#print vt

sdiag = numpy.diag(s)
#print sdiag

mult = numpy.dot(ut,sdiag)
#print mult

mult2 = numpy.dot(mult,vt)
#print mult2

assert numpy.allclose(mat2,numpy.dot(ut,numpy.dot(numpy.diag(s),vt)))


row = numpy.array([0,2,2,0,1,2])
col = numpy.array([0,0,1,2,2,2])
data=numpy.array([1,2,3,4,5,6])
matrix = csc_matrix((data,(row,col)))

print matrix.todense()




#assert numpy.allclose(mat,numpy.dot(ut.T,numpy.dot(numpy.diag(s),vt)))
