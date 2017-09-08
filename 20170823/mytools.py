import numpy

def linematch(x,y):
	N = float(len(x))
	sx,sy,sxx,sxy,syy=0,0,0,0,0
	for i in range(len(x)):
		sx += x[i]
		sy += y[i]
		sxx += x[i]*x[i]
		sxy += x[i]*y[i]
		syy += y[i]*y[i]
	a = (sx*sy/N - sxy)/(sx*sx/N-sxx)
	b = (sy - a * sx)/N
	r = 0
	for i in range(len(x)):
		i +=(a*x[i] + b - y[i])**2
	r = numpy.sqrt(r)
	return a,b,r

def meanvalue(x,n):
	he = 0
	for i in range(n):
		he += x[i]
	he /= n
	return he

def meansquare(x,n):
	he = 0
	for i in range(n):
		he += x[i]**2
	he /= n
	return he
