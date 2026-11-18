import sys,time,glob,os
from rembg import new_session, remove
from PIL import Image
s=new_session(sys.argv[1]); files=sorted(glob.glob(sys.argv[2]+'/*.jpg'))[int(sys.argv[4]):int(sys.argv[5])]
os.makedirs(sys.argv[3],exist_ok=True)
t=time.time()
for f in files:
    im=Image.open(f); m=remove(im,session=s,only_mask=True)
    m.save(os.path.join(sys.argv[3],os.path.basename(f)[:-4]+'.png'))
print(sys.argv[1],(time.time()-t)/max(len(files),1),'s/frame')
