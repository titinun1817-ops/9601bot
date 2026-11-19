import sys,json,subprocess,numpy as np,cv2
W,H=720,1280
segs=json.load(open(sys.argv[1])); src=sys.argv[2]; out=sys.argv[3]
def ease(u,k):
    u=min(max(u,0),1); return u*u*(3-2*u) if k=='s' else 1-2**(-10*u)
def cyz(z):  # keep burned-in logo (y .785-.92) under the footer band (top .781 of frame)
    y0=max(0.0,0.785-0.781/z-0.005); return y0+0.5/z
def cam(t):
    for t0,t1,z0,z1,k in segs:
        if t<t1: return z0+(z1-z0)*ease((t-t0)/(t1-t0),k)
    return segs[-1][3]
dec=subprocess.Popen(['ffmpeg','-v','error','-i',src,'-vf','fps=30','-pix_fmt','bgr24','-f','rawvideo','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','-','-vf','unsharp=5:5:0.6','-c:v','libx264','-crf','14','-preset','medium','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
n=0
while True:
    b=dec.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3); z=cam(n/30); cy=cyz(z)
    cw,ch=W/z,H/z; y0=min(max(cy*H-ch/2,0),H-ch); x0=(W-cw)/2
    M=np.float32([[1080/cw,0,-x0*1080/cw],[0,1920/ch,-y0*1920/ch]])
    enc.stdin.write(cv2.warpAffine(f,M,(1080,1920),flags=cv2.INTER_LANCZOS4).tobytes()); n+=1
enc.stdin.close(); enc.wait(); print(n,'frames')
