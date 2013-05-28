__author__ = 'juliewe'

import numpy, scipy.sparse
from sparsesvd import sparsesvd
a=long(200)
b=long(100)
factors=long(50)
mat = numpy.random.rand(a,b)
print "Created random matrix "+str(a)+"x"+str(b)
smat=scipy.sparse.csc_matrix(mat)
print "Converted into csc format"
ut,s,vt = sparsesvd(smat,50)
print "Performed svd with "+str(factors)+ "factors"
assert numpy.allclose(mat,numpy.dot(ut.T,numpy.dot(numpy.diag(s),vt)))
