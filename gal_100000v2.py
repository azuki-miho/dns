import galsim
import math
import numpy
import random
import time
start = time.clock()
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
n = 500
e10 =numpy.random.normal(loc=0.0,scale=0.1,size=n)
e20 =numpy.random.normal(loc=0.0,scale=0.04,size=n)
for i in range(n):
	e20[i] = 0
	if (abs((e10[i]**2)*(e20[i]**2))>1.0):
		e10[i] = 0.0
		e20[i] = 0.0

e1_psf = 0.01
e2_psf = -0.005
gm1 = 0.5
gm2 = 0.005
gsparams=galsim.GSParams(folding_threshold=1.e-2,maxk_threshold=2.e-3,\
                         xvalue_accuracy=1.e-4,kvalue_accuracy=1.e-4,\
                         shoot_accuracy=1.e-4,minimum_fft_size=64)

psf1=galsim.Moffat(fwhm=psf_fwhm[0],beta=2.5,gsparams=gsparams) #to be continue
#psf1=psf1.shear(e1=e1_psf,e2=e2_psf)
#psf1=galsim.Gaussian(fwhm=psf_fwhm[0],gsparams=gsparams)

#psf1=galsim.Kolmogorov(fwhm=psf_fwhm[0],gsparams=gsparams)
gal1=galsim.Gaussian(half_light_radius=2,gsparams=gsparams)
gal2=galsim.Exponential(half_light_radius=1,gsparams=gsparams)
gal3=galsim.DeVaucouleurs(half_light_radius=1,gsparams=gsparams)
gal4=galsim.Sersic(half_light_radius=1,n=2.5,gsparams=gsparams)#to be continue

psf=psf1
k=0
galarray1 = []
galarray2 = []
galarray3 = []
galarray4 = []
galarray1Sd = []
galarray2Sd = []
galarray3Sd = []
galarray4Sd = []
for i in range(n):
	k += 1
	rng=galsim.UniformDeviate(random_seed+k+1)
	flux=rng()*(gal_flux_max-gal_flux_min)+gal_flux_min
	this_gal=gal1.withFlux(flux)
	hlr=rng()*(gal_hlr_max-gal_hlr_min)+gal_hlr_min
	this_gal=this_gal.dilate(hlr)
	this_gal=this_gal.shear(e1=e10[i],e2=e20[i])#.shear(g1=gm1,g2=gm2)
	final=galsim.Convolve([this_gal,psf])
	
	print(rng())
	image=galsim.ImageF(nx,ny,scale=pixel_scale)
	fft_image=image[galsim.BoundsI(1,nx,1,ny)]
	final.drawImage(fft_image,method='fft')
	
	sky_level_pixel=sky_level*pixel_scale**2
	fft_image.addNoise(galsim.PoissonNoise(rng,sky_level=sky_level_pixel))#add noise
	
	galarray1Sd.append(image)
	galarray1.append(image.array)
for i in range(n):
	k += 1
	rng=galsim.UniformDeviate(random_seed+k+1)
	flux=rng()*(gal_flux_max-gal_flux_min)+gal_flux_min
	this_gal=gal2.withFlux(flux)
	hlr=rng()*(gal_hlr_max-gal_hlr_min)+gal_hlr_min
	this_gal=this_gal.dilate(hlr)
	this_gal=this_gal.shear(e1=e10[i],e2=e20[i])#.shear(g1=gm1,g2=gm2)
	final=galsim.Convolve([this_gal,psf])
	
	print(rng())
		
	image=galsim.ImageF(nx,ny,scale=pixel_scale)
	fft_image=image[galsim.BoundsI(1,nx,1,ny)]
	final.drawImage(fft_image,method='fft')
	
	sky_level_pixel=sky_level*pixel_scale**2
	fft_image.addNoise(galsim.PoissonNoise(rng,sky_level=sky_level_pixel))#add noise
		
	
	galarray2Sd.append(image)
	galarray2.append(image.array)
for i in range(n):
	k += 1
	rng=galsim.UniformDeviate(random_seed+k+1)
	flux=rng()*(gal_flux_max-gal_flux_min)+gal_flux_min
	this_gal=gal3.withFlux(flux)
	hlr=rng()*(gal_hlr_max-gal_hlr_min)+gal_hlr_min
	this_gal=this_gal.dilate(hlr)
	this_gal=this_gal.shear(e1=e10[i],e2=e20[i])#.shear(g1=0.5,g2=0.5)
	final=galsim.Convolve([this_gal,psf])
	
	print(rng())
		
	
	image=galsim.ImageF(nx,ny,scale=pixel_scale)
	fft_image=image[galsim.BoundsI(1,nx,1,ny)]
	final.drawImage(fft_image,method='fft')
	
	sky_level_pixel=sky_level*pixel_scale**2
	fft_image.addNoise(galsim.PoissonNoise(rng,sky_level=sky_level_pixel))#add noise
		
	
	galarray3Sd.append(image)
	galarray3.append(image.array)
for i in range(n):
	k += 1
	rng=galsim.UniformDeviate(random_seed+k+1)
	flux=rng()*(gal_flux_max-gal_flux_min)+gal_flux_min
	this_gal=gal4.withFlux(flux)
	hlr=rng()*(gal_hlr_max-gal_hlr_min)+gal_hlr_min
	this_gal=this_gal.dilate(hlr)
	this_gal=this_gal.shear(e1=e10[i],e2=e20[i])#.shear(g1=0.5,g2=0.5)
	final=galsim.Convolve([this_gal,psf])
	
	print(rng())
		
	
	image=galsim.ImageF(nx,ny,scale=pixel_scale)
	fft_image=image[galsim.BoundsI(1,nx,1,ny)]
	final.drawImage(fft_image,method='fft')
	
	sky_level_pixel=sky_level*pixel_scale**2
	fft_image.addNoise(galsim.PoissonNoise(rng,sky_level=sky_level_pixel))#add noise
		
	
	galarray4Sd.append(image)
	galarray4.append(image.array)
final_epsf_image=psf.drawImage(scale=pixel_scale)
