# Dead-air cut: concat the kept source ranges of IMG_7745 into one 4K file (video+audio), and map source time -> new time.
import json,subprocess,sys,os
D=json.load(open(os.path.join(os.path.dirname(__file__),'deadair.json'))); K=D['keep']
def n(s):
    t=0
    for a,b in K:
        if s<a: return t
        if s<=b: return t+(s-a)
        t+=b-a
    return t+(s-K[-1][1])
if __name__=='__main__':
    src,out=sys.argv[1:3]; fc=''; cat=''
    for i,(a,b) in enumerate(K):
        fc+=f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a:0]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={b-a-0.012:.3f}:d=0.012[a{i}];'
        cat+=f'[v{i}][a{i}]'
    fc+=f'{cat}concat=n={len(K)}:v=1:a=1[v][a]'
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-crf','12','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k',out],check=True)
    print('kept',round(sum(b-a for a,b in K),3))
