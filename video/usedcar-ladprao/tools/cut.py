import cv2,numpy as np,glob,os,subprocess
fr=sorted(glob.glob('frames/*.jpg')); os.makedirs('cut',exist_ok=True); os.makedirs('ring',exist_ok=True)
prev=None
for i,f in enumerate(fr):
    im=cv2.imread(f); m=cv2.imread('masks/'+os.path.basename(f)[:-4]+'.png',0).astype(np.float32)/255
    if prev is not None: m=0.6*m+0.4*prev   # temporal smoothing against flicker
    prev=m
    mb=(m>0.5).astype(np.uint8)
    mb=cv2.erode(mb,np.ones((3,3),np.uint8),1)
    a=cv2.GaussianBlur(mb.astype(np.float32),(0,0),1.6)
    rgba=np.dstack([im,(a*255).astype(np.uint8)])
    cv2.imwrite('cut/%04d.png'%(i+1),rgba)
    d=cv2.dilate(mb,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25)))
    ring=cv2.GaussianBlur(np.clip(d.astype(np.float32)-mb,0,1),(0,0),5)*1.6
    glow=cv2.GaussianBlur(d.astype(np.float32),(0,0),22)*0.55
    al=np.clip(np.maximum(ring,glow)*(1-a),0,1)
    out=np.dstack([np.full_like(im,255),(al*255).astype(np.uint8)])
    cv2.imwrite('ring/%04d.png'%(i+1),out)
