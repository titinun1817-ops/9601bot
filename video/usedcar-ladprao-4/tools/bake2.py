import sys,json,subprocess,numpy as np,cv2,math
W,H=2160,3840
segs=json.load(open(sys.argv[1])); src=sys.argv[2]; out=sys.argv[3]
def ease(u,k):
    u=min(max(u,0),1); return u*u*(3-2*u) if k=='s' else 1-2**(-10*u)
def cam(t):
    for t0,t1,z0,z1,c0,c1,k in segs:
        if t<t1:
            e=ease((t-t0)/(t1-t0),k); return z0+(z1-z0)*e, c0+(c1-c0)*e
dec=subprocess.Popen(['ffmpeg','-v','error','-ss','0.3','-i',src,'-t','14.3','-vf','fps=30','-pix_fmt','bgr24','-f','rawvideo','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','14','-preset','medium','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
n=0;cams=[]
while True:
    b=dec.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3); t=n/30
    z,cy=cam(t); cw,ch=W/z,H/z
    y0=min(max(cy*H-ch/2,0),H-ch); x0=(W-cw)/2
    M=np.float32([[1080/cw,0,-x0*1080/cw],[0,1920/ch,-y0*1920/ch]])
    o=cv2.warpAffine(f,M,(1080,1920),flags=cv2.INTER_LANCZOS4)
    enc.stdin.write(o.tobytes()); cams.append([round(t,4),z,x0/W,y0/H]); n+=1
enc.stdin.close(); enc.wait(); json.dump(cams,open(out+'.cam.json','w')); print(n,'frames')
