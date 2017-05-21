import galsim
import xlwt
import math
import numpy
import random
import pywt
from ellipse import *
from mytools import *
import galsim.hsm as hsm

random_seed=553728
sky_level=1.e1
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
n = 200
m = 3
xiuzheng = 1.6
xz = [1,-1]
k = 0
xieru = xlwt.Workbook()
sheet = xieru.add_sheet(u'sheet1',cell_overwrite_ok=True)

sheet.write(0,0,'g1')
sheet.write(0,1,'g2')
sheet.write(0,2,'BJe1')
sheet.write(0,3,'BJe2')
sheet.write(0,4,'RGe1')
sheet.write(0,5,'RGe2')
sheet.write(0,6,'Me1')
sheet.write(0,7,'Me2')
sheet.write(0,8,'wucha')

e10 =numpy.random.normal(loc=0.0,scale=0.1,size=n)
e20 =numpy.random.normal(loc=0.0,scale=0.04,size=n)
g10 =numpy.random.uniform(-0.03,0.06,m)
g20 =numpy.random.uniform(-0.03,0.06,m)
for i in range(n):
	e20[i] = 0
	if (abs((e10[i]**2)*(e20[i]**2))>1.0):
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
final_epsf_image=psf1.drawImage(scale=pixel_scale)
gal = [gal1,gal2,gal3,gal4]
for i in range(m):
	BJe1array = [[],[],[],[]]
	BJe2array = [[],[],[],[]]
	RGe1array = [[],[],[],[]]
	RGe2array = [[],[],[],[]]
	Me1array = [[],[],[],[]]
	Me2array = [[],[],[],[]]
	for j in range(4):
		for p in range(2):
			for l in range(n):
				k += 1
				rng=galsim.UniformDeviate(random_seed+k+1)
				flux=rng()*(gal_flux_max-gal_flux_min)+gal_flux_min
				this_gal=gal[j].withFlux(flux)
				hlr=rng()*(gal_hlr_max-gal_hlr_min)+gal_hlr_min
				this_gal=this_gal.dilate(hlr)
				this_gal=this_gal.shear(e1=xz[p]*e10[l],e2=xz[p]*e20[l]).shear(g1=g10[i],g2=g20[i])
				final=galsim.Convolve([this_gal,psf])
				print(rng())
				image=galsim.ImageF(nx,ny,scale=pixel_scale)
				fft_image=image[galsim.BoundsI(1,nx,1,ny)]
				final.drawImage(fft_image,method='fft')
				sky_level_pixel=sky_level*pixel_scale**2
				fft_image.addNoise(galsim.PoissonNoise(rng,sky_level=sky_level_pixel))#add noise
				#image
				rst = hsm.EstimateShear(image,final_epsf_image,shear_est='BJ')
				BJe1array[j].append(rst.corrected_e1)
				BJe2array[j].append(rst.corrected_e2)
				rst = hsm.EstimateShear(image,final_epsf_image,shear_est='REGAUSS')
				RGe1array[j].append(rst.corrected_e1)
				RGe2array[j].append(rst.corrected_e2)
				e1,e2 = elli(image.array)
				Me1array[j].append(e1)
				Me2array[j].append(e2)
	BJe1 = []
	BJe2 = []
	RGe1 = []
	RGe2 = []
	Me1 = []
	Me2 = []
	Wucha = []
	for j in range(4):
		BJe1.append(meanvalue(BJe1array[j],2*n)/xiuzheng)
		BJe2.append(meanvalue(BJe2array[j],2*n)/xiuzheng)
		RGe1.append(meanvalue(RGe1array[j],2*n)/xiuzheng)
		RGe2.append(meanvalue(RGe2array[j],2*n)/xiuzheng)
		Me1.append(meanvalue(Me1array[j],2*n)/xiuzheng)
		Me2.append(meanvalue(Me2array[j],2*n)/xiuzheng)
		Wucha.append((meansquare(RGe1array[j],2*n)/10000)**0.5)
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
