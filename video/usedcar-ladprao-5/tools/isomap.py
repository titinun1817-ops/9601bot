# Generates the isometric map markup + GSAP for compositions/front.html (#fr-map)
import math
S=44; C=math.cos(math.pi/6); SN=0.5; OX=450; OY=70
def P(x,y,z=0): return (round((x-y)*C*S+OX,1), round((x+y)*SN*S-z*S+OY,1))
def poly(pts,fill,extra=''): return f'<polygon points="{" ".join(f"{a},{b}" for a,b in pts)}" fill="{fill}" {extra}/>'
out=[]; js=[]
# slab
T=0.55
top=[P(0,0),P(10,0),P(10,10),P(0,10)]
out.append('<g id="im-slab">'+poly([P(10,0),P(10,10),P(10,10,-T),P(10,0,-T)],'#c9cdd4')+poly([P(0,10),P(10,10),P(10,10,-T),P(0,10,-T)],'#dfe2e7')+poly(top,'#f3f4f6')+'</g>')
# grass patches
out.append('<g id="im-grass">'+poly([P(0.3,0.3),P(4.9,0.3),P(4.9,5.7),P(0.3,5.7)],'#e3f1df')+poly([P(6.5,0.3),P(9.7,0.3),P(9.7,5.7),P(6.5,5.7)],'#e3f1df')+poly([P(0.3,7.7),P(9.7,7.7),P(9.7,9.7),P(0.3,9.7)],'#e3f1df')+'</g>')
# roads
road_main=[P(0,6),P(10,6),P(10,7.4),P(0,7.4)]; soi=[P(5.2,0),P(6.2,0),P(6.2,6),P(5.2,6)]
dash=' '.join(f'{a},{b}' for a,b in [P(0,6.7),P(10,6.7)])
dash2=' '.join(f'{a},{b}' for a,b in [P(5.7,0),P(5.7,6)])
out.append('<g id="im-road1">'+poly(road_main,'#3f434c')+f'<polyline points="{dash}" stroke="#fff" stroke-width="4" stroke-dasharray="18 14" fill="none"/></g>')
out.append('<g id="im-road2">'+poly(soi,'#4a4e57')+f'<polyline points="{dash2}" stroke="#fff" stroke-width="3" stroke-dasharray="12 10" fill="none"/></g>')
# iso road labels
a,b=P(0.9,7.15); out.append(f'<text id="im-lbl1" transform="matrix({C:.3f},{SN},{-C:.3f},{SN},{a},{b})" font-family="Kanit" font-weight="800" font-size="30" fill="#fff">ถ.ลาดพร้าว</text>')
a,b=P(5.95,0.6); out.append(f'<text id="im-lbl2" transform="matrix({-C:.3f},{SN},{C:.3f},{SN},{a},{b})" font-family="Kanit" font-weight="800" font-size="24" fill="#fff" transform-origin="0 0">ซอย 21</text>')
# buildings (x0,x1,y0,y1,h,kind)
B=[(0.6,2.4,0.6,2.6,1.6,'w'),(2.8,4.6,0.6,2.2,2.4,'w'),(0.6,2.2,3.2,5.4,1.1,'w'),(7.0,9.4,0.5,2.6,1.5,'w'),
   (6.6,9.2,3.3,5.6,2.3,'t'),(0.8,3.0,8.0,9.6,1.0,'w'),(3.6,5.4,8.0,9.6,1.9,'w'),(6.4,9.2,8.1,9.5,1.2,'w')]
order=sorted(range(len(B)),key=lambda i:B[i][1]+B[i][3])
for n,i in enumerate(order):
    x0,x1,y0,y1,h,k=B[i]
    topc,lc,rc=('#ffffff','#e9ecf0','#d3d7de') if k=='w' else ('#ffffff','#e3202a','#b3161e')
    g=[poly([P(x1,y0),P(x1,y1),P(x1,y1,h),P(x1,y0,h)],rc), poly([P(x0,y1),P(x1,y1),P(x1,y1,h),P(x0,y1,h)],lc), poly([P(x0,y0,h),P(x1,y0,h),P(x1,y1,h),P(x0,y1,h)],topc)]
    # window strips
    for zz in [h*0.35,h*0.7]:
        if k=='w': g.append(f'<polyline points="{" ".join(f"{a},{b}" for a,b in [P(x0+0.2,y1,zz),P(x1-0.2,y1,zz)])}" stroke="#c4cad3" stroke-width="5" fill="none"/>')
        else: g.append(f'<polyline points="{" ".join(f"{a},{b}" for a,b in [P(x0+0.2,y1,zz),P(x1-0.2,y1,zz)])}" stroke="#ffffff" stroke-width="6" fill="none" opacity=".85"/>')
    if k=='t': g.append(poly([P(x0+0.25,y0+0.25,h+0.02),P(x1-0.25,y0+0.25,h+0.02),P(x1-0.25,y1-0.25,h+0.02),P(x0+0.25,y1-0.25,h+0.02)],'#5bb947'))
    out.append(f'<g id="im-b{i}">'+''.join(g)+'</g>')
    js.append(f'tl.fromTo("#im-b{i}", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.32, ease: "back.out(1.7)" }}, {9.86+n*0.035:.3f});')
# trees
trees=[(3.6,4.0),(4.4,3.2),(3.2,5.0),(8.0,7.95),(2.0,7.95),(9.6,3.0),(1.6,2.9)]
for j,(x,y) in enumerate(trees):
    a,b=P(x,y); out.append(f'<g id="im-t{j}"><ellipse cx="{a}" cy="{b+4}" rx="16" ry="8" fill="rgba(0,0,0,.12)"/><rect x="{a-3}" y="{b-22}" width="6" height="22" fill="#8a6a4a"/><circle cx="{a}" cy="{b-34}" r="20" fill="#5bb947"/><circle cx="{a-6}" cy="{b-40}" r="9" fill="#7ccc6a"/></g>')
    js.append(f'tl.fromTo("#im-t{j}", {{ scale: 0, transformOrigin: "50% 100%" }}, {{ scale: 1, duration: 0.3, ease: "back.out(2.5)" }}, {10.0+j*0.03:.3f});')
# pin on target roof
tx,ty=P(7.9,4.45,2.3)
out.append(f'<ellipse id="im-pulse" cx="{tx}" cy="{ty}" rx="70" ry="35" fill="none" stroke="#e3202a" stroke-width="6"/>')
out.append(f'<ellipse id="im-pinshadow" cx="{tx}" cy="{ty}" rx="22" ry="11" fill="rgba(0,0,0,.3)"/>')
out.append(f'<g id="im-pin"><path transform="translate({tx-36},{ty-112}) scale(3)" fill="#e3202a" stroke="#fff" stroke-width="1.4" d="M12 1.5C6.8 1.5 2.8 5.5 2.8 10.6c0 6.6 9.2 17.4 9.2 17.4s9.2-10.8 9.2-17.4c0-5.1-4-9.1-9.2-9.1z"/><circle cx="{tx}" cy="{ty-80}" r="11" fill="#fff"/></g>')
svg='<svg id="im-svg" width="900" height="620" viewBox="0 0 900 620" overflow="visible">'+''.join(out)+'</svg>'
js=['tl.fromTo("#fr-map", { opacity: 0 }, { opacity: 1, duration: 0.05 }, 9.68);',
    'tl.fromTo("#im-svg", { scale: 0.3, rotation: -12, y: 80, transformOrigin: "50% 60%" }, { scale: 1, rotation: 0, y: 0, duration: 0.45, ease: "back.out(1.5)" }, 9.68);',
    'tl.fromTo("#im-svg", { y: 0 }, { y: -14, duration: 1.0, ease: "sine.inOut", immediateRender: false }, 10.13);',
    'tl.fromTo("#im-road1", { opacity: 0, scaleX: 0, transformOrigin: "0% 50%" }, { opacity: 1, scaleX: 1, duration: 0.3, ease: "power3.out" }, 9.78);',
    'tl.fromTo("#im-road2", { opacity: 0, scaleY: 0, transformOrigin: "50% 100%" }, { opacity: 1, scaleY: 1, duration: 0.25, ease: "power3.out" }, 9.9);',
    'tl.fromTo(["#im-lbl1","#im-lbl2"], { opacity: 0 }, { opacity: 1, duration: 0.2 }, 10.0);',
    'tl.fromTo("#im-pin", { y: -320, opacity: 0 }, { y: 0, opacity: 1, duration: 0.42, ease: "bounce.out" }, 10.2);',
    'tl.fromTo("#im-pinshadow", { scale: 0.2, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.3, ease: "power2.out" }, 10.2);',
    'tl.fromTo("#im-pulse", { scale: 0.3, opacity: 1, transformOrigin: "50% 50%" }, { scale: 2.2, opacity: 0, duration: 0.6, ease: "expo.out" }, 10.36);',
    'tl.fromTo("#fr-map-label", { y: 40, opacity: 0, scale: 0.8 }, { y: 0, opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 10.24);',
    'tl.to("#fr-map", { scale: 0.7, opacity: 0, duration: 0.18, ease: "power3.in" }, 10.9);']+js
open('tools/isomap.svg.html','w').write(svg); open('tools/isomap.js','w').write('\n    '.join(js))
print(len(svg))
