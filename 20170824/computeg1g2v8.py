import galsim
import xlwt
import math
import numpy
import random
import pywt
from ellipse import *
from mytools import *
import galsim.hsm as hsm
from mydns import *
import matplotlib.pyplot as plt
from Fourier_Quad import Fourier_Quad

f = open("./20170824/20170824","w")

FQ = Fourier_Quad()
random_seed=553728
sky_level=14.e3
pixel_scale=0.28
nx=64
ny=64
gal_flux_min=1.e4
gal_flux_max=1.e5
gal_hlr_min=0.3
gal_hlr_max=1.3
gal_e_min=0.
gal_e_max=0.8
psf_fwhm=[1.5,0.7,0.6,0.5]
psf_beta=[2.4,2.5,2.3,1.5]
n = 10000
m = 20
xz = [1,-1]
k = 0

xieru = xlwt.Workbook()
sheet1 = xieru.add_sheet(u'g1',cell_overwrite_ok=True)
sheet2 = xieru.add_sheet(u'g2',cell_overwrite_ok=True)

"""
sheet.write(0,0,'g1')
sheet.write(0,1,'g2')
sheet.write(0,2,'BJe1')
sheet.write(0,3,'BJe2')
sheet.write(0,4,'RGe1')
sheet.write(0,5,'RGe2')
sheet.write(0,6,'Me1')
sheet.write(0,7,'Me2')
sheet.write(0,8,'wucha')
"""
sigma1 = 0.3
sigma2 = 0.3
e10 =numpy.random.normal(loc=0.0,scale=sigma1,size=n)
e20 =numpy.random.normal(loc=0.0,scale=sigma2,size=n)
g10 =numpy.random.uniform(-0.01,0.01,m)
g20 =numpy.random.uniform(-0.01,0.01,m)
for i in range(n):
	e20[i] = 0
	if ((e10[i]**2)+(e20[i]**2)>0.64):
		e10[i] = 0.0
		e20[i] = 0.0

gsparams=galsim.GSParams(folding_threshold=1.e-2,maxk_threshold=2.e-3,\
                         xvalue_accuracy=1.e-4,kvalue_accuracy=1.e-4,\
                         shoot_accuracy=1.e-4,minimum_fft_size=64)

#psf1=galsim.Moffat(fwhm=psf_fwhm[0],beta=2.5,gsparams=gsparams) #to be continue
#psf1=psf1.shear(e1=e1_psf,e2=e2_psf)
psf1=galsim.Gaussian(fwhm=psf_fwhm[0],gsparams=gsparams)

#psf1=galsim.Kolmogorov(fwhm=psf_fwhm[0],gsparams=gsparams)
gal1=galsim.Gaussian(half_light_radius=2,gsparams=gsparams)
gal2=galsim.Exponential(half_light_radius=1,gsparams=gsparams)
gal3=galsim.DeVaucouleurs(half_light_radius=1,gsparams=gsparams)
gal4=galsim.Sersic(half_light_radius=1,n=2.5,gsparams=gsparams)#to be continue

psf=psf1
final_epsf_image=psf1.drawImage(nx=nx,ny=ny,scale=pixel_scale)
gal = [gal1,gal2,gal3,gal4]


BJe1 = [[],[],[],[]]
BJe2 = [[],[],[],[]]
RGe1 = [[],[],[],[]]
RGe2 = [[],[],[],[]]
FQe1 = [[],[],[],[]]
FQe2 = [[],[],[],[]]
Me1 = [[],[],[],[]]
Me2 = [[],[],[],[]]
#Wucha = [[],[],[],[]]
snrarray = [[],[],[],[]]
wrongBJarray = [[],[],[],[]]
wrongRGarray = [[],[],[],[]]
for i in range(m):
	print i
	BJe1array = [[],[],[],[]]
	BJe2array = [[],[],[],[]]
	RGe1array = [[],[],[],[]]
	RGe2array = [[],[],[],[]]
	FQe1array = [[],[],[],[]]
	FQe2array = [[],[],[],[]]
	FQnarray = [[],[],[],[]]
	Me1array = [[],[],[],[]]
	Me2array = [[],[],[],[]]
	for j in range(4):
		wrongBJ = 0
		wrongRG = 0
		for l in range(n):
			BJpeerdelete = 0
			RGpeerdelete = 0
			k += 1
			rng=galsim.UniformDeviate(random_seed+k+1)
			flux=rng()*(gal_flux_max-gal_flux_min)+gal_flux_min
			this_gal=gal[j].withFlux(flux)
			hlr=rng()*(gal_hlr_max-gal_hlr_min)+gal_hlr_min
			this_gal=this_gal.dilate(hlr)
			this_gal=this_gal.shear(e1=e10[l],e2=e20[l])
			for p in range(4):
				this_gal_r = this_gal.rotate(theta = p*45*galsim.degrees)
				this_gal_r = this_gal_r.shear(g1 = g10[i],g2 = g20[i])
				final=galsim.Convolve([this_gal_r,psf])
				#print(rng())
				image=galsim.ImageF(nx,ny,scale=pixel_scale)
				image0=galsim.ImageF(nx,ny,scale=pixel_scale)
				fft_image=image[galsim.BoundsI(1,nx,1,ny)]
				fft_image0=image0[galsim.BoundsI(1,nx,1,ny)]
				final.drawImage(fft_image,method='fft')
				final.drawImage(fft_image0,method='fft')
				sky_level_pixel=sky_level*pixel_scale**2
				fft_image.addNoise(galsim.PoissonNoise(rng,sky_level=sky_level_pixel))#add noise
				#image
				snrog = snr(image0.array,image.array)
				snrarray[j].append(snrog)
				#print snrog
				FQg1,FQg2,FQn,FQu,FQv = FQ.shear_est(image.array,final_epsf_image.array,64,background_noise=True,F=False)
				FQe1array[j].append(FQg1)
				FQe2array[j].append(FQg2)
				FQnarray[j].append(FQn)
				if BJpeerdelete != 1:
					rst = hsm.EstimateShear(image,final_epsf_image,shear_est='BJ')
					if rst == 1:
						wrongBJ = wrongBJ + 4
						if p == 0:
							BJpeerdelete = 1
						else:
							for sc in range(p):
								BJe1array[j].pop()
								BJe2array[j].pop()
					else:
						BJe1array[j].append(rst.corrected_e1)
						BJe2array[j].append(rst.corrected_e2)
				if p == 3:
					BJpeerdelete = 0
				if RGpeerdelete != 1:
					rst = hsm.EstimateShear(image,final_epsf_image,shear_est='REGAUSS')
					if rst == 1:
						wrongRG = wrongRG + 4
						if p==0:
							RGpeerdelete = 1
						else:
							for sc in range(p):
								RGe1array[j].pop()
								RGe2array[j].pop()
					else:
						RGe1array[j].append(rst.corrected_e1)
						RGe2array[j].append(rst.corrected_e2)
				if p == 3:
					RGpeerdelete = 0
				#e1,e2 = elli(image.array)
				#Me1array[j].append(e1)
				#Me2array[j].append(e2)
		BJe1meansquare = meansquare(BJe1array[j],4*n-wrongBJ)
		BJe2meansquare = meansquare(BJe2array[j],4*n-wrongBJ)
		RGe1meansquare = meansquare(RGe1array[j],4*n-wrongRG)
		RGe2meansquare = meansquare(RGe2array[j],4*n-wrongRG)
		BJe1[j].append(meanvalue(BJe1array[j],4*n-wrongBJ)/(2-BJe1meansquare-BJe2meansquare))
		BJe2[j].append(meanvalue(BJe2array[j],4*n-wrongBJ)/(2-BJe1meansquare-BJe2meansquare))
		RGe1[j].append(meanvalue(RGe1array[j],4*n-wrongRG)/(2-RGe1meansquare-RGe2meansquare))
		RGe2[j].append(meanvalue(RGe2array[j],4*n-wrongRG)/(2-RGe1meansquare-RGe2meansquare))
		FQe1[j].append(meanvalue(FQe1array[j],4*n)/meanvalue(FQnarray[j],4*n))
		FQe2[j].append(meanvalue(FQe2array[j],4*n)/meanvalue(FQnarray[j],4*n))
		f.write("wrongBJ %f\n"%wrongBJ)
		f.write("wrongRG %f\n"%wrongRG)
		wrongBJarray[j].append(wrongBJ)
		wrongRGarray[j].append(wrongRG)
		#Me1[j].append(meanvalue(Me1array[j],2*n)/xiuzheng)
		#Me2[j].append(meanvalue(Me2array[j],2*n)/xiuzheng)
		#Wucha[j].append((meansquare(RGe1array[j],2*n)/10000)**0.5)

for i in range(m):
	sheet1.write(i,0,g10[i])
	sheet1.write(m+i,0,g10[i])
	sheet1.write(2*m+i,0,g10[i])
	sheet2.write(i,0,g20[i])
	sheet2.write(m+i,0,g20[i])
	sheet2.write(2*m+i,0,g20[i])
	for j in range(4):
		sheet1.write(i,j+1,BJe1[j][i])
		sheet1.write(i+m,j+1,RGe1[j][i])
		sheet1.write(i+m*2,j+1,FQe1[j][i])
		sheet2.write(i,j+1,BJe2[j][i])
		sheet2.write(i+m,j+1,RGe2[j][i])
		sheet2.write(i+m*2,j+1,FQe2[j][i])

xieru.save("g1g20824.xlsx")

galname = ["GS","EX","DV","SS"]
f.write("final\n")
for j in range(4):
	f.write(galname[j]+"wrongBJ%f\n"%meanvalue(wrongBJarray[j],m))
	f.write(galname[j]+"wrongRG%f\n"%meanvalue(wrongRGarray[j],m))
f.close()
snra = []
for i in range(4):
	snra.append(meanvalue(snrarray[i],2*n))
fig=plt.figure()
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
		figure.set_title("The GS's snr:%.1f The EX's snr:%.1f The DV's snr:%.1f The SS's snr%.1f"%(snra[0],snra[1],snra[2],snra[3]),fontsize=8)
		figure.legend(loc='lower right',fontsize=10)
plt.show()

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
