"""Check source coverage and verify worked answers by differentiating geometry."""
from math import sin, cos, sqrt, pi, atan2
from pathlib import Path
import re
from PIL import Image

root=Path(__file__).resolve().parents[1]
html=(root/'site/lecture11.html').read_text(encoding='utf-8')
expected={
    'overview':('rvTrFmn_-Cg',14,'0:45'),
    'contents1':('8EpMGFdmujw',155,'7:54'),
    'contents2':('bBfKAAQQCPA',180,'8:48'),
    'problem_solving':('p9g4KpMNfpg',643,'32:35'),
    'summary':('A2OQ13NEQF4',26,'1:16'),
}
for name,(vid,count,last) in expected.items():
    raw=(root/f'transcripts/lecture11/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {vid}\nLanguage: en\nCaptions: auto-generated' in raw
    assert not re.search('[가-힣]',raw)
    cues=re.findall(r'^\[(\d+:\d\d)\]',raw,re.M)
    assert len(cues)==count and cues[-1]==last,(name,len(cues),cues[-1])
    seconds=[60*int(t.split(':')[0])+int(t.split(':')[1]) for t in cues]
    assert seconds==sorted(seconds) and vid in html
sections=dict(re.findall(r'<section class="source-section" id="slide-(\d+)"[^>]*>([\s\S]*?)</section>',html))
assert list(sections)==[f'{n:02d}' for n in range(1,54)]
for n,body in sections.items():
    with Image.open(root/f'site/assets/slides/lecture11/slide-{n}.jpg') as im:
        assert im.size==(1920,1080)
    assert body.count('<figure class="source-slide">')==1
for n in [20,30,35,39,40,43,45,50,51]:
    s=sections[f'{n:02d}']
    assert s.index('</figure>')<s.index('원본 교정 · 적용 조건')<s.index('핵심 해설')
hero=re.search(r'<section class="hero">([\s\S]*?)</section>',html)[1]
assert re.findall(r'button button--primary" href="https://www.youtube.com/watch\?v=([^"]+)',hero)==[
    expected[k][0] for k in ['contents1','contents2','problem_solving']]
assert not re.search(r'\{\{|학습 목표|자가\s*점검|private-materials|마스터|에델',html)
assert html.count('class="exam-card"')==12
for n,required in {
    28:['0.15a₁ rad/s²'],30:['−3.810b₁+0.468b₂+1.800b₃','−3.533n₁−1.500n₂+1.800n₃'],
    40:['48/13≈3.69231','12/√13≈3.32820'],41:['=−12c₁ in/s'],
    49:['25r₁+25√3r₂+80r₃'],50:['−1600r₁+800r₃ in/s²'],
    51:['−1300r₁+300√3r₂+1800r₃','in/s²']
}.items():
    for text in required: assert text in sections[f'{n:02d}'],(n,text)

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def plus(*vectors): return [sum(v[i] for v in vectors) for i in range(3)]
def scale(s,v): return [s*x for x in v]
def trans(a): return list(map(list,zip(*a)))
def mm(a,b): return [[dot(row,col) for col in trans(b)] for row in a]
def mv(a,v): return [dot(row,v) for row in a]
def close(a,b,tol=1e-7): assert max(abs(x-y) for x,y in zip(a,b))<tol,(a,b,tol)
def deriv(f,t,h=1e-5): return [(p-m)/(2*h) for p,m in zip(f(t+h),f(t-h))]
def deriv2(f,t,h=1e-4): return [(p-2*c+m)/(h*h) for p,c,m in zip(f(t+h),f(t),f(t-h))]
def rx(x): return [[1,0,0],[0,cos(x),-sin(x)],[0,sin(x),cos(x)]]
def ry(x): return [[cos(x),0,sin(x)],[0,1,0],[-sin(x),0,cos(x)]]
def rz(x): return [[cos(x),-sin(x),0],[sin(x),cos(x),0],[0,0,1]]
def angular_from_matrix(f,t):
    # Spatial skew matrix Rdot R^T, independently obtained from orientation.
    rp,rm=f(t+1e-5),f(t-1e-5)
    rd=[[(a-b)/2e-5 for a,b in zip(x,y)] for x,y in zip(rp,rm)]
    s=mm(rd,trans(f(t)))
    return [s[2][1],s[0][2],s[1][0]]

# Crane: differentiate the point's Cartesian position, including nonaligned frames.
for theta0,phi0 in [(0,pi/6),(.7,.3),(-.4,.9)]:
    def orient(t): return mm(ry(theta0+.3*t),rz(phi0+.5*t))
    def position(t):
        th,ph=theta0+.3*t,phi0+.5*t
        return [12*cos(ph)*cos(th),12*sin(ph),-12*cos(ph)*sin(th)]
    def omega(t): return mv(ry(theta0+.3*t),[0,.3,.5])
    R=orient(0)
    alpha=mv(ry(theta0),[.15,0,0])
    close(angular_from_matrix(orient,0),omega(0))
    close(deriv(omega,0),alpha)
    r=position(0)
    vv=cross(omega(0),r)
    aa=plus(cross(alpha,r),cross(omega(0),cross(omega(0),r)))
    close(deriv(position,0),vv)
    close(deriv2(position,0),aa,1e-6)
    s,c=sin(phi0),cos(phi0)
    close(mv(trans(R),vv),[0,6,-3.6*c])
    close(mv(trans(R),aa),[-12*(.25+.09*c*c),12*.09*s*c,3.6*s])
    if theta0==0:
        close(aa,[-3.5333836474405094,-1.5,1.8])
        close(mv(trans(R),aa),[-3.81,.4676537180435969,1.8])

# Disk/rod: derive B's translation and the rod attitude from the fixed-length geometry.
def disk_a(t): return [0,-2*sin(12*t),2*cos(12*t)]
def slider_b(t):
    a=disk_a(t)
    return [sqrt(49-(3-a[1])**2-a[2]**2),3,0]
def angles(t):
    a,b=disk_a(t),slider_b(t)
    return [atan2(3-a[1],a[2]),atan2(-b[0],sqrt((3-a[1])**2+a[2]**2))]
def rod_orientation(t):
    ph,ps=angles(t)
    return mm(rx(ph),ry(ps))
close(deriv(disk_a,0),[0,-24,0],1e-6)
close(deriv(slider_b,0),[-12,0,0],1e-6)
close(deriv(angles,0),[48/13,12/sqrt(13)],1e-6)
omega_rod=angular_from_matrix(rod_orientation,0)
close(omega_rod,[48/13,24/13,36/13],1e-6)
AB=plus(slider_b(0),scale(-1,disk_a(0)))
close(plus([0,-24,0],cross(omega_rod,AB)),[-12,0,0],2e-6)
for t in [-.02,0,.03]:
    AB=plus(slider_b(t),scale(-1,disk_a(t)))
    assert abs(dot(AB,AB)-49)<1e-12
    close(mv(rod_orientation(t),[0,0,-7]),AB)

# Moving collar: vary both s and rotation, and compare full Cartesian derivatives.
e=[.5,sqrt(3)/2,0]
for theta0,t in [(0,0),(.6,.01),(-.4,-.008)]:
    def theta(q): return theta0-20*q-100*q*q
    def distance(q): return 8+50*q+300*q*q
    def position(q): return mv(ry(theta(q)),scale(distance(q),e))
    R=ry(theta(t))
    r=scale(distance(t),e)
    w=[0,-20-200*t,0]
    a=[0,-200,0]
    relative_v=scale(50+600*t,e)
    relative_a=scale(600,e)
    fixed_a=plus(cross(a,r),cross(w,cross(w,r)))
    coriolis=scale(2,cross(w,relative_v))
    vv=plus(cross(w,r),relative_v)
    aa=plus(fixed_a,relative_a,coriolis)
    close(mv(trans(R),deriv(position,t,1e-6)),vv,1e-6)
    close(mv(trans(R),deriv2(position,t,1e-5)),aa,.001)
    if t==0:
        close(vv,[25,25*sqrt(3),80])
        close(fixed_a,[-1600,0,800])
        close(coriolis,[0,0,1000])
        close(aa,[-1300,300*sqrt(3),1800])
print('LECTURE11_VERIFIED: 53 slides; 1018 English cues; 3 worked examples cross-checked by Cartesian and orientation differentiation; correction placement and hero links.')
