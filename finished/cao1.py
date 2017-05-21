import numpy as np
import matplotlib.pyplot as plt
def expon(I0,x,y,f,re,nsers):
    r=np.sqrt(x**2/f+y**2*f)
    res=I0*np.exp(-7.669*((r/re)**(1.0/nsers)-1.0))
    return res

def main():
    g1=0.01
    g2=0.002
    k=0
    xg=yg=np.mgrid[0:99,0:99]
    image1=np.zeros((99,99))
    image2=np.zeros((99,99))
    I0=500.0
    f=0.6
    re=10.0
    nsers=4
    fwhm=5.0
    nrand=5000
    A=np.array([[1+g1-k,g2],[g2,1-g1-k]])
    Rot=np.array([[0.,-1.],[1.,0.]])
    for i in range(nrand):
        x,y=np.random.randint(low=0,high=98,size=2)
        #B=np.array([[x],[y]])
        #C=np.dot(Rot,B)
        xr=x-49
        yr=y-49
        xt=-yr
        yt=xr
        lum1=expon(I0,xr,yr,f,re,nsers)
        lum2=expon(I0,xt,yt,f,re,nsers)
        print(lum1)
        gauss1=np.exp(-0.5*(xr**2/f+yr**2*f)/fwhm/fwhm)
        print(gauss1)
        gauss2=np.exp(-0.5*(xr**2/f+yr**2*f)/fwhm/fwhm)
        xtz=xt+49
        ytz=yt+49
        image1[x][y]=image1[x][y]+gauss1*lum1
        image2[xtz][ytz]=image2[xtz][ytz]+gauss2*lum2
    image=np.zeros((99,198))
    for i in range(99):
        image[i]=image[i]+np.append(image1[i],image2[i])
    plt.imshow(image)
    plt.show()
    #plt.imshow(image2)
    #plt.show()

if  __name__=='__main__':
    main()
        
