# Re-time a composition built for the first Ladprao clip onto this clip's speech (piecewise-linear).
import re,sys,json,os,numpy as np
A=json.load(open(os.path.join(os.path.dirname(__file__),os.environ.get('ANCHORS','anchors.json'))))
_OLD=[(0,0),(0.24,0.18),(0.9,0.8),(1.48,1.38),(1.94,1.74),(2.6,2.46),(3.14,3.22),(3.58,3.62),(4.72,4.9),(4.75,4.93),
   (5.34,5.9),(5.84,6.32),(6.08,6.7),(6.75,7.4),(7.28,8.12),(7.52,8.28),(7.88,8.58),(8.16,8.86),(8.58,9.5),
   (9.74,10.64),(10.24,11.12),(10.76,11.44),(10.9,11.75),(13.0,13.4)]
xo,xn=zip(*A)
def f(t): return round(float(np.interp(t,xo,xn)),3)
def fix(s):
    def ds(m):
        st=float(m.group(2)); du=float(m.group(4)); ns=f(st); ne=f(st+du)
        return f'{m.group(1)}{ns}{m.group(3)}{round(ne-ns,3)}"'
    s=re.sub(r'(data-start=")([\d.]+)("[^>]*?data-duration=")([\d.]+)"',ds,s)
    s=re.sub(r'(data-media-start=")([\d.]+)"',lambda m:f'{m.group(1)}{f(float(m.group(2)))}"',s)
    s=re.sub(r'\}, ([\d.]+)(\)| \+)',lambda m:f'}}, {f(float(m.group(1)))}{m.group(2)}',s)
    s=re.sub(r'(shake\()([\d.]+),',lambda m:f'{m.group(1)}{f(float(m.group(2)))},',s)
    s=re.sub(r'(", )([\d.]+)\]',lambda m:f'{m.group(1)}{f(float(m.group(2)))}]',s)
    return s
for p in sys.argv[1:]:
    s=open(p).read(); open(p,'w').write(fix(s)); print('retimed',p)
