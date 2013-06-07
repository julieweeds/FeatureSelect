__author__ = 'Julie'
import math

class Polynomial:

    def __init__(self):
        self.coeffs=[-4,-1,6,-1]

    def setall(self,list):
        self.coeffs=list

    def apply(self,x):

        n=0
        y=0
        for coeff in self.coeffs:
           y+= math.pow(x,n)*coeff
           n+=1
        return y

if __name__ == "__main__":
    poly = Polynomial()
    xs = [1.76994587,6.30386923]
    for x in xs:
        print str(x)+" ==> "+str(poly.apply(x))

