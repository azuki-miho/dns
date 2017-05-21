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
n = 50
e10 =numpy.random.normal(loc=0.0,scale=0.7,size=n)
e20 =numpy.random.normal(loc=0.0,scale=0.04,size=n)
for i in range(n):
	e20[i] = 0
	if abs(e10[i]) >=0.99:
		e10[i] = 0
	#if abs(e20[i]) >=0.01:
		#e20[i] = 0
e1_psf = 0.02
e2_psf = 0.005
gm1 = 0.5
gm2 = 0.005
gsparams=galsim.GSParams(folding_threshold=1.e-2,maxk_threshold=2.e-3,\
                         xvalue_accuracy=1.e-4,kvalue_accuracy=1.e-4,\
                         shoot_accuracy=1.e-4,minimum_fft_size=64)
psf1=galsim.Gaussian(fwhm=psf_fwhm[0],gsparams=gsparams) #to be continue
psf1=psf1#.shear(e1=e1_psf,e2=e2_psf)

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
	image=galsim.ImageF(2*nx+2,ny,scale=pixel_scale)
	fft_image=image[galsim.BoundsI(1,nx,1,ny)]
	phot_image=image[galsim.BoundsI(nx+3,2*nx+2,1,ny)]
	final.drawImage(fft_image,method='fft')
	
	sky_level_pixel=sky_level*pixel_scale**2
	fft_image.addNoise(galsim.PoissonNoise(rng,sky_level=sky_level_pixel))#add noise
	rng=galsim.UniformDeviate(random_seed+k+1)
	rng();rng();rng();rng();
	final.drawImage(phot_image,method='phot',max_extra_noise=sky_level_pixel/100,\
	
	                rng=rng)
	pd=galsim.PoissonDeviate(rng,mean=sky_level_pixel)
	phot_image.addNoise(galsim.DeviateNoise(pd))
	phot_image -= sky_level_pixel
		
	
	imagea = image.array
	galarray1.append(imagea[0:64,0:64])
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
		
	image=galsim.ImageF(2*nx+2,ny,scale=pixel_scale)
	fft_image=image[galsim.BoundsI(1,nx,1,ny)]
	phot_image=image[galsim.BoundsI(nx+3,2*nx+2,1,ny)]
	final.drawImage(fft_image,method='fft')
	
	sky_level_pixel=sky_level*pixel_scale**2
	fft_image.addNoise(galsim.PoissonNoise(rng,sky_level=sky_level_pixel))#add noise
	rng=galsim.UniformDeviate(random_seed+k+1)
	rng();rng();rng();rng();
	final.drawImage(phot_image,method='phot',max_extra_noise=sky_level_pixel/100,\
	
	                rng=rng)
	pd=galsim.PoissonDeviate(rng,mean=sky_level_pixel)
	phot_image.addNoise(galsim.DeviateNoise(pd))
	phot_image -= sky_level_pixel
		
	
	imagea = image.array
	galarray2.append(imagea[0:64,0:64])
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
		
	
	image=galsim.ImageF(2*nx+2,ny,scale=pixel_scale)
	fft_image=image[galsim.BoundsI(1,nx,1,ny)]
	phot_image=image[galsim.BoundsI(nx+3,2*nx+2,1,ny)]
	final.drawImage(fft_image,method='fft')
	
	sky_level_pixel=sky_level*pixel_scale**2
	fft_image.addNoise(galsim.PoissonNoise(rng,sky_level=sky_level_pixel))#add noise
	rng=galsim.UniformDeviate(random_seed+k+1)
	rng();rng();rng();rng();
	final.drawImage(phot_image,method='phot',max_extra_noise=sky_level_pixel/100,\
	
	                rng=rng)
	pd=galsim.PoissonDeviate(rng,mean=sky_level_pixel)
	phot_image.addNoise(galsim.DeviateNoise(pd))
	phot_image -= sky_level_pixel
		
	
	imagea = image.array
	galarray3.append(imagea[0:64,0:64])
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
		
	
	image=galsim.ImageF(2*nx+2,ny,scale=pixel_scale)
	fft_image=image[galsim.BoundsI(1,nx,1,ny)]
	phot_image=image[galsim.BoundsI(nx+3,2*nx+2,1,ny)]
	final.drawImage(fft_image,method='fft')
	
	sky_level_pixel=sky_level*pixel_scale**2
	fft_image.addNoise(galsim.PoissonNoise(rng,sky_level=sky_level_pixel))#add noise
	rng=galsim.UniformDeviate(random_seed+k+1)
	rng();rng();rng();rng();
	final.drawImage(phot_image,method='phot',max_extra_noise=sky_level_pixel/100,\
	
	                rng=rng)
	pd=galsim.PoissonDeviate(rng,mean=sky_level_pixel)
	phot_image.addNoise(galsim.DeviateNoise(pd))
	phot_image -= sky_level_pixel
		
	
	imagea = image.array
	galarray4.append(imagea[0:64,0:64])
