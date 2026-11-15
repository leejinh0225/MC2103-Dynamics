"""Verify source coverage and cross-check rotation calculations geometrically."""
from math import cos, sin, radians, sqrt
from pathlib import Path
from PIL import Image
import re

root=Path(__file__).resolve().parents[1]
html=(root/'site/lecture10.html').read_text(encoding='utf-8')
expected={
    'overview':('8-cbq84asB4',17,'0:48'),
    'contents1':('XcUjJyywyfU',391,'19:22'),
    'contents2':('QnkRdVLMy8o',685,'34:22'),
    'problem_solving':('PsLITXfcJug',400,'19:44'),
    'summary':('GeIUzTOQs1c',27,'1:21'),
}
for name,(vid,count,last) in expected.items():
    raw=(root/f'transcripts/lecture10/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {vid}\nLanguage: en\nCaptions: auto-generated' in raw
    assert not re.search('[가-힣]',raw)
    cues=re.findall(r'^\[(\d+:\d\d)\]',raw,re.M)
    assert len(cues)==count and cues[-1]==last,(name,len(cues),cues[-1])
    secs=[60*int(t.split(':')[0])+int(t.split(':')[1]) for t in cues]
    assert secs==sorted(secs) and vid in html
sections=dict(re.findall(r'<section class="source-section" id="slide-(\d+)"[^>]*>([\s\S]*?)</section>',html))
assert list(sections)==[f'{n:02d}' for n in range(1,59)]
for n,body in sections.items():
    with Image.open(root/f'site/assets/slides/lecture10/slide-{n}.jpg') as im:
        assert im.size==(1920,1080)
    assert body.count('<figure class="source-slide">')==1
for n in [10,17,25,51,53]:
    s=sections[f'{n:02d}']
    assert s.index('</figure>')<s.index('원본 교정 · 적용 조건')<s.index('핵심 해설')
hero=re.search(r'<section class="hero">([\s\S]*?)</section>',html)[1]
assert re.findall(r'button button--primary" href="https://www.youtube.com/watch\?v=([^"]+)',hero)==[
    expected[k][0] for k in ['contents1','contents2','problem_solving']]
assert not re.search(r'\{\{|학습 목표|자가\s*점검|private-materials|마스터|에델',html)

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def transpose(m): return list(map(list,zip(*m)))
def mul(a,b): return [[dot(row,col) for col in transpose(b)] for row in a]
def mv(m,v): return [dot(row,v) for row in m]
def close(a,b,tol=1e-12): assert max(abs(x-y) for x,y in zip(a,b))<tol,(a,b)
def matclose(a,b,tol=1e-12):
    for x,y in zip(a,b): close(x,y,tol)
I=[[1,0,0],[0,1,0],[0,0,1]]
def rotate(v,axis,angle):
    # Geometric Rodrigues formula; rotate the current axes themselves for intrinsic sequences.
    c,s=cos(angle),sin(angle)
    return [c*x+s*y+(1-c)*dot(axis,v)*z for x,y,z in zip(v,cross(axis,v),axis)]
def sequence(order,angles,body):
    axes=[row[:] for row in I]
    for k,t in zip(order,angles):
        axis=axes[k][:] if body else I[k]
        axes=[rotate(v,axis,t) for v in axes]
    return transpose(axes)
def expanded_xyz(t,f,p):
    ct,st,cf,sf,cp,sp=cos(t),sin(t),cos(f),sin(f),cos(p),sin(p)
    return [[cf*cp,-cf*sp,sf],[ct*sp+st*sf*cp,ct*cp-st*sf*sp,-st*cf],
            [st*sp-ct*sf*cp,st*cp+ct*sf*sp,ct*cf]]
def expanded_zyx(t,f,p):
    ct,st,cf,sf,cp,sp=cos(t),sin(t),cos(f),sin(f),cos(p),sin(p)
    return [[cf*cp,-ct*sp+st*sf*cp,st*sp+ct*sf*cp],
            [cf*sp,ct*cp+st*sf*sp,-st*cp+ct*sf*sp],[-sf,st*cf,ct*cf]]
for deg in [(12,37,81),(-48,26,11),(0,90,23),(90,0,-90),(30,30,30)]:
    t,f,p=map(radians,deg)
    rb=sequence([0,1,2],[t,f,p],True)
    rs=sequence([0,1,2],[t,f,p],False)
    matclose(rb,expanded_xyz(t,f,p))
    matclose(rs,expanded_zyx(t,f,p))
    matclose(rb,sequence([2,1,0],[p,f,t],False))
    for R in [rb,rs]:
        matclose(mul(transpose(R),R),I)
        assert abs(dot(R[0],cross(R[1],R[2]))-1)<1e-12
        v=[.4,-1.8,2.3]
        close(mv(transpose(R),mv(R,v)),v)
        assert abs(dot(mv(R,v),mv(R,v))-dot(v,v))<1e-12
angle=radians(30)
body=sequence([2,1,0],[angle]*3,True)
space=sequence([2,1,0],[angle]*3,False)
matclose(body,[[.750,-.217,.625],[.433,.875,-.217],[-.500,.433,.750]],.00051)
matclose(space,[[.750,-.433,.500],[.650,.625,-.433],[-.125,.650,.750]],.00051)
A=[[.866,.500,0],[-.500,.866,0],[0,0,1]] # basis vectors as rows
B=[[.750,.433,-.500],[-.217,.875,.433],[.625,-.217,.750]]
C=[[dot(a,b) for b in B] for a in A]
printed=[[.866,.250,.433],[0,.866,-.500],[-.500,.433,.750]]
matclose(C,printed,.00051)
matclose(C,[[.866,.249578,.432750],[-.000022,.866250,-.500422],[-.500,.433,.750]])
qa=[.683,.366,1.183]
qb=mv(transpose(printed),qa)
close(qb,[-.000022,.999945,.999989])
close(mv(printed,[0,1,1]),qa)
q=rotate([0,1,1],[1,0,0],radians(45))
close(q,[0,0,sqrt(2)])
close(rotate(q,[1,0,0],radians(-45)),[0,1,1])
assert abs(dot(q,q)-2)<1e-12
print('LECTURE10_VERIFIED: 58 slides; 1520 English cues; 5 independent Rodrigues cases; 4 examples; active/passive basis conditions.')
