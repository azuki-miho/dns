import xlwt
import pywt
import xlrd
from mytools import *
import matplotlib.pyplot as plt
import numpy as np
m = 20

data = xlrd.open_workbook('g1g20823.xlsx')
g1 = data.sheet_by_name(u'g1')
g2 = data.sheet_by_name(u'g2')

BJe1 = np.zeros((4,20))
BJe2 = np.zeros((4,20))
RGe1 = np.zeros((4,20))
RGe2 = np.zeros((4,20))
FQe1 = np.zeros((4,20))
FQe2 = np.zeros((4,20))
g10 = np.zeros(20)
g20 = np.zeros(20)

for i in range(m):
	g10[i] = g1.cell(i,0).value
	g20[i] = g2.cell(i,0).value
	for j in range(4):
		BJe1[j][i] = g1.cell(i,j+1).value
		RGe1[j][i] = g1.cell(i+m,j+1).value
		FQe1[j][i] = g1.cell(i+2*m,j+1).value
		BJe2[j][i] = g2.cell(i,j+1).value
		RGe2[j][i] = g2.cell(i+m,j+1).value
		FQe2[j][i] = g2.cell(i+2*m,j+1).value
galname = ["GS","EX","DV","SS"]
fig=plt.figure(figsize=(16,12))
xf = numpy.linspace(-0.01,0.01,100)
colorname = ["red","green","blue","yellow"]
markername = ['+','o','*','x']
colorn = ['r','g','b','y']
for i in range(6):
	if i == 0:
		g = g10
		ea = BJe1 
		figure = fig.add_subplot(231)
		plt.ylabel("g1")
	elif i == 1:
		g = g20
		ea = BJe2
		figure = fig.add_subplot(234)
		plt.xlabel("BJ02")
		plt.ylabel("g2")
	elif i == 2:
		g = g10
		ea = RGe1
		figure = fig.add_subplot(232)
		plt.text(0.5,1.2,'Results of Shear Estimation',horizontalalignment='center',fontsize=30,transform=figure.transAxes)
	elif i == 3:
		g = g20
		ea = RGe2
		figure = fig.add_subplot(235)
		plt.xlabel("RG03")
	elif i == 4:
		g = g10
		ea = FQe1
		figure = fig.add_subplot(233)
	else:
		g = g20
		ea = FQe2
		figure = fig.add_subplot(236)
		plt.xlabel("Z11")
	figure.set_aspect("equal")
	figure.set_xlim(-0.01,0.01)
	figure.set_ylim(-0.01,0.01)
	figure.plot(xf,xf,color="black")
	for j in range(4):
		g = numpy.array(g)
		e = numpy.array(ea[j])
		a,b,r = linematch(g,e)
		yf = a*xf+b
		figure.plot(xf,yf,color=colorname[j],label="%s y=%.4fx+%.4f"%(galname[j],a,b))
		figure.scatter(g,e,marker=markername[j],color=colorn[j])
		figure.legend(loc='lower right',fontsize=10)
plt.savefig('20170823.eps')

"""
	for j in range(4):
		sheet.write(j+4*i+1,0,g10[i])
		sheet.write(j+4*i+1,1,g20[i])
		sheet.write(j+4*i+1,2,BJe1[j])
		sheet.write(j+4*i+1,3,BJe2[j])
		sheet.write(j+4*i+1,4,RGe1[j])
		sheet.write(j+4*i+1,5,RGe2[j])
		sheet.write(j+4*i+1,6,Me1[j])
		sheet.write(j+4*i+1,7,Me2[j])
		sheet.write(j+4*i+1,8,Wucha[j])
xieru.save('computeg1g2_0.xlsx')
"""
