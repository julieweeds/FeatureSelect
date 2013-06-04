__author__ = 'juliewe'


import numpy as np
#import sklearn.decomposition.NMF as NMF
#implements C.J.Lin's projected gradient methods for NMF

X = np.array([[1,1],[2,1],[3,1.2],[4,1],[5,0.8],[6,1]])  #n*d
from sklearn.decomposition import ProjectedGradientNMF
model = ProjectedGradientNMF(n_components=2,init='random',random_state=0)
w= model.fit_transform(X)  #left factor w (n*k)
h= model.components_ #right factor h (k*d)

print w
print h
v = np.dot(w,h)
print v



