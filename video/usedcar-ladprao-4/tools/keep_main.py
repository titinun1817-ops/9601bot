# Keep only the presenter in rembg masks: drop passers-by (keep the largest connected blob).
import cv2,glob,os,numpy as np,sys
src=sys.argv[1]
for f in sorted(glob.glob(src+'/*.png')):
    m=cv2.imread(f,0); n,lab,st,_=cv2.connectedComponentsWithStats((m>64).astype(np.uint8))
    if n<=2: continue
    k=1+int(np.argmax(st[1:,cv2.CC_STAT_AREA])); keep=cv2.dilate((lab==k).astype(np.uint8),np.ones((9,9),np.uint8))
    cv2.imwrite(f,(m*keep).astype(np.uint8))
print('ok')
