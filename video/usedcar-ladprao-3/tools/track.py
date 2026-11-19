import cv2,numpy as np,json
import sys
ref,start,end=map(int,sys.argv[1:4])
def g(n): return cv2.cvtColor(cv2.imread('frames/%04d.jpg'%n),cv2.COLOR_BGR2GRAY)
r=g(ref); mask=np.zeros_like(r); mask[150:700,350:1000]=255
p0=cv2.goodFeaturesToTrack(r,400,0.01,8,mask=mask)
out={}
for n in range(start,end+1):
    if n>end: break
    try: im=g(n)
    except: break
    p1,st,_=cv2.calcOpticalFlowPyrLK(r,im,p0,None,winSize=(31,31),maxLevel=4)
    ok=st[:,0]==1
    M,_=cv2.estimateAffinePartial2D(p0[ok],p1[ok],method=cv2.RANSAC)
    out[n]=[round(float(M[0,0]),5),round(float(M[1,0]),5),round(float(M[0,2]),2),round(float(M[1,2]),2)]
json.dump(out,open('track.json','w'))
for k in list(out)[::20]: print(k,out[k])
