import cv2,glob,os,numpy as np,mediapipe as mp, sys
from mediapipe.tasks.python import vision, BaseOptions
det=vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(base_options=BaseOptions(model_asset_path=sys.argv[1]),min_detection_confidence=0.4))
fr=sorted(glob.glob('frames/*.jpg')); boxes=[]
for f in fr:
    rgb=cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2RGB); m=cv2.imread('masks_raw/'+os.path.basename(f)[:-4]+'.png',0)
    ys,xs=np.where(m>128); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
    cy0=max(0,y0-40); cy1=min(1920,y0+int((y1-y0)*0.45)); cx0=max(0,x0-60); cx1=min(1080,x1+60)
    crop=rgb[cy0:cy1,cx0:cx1]; sc=640/max(crop.shape[:2]); crop=np.ascontiguousarray(cv2.resize(crop,None,fx=sc,fy=sc))
    r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=crop))
    b=max(((cx0+d.bounding_box.origin_x/sc,cy0+d.bounding_box.origin_y/sc,d.bounding_box.width/sc,d.bounding_box.height/sc) for d in r.detections),key=lambda q:q[2],default=None)
    boxes.append(b if b else (np.nan,)*4)
B=np.array(boxes,float); idx=np.arange(len(B))
for c in range(4):
    ok=~np.isnan(B[:,c]); B[:,c]=np.interp(idx,idx[ok],B[:,c][ok])
    k=5; p=np.pad(B[:,c],k,mode='edge'); B[:,c]=[np.median(p[i:i+2*k+1]) for i in range(len(B))]
Y,X=np.mgrid[0:1920,0:1080]
for i,f in enumerate(fr):
    name=os.path.basename(f)[:-4]+'.png'; m=cv2.imread('masks_raw/'+name,0).astype(np.float32)
    x,y,w,h=B[i]; cx=x+w/2; cy=y+h*0.45; rx=w*0.66; ry=h*0.80
    ell=((X-cx)/rx)**2+((Y-cy)/ry)**2
    keep=np.where(Y<y, np.clip((1.0-ell)*6,0,1), 1.0)
    cv2.imwrite('masks/'+name,(m*keep).astype(np.uint8))
print('done')
