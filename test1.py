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

FQ = Fourier_Quad()
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
n = 2500
m = 4
xiuzheng = 1.82
xz = [1,-1]
k = 0
"""
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
"""
e10 =numpy.random.normal(loc=0.0,scale=0.3,size=n)
e20 =numpy.random.normal(loc=0.0,scale=0.3,size=n)
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

