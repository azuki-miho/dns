from mydns import *
from gal_100000v2 import *
import pywt
from ellipse import *
import numpy as np
import matplotlib.pyplot as plt
from mytools import *
import galsim.hsm as hsm

gal1e1arr = []
gal1e2arr = []
gal2e1arr = []
gal2e2arr = []
gal3e1arr = []
gal3e2arr = []
gal4e1arr = []
gal4e2arr = []

rggal1e1 = []
rggal1e2 = []
rggal2e1 = []
rggal2e2 = []
rggal3e1 = []
rggal3e2 = []
rggal4e1 = []
rggal4e2 = []

bjgal1e1 = []
bjgal1e2 = []
bjgal2e1 = []
bjgal2e2 = []
bjgal3e1 = []
bjgal3e2 = []
bjgal4e1 = []
bjgal4e2 = []

for i in range(n):
	e1,e2 = elli(galarray1[i])
	gal1e1arr.append(e1)
	gal1e2arr.append(e2)
	
	e1,e2 = elli(galarray2[i])
	gal2e1arr.append(e1)
	gal2e2arr.append(e2)
	
	e1,e2 = elli(galarray3[i])
	gal3e1arr.append(e1)
	gal3e2arr.append(e2)
	
	e1,e2 = elli(galarray4[i])
	gal4e1arr.append(e1)
	gal4e2arr.append(e2)
	rst = hsm.EstimateShear(galarray1Sd[i],final_epsf_image,shear_est='REGAUSS')
	rggal1e1.append(rst.corrected_e1)
	rggal1e2.append(rst.corrected_e2)

	rst = hsm.EstimateShear(galarray1Sd[i],final_epsf_image,shear_est='BJ')
	bjgal1e1.append(rst.corrected_e1)
	bjgal1e2.append(rst.corrected_e2)

	rst = hsm.EstimateShear(galarray2Sd[i],final_epsf_image,shear_est='REGAUSS')
	rggal2e1.append(rst.corrected_e1)
	rggal2e2.append(rst.corrected_e2)

	rst = hsm.EstimateShear(galarray2Sd[i],final_epsf_image,shear_est='BJ')
	bjgal2e1.append(rst.corrected_e1)
	bjgal2e2.append(rst.corrected_e2)

	rst = hsm.EstimateShear(galarray3Sd[i],final_epsf_image,shear_est='REGAUSS')
	rggal3e1.append(rst.corrected_e1)
	rggal3e2.append(rst.corrected_e2)
	
	rst = hsm.EstimateShear(galarray3Sd[i],final_epsf_image,shear_est='BJ')
	bjgal3e1.append(rst.corrected_e1)
	bjgal3e2.append(rst.corrected_e2)

	rst = hsm.EstimateShear(galarray4Sd[i],final_epsf_image,shear_est='REGAUSS')
	rggal4e1.append(rst.corrected_e1)
	rggal4e2.append(rst.corrected_e2)
	
	rst = hsm.EstimateShear(galarray4Sd[i],final_epsf_image,shear_est='BJ')
	bjgal4e1.append(rst.corrected_e1)
	bjgal4e2.append(rst.corrected_e2)

gal1e1arr = np.array(gal1e1arr)
gal1e2arr = np.array(gal1e2arr)
gal2e1arr = np.array(gal2e1arr)
gal2e2arr = np.array(gal2e2arr)
gal3e1arr = np.array(gal3e1arr)
gal3e2arr = np.array(gal3e2arr)
gal4e1arr = np.array(gal4e1arr)
gal4e2arr = np.array(gal4e2arr)

rggal1e1 = np.array(rggal1e1)
rggal1e2 = np.array(rggal1e2)
rggal2e1 = np.array(rggal2e1)
rggal2e2 = np.array(rggal2e2)
rggal3e1 = np.array(rggal3e1)
rggal3e2 = np.array(rggal3e2)
rggal4e1 = np.array(rggal4e1)
rggal4e2 = np.array(rggal4e2)

bjgal1e1 = np.array(bjgal1e1)
bjgal1e2 = np.array(bjgal1e2)
bjgal2e1 = np.array(bjgal2e1)
bjgal2e2 = np.array(bjgal2e2)
bjgal3e1 = np.array(bjgal3e1)
bjgal3e2 = np.array(bjgal3e2)
bjgal4e1 = np.array(bjgal4e1)
bjgal4e2 = np.array(bjgal4e2)

e10 = np.array(e10)
e20 = np.array(e20)
"""
varsig = 0
for i in range(200):
	s1 = (sige[i][0]-orge[i][0])/orge[i][0]
	s2 = (sige[i][1]-orge[i][1])/orge[i][1]
	var = s1**2 + s2**2
	varsig += var
"""



"""
print("This is the variance of the signal")
print(varsig)
#testsnr for lpdn
min_var = 0
elp = []
for j in range(40):
	varlp = 0
	for i in range(200):
		lpimage = lpdn(galarray[i],r=j+3)
		(e1,e2) = elli(lpimage)
"""			

xf = np.linspace(-1,1,1000)

fig=plt.figure()
fig1=fig.add_subplot(221)
a,b,r=linematch(e10,gal1e1arr)
fig1.set_title("the Gaussian model")

yf = a*xf + b
fig1.plot(xf,yf,color="blue")
fig1.scatter(e10,gal1e1arr,marker='o',color='b',label='origin y=%fx+%f'%(a,b))

a,b,r=linematch(e10,rggal1e1)
yf = a*xf + b
fig1.plot(xf,yf,color="red")
fig1.scatter(e10,rggal1e1,marker='x',color='r',label='REGAUSS Method y=%fx+%f'%(a,b))

a,b,r=linematch(e10,bjgal1e1)
yf = a*xf + b
fig1.plot(xf,yf,color="green")
fig1.scatter(e10,bjgal1e1,marker='+',color='g',label='BJ Method y=%fx+%f'%(a,b))

fig1.plot(xf,xf,color="black")
fig1.legend(loc='upper right')
############################
fig2=fig.add_subplot(222)
a,b,r=linematch(e10,gal2e1arr)
fig2.set_title("the Exponential model")

yf = a*xf + b
fig2.plot(xf,yf,color="blue")
fig2.scatter(e10,gal2e1arr,marker='o',color='b',label='origin y=%fx+%f'%(a,b))

a,b,r=linematch(e10,rggal2e1)
yf = a*xf + b
fig2.plot(xf,yf,color="red")
fig2.scatter(e10,rggal2e1,marker='x',color='r',label='REGAUSS Method y=%fx+%f'%(a,b))

a,b,r=linematch(e10,bjgal1e1)
yf = a*xf + b
fig2.plot(xf,yf,color="green")
fig2.scatter(e10,bjgal2e1,marker='+',color='g',label='BJ Method y=%fx+%f'%(a,b))

fig2.plot(xf,xf,color="black")
fig2.legend(loc='upper right')
############################
fig3=fig.add_subplot(223)
a,b,r=linematch(e10,gal3e1arr)
fig3.set_title("the DeVaucouleurs model")

yf = a*xf + b
fig3.plot(xf,yf,color="blue")
fig3.scatter(e10,gal3e1arr,marker='o',color='b',label='origin y=%fx+%f'%(a,b))

a,b,r=linematch(e10,rggal3e1)
yf = a*xf + b
fig3.plot(xf,yf,color="red")
fig3.scatter(e10,rggal3e1,marker='x',color='r',label='REGAUSS Method y=%fx+%f'%(a,b))

a,b,r=linematch(e10,bjgal3e1)
yf = a*xf + b
fig3.plot(xf,yf,color="green")
fig3.scatter(e10,bjgal3e1,marker='+',color='g',label='BJ Method y=%fx+%f'%(a,b))

fig3.plot(xf,xf,color="black")
fig3.legend(loc='upper right')
##############################

fig4=fig.add_subplot(224)
a,b,r=linematch(e10,gal4e1arr)
fig4.set_title("the Sersic model")
fig4.scatter(e10,gal4e1arr)

yf = a*xf + b
fig4.plot(xf,yf,color="blue")
fig4.scatter(e10,gal4e1arr,marker='o',color='b',label='origin y=%fx+%f'%(a,b))

a,b,r=linematch(e10,rggal4e1)
yf = a*xf + b
fig4.plot(xf,yf,color="red")
fig4.scatter(e10,rggal4e1,marker='x',color='r',label='REGAUSS Method y=%fx+%f'%(a,b))

a,b,r=linematch(e10,bjgal4e1)
yf = a*xf + b
fig4.plot(xf,yf,color="green")
fig4.scatter(e10,bjgal4e1,marker='+',color='g',label='BJ Method y=%fx+%f'%(a,b))
fig4.legend(loc='upper right')

fig4.plot(xf,xf,color="black")
end = time.clock()
print(end-start)
plt.show()

	
"""
#testsnr for mvdn
min_var = 0
for k in range(4):
	varmv = 0
	for i in range(200):
		mvimage = mvdn(galarray[i],rg=k+1)
		(e1,e2) = elli(mvimage)
		s1 = (e1-orge[i][0])/orge[i][0]
		s2 = (e2-orge[i][1])/orge[i][1]
		s = s1**2 + s2**2
		varmv += s
	if (min_var == 0):
		min_var = varmv
		print("This is the variance for the mvdn")
		print(varmv);print(k+1)
	else:
		if (varmv <= min_var):
			min_var = varmv
			print("This is the variance for the mvdn")
			print(varmv);print(k+1)

#testsnr for wldn1
min_var = 0
for j in range(5):
	varwl1 = 0
	for i in range(200):
		wlimage1 = wldn1(galarray[i],k=j)
		(e1,e2) = elli(wlimage1)
		s1 = (e1-orge[i][0])/orge[i][0]
		s2 = (e2-orge[i][1])/orge[i][1]
		s = s1**2 + s2**2
		varwl1 += s
	if (min_var == 0):
		min_var = varwl1
		print("This is the variance for the wldn1")
		print(varwl1);print(j+1)
	else:
		if (varwl1 <= min_var):
			min_var = varwl1
			print("This is the variance for the wldn1")
			print(varwl1);print(j+1)
#testsnr for wldn2
wls = pywt.wavelist()[0:15]+pywt.wavelist()[24:80]+[pywt.wavelist()[89],]
wls = wls + pywt.wavelist()[92:107]+pywt.wavelist()[108:]
min_var = 0
for j in range(len(wls)):
	for k in range(5):
		varwl2 = 0
		for i in range(200):
			wlimage2 = wldn2(galarray[i],rat=k/10.,wav=wls[j])
			(e1,e2) = elli(wlimage2)
			s1 = (e1-orge[i][0])/orge[i][0]
			s2 = (e2-orge[i][1])/orge[i][1]
			s = s1**2 + s2**2
			varwl2 += s
		if (min_var == 0):
			min_var =varwl2
			print("This is the variance for the");print(wls[j]);print(varwl2)
			print(k/10.)
		else:
			if (varwl2 <= min_var):
				min_var =varwl2
				print("This is the variance for the");print(wls[j])
				print(varwl2);print(k/10.)
"""
