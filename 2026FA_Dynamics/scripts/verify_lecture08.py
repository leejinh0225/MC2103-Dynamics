"""Verify Lecture 8 coverage, fixed layout, original English captions, and mechanics."""
from pathlib import Path
from html.parser import HTMLParser
from math import sqrt, sin, cos, radians, isclose
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT/'site'
html = (SITE/'lecture08.html').read_text(encoding='utf-8')


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.sections, self.slides, self.refs = [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'section' and 'source-section' in a.get('class','').split():
            self.sections.append(a['id'])
        if tag == 'img':
            assert a.get('alt') and (a['width'],a['height']) == ('1920','1080')
            self.slides.append(a['src'])
        if tag == 'a':
            self.refs.append(a.get('href',''))


page = Parser()
page.feed(html)
assert len(page.ids) == len(set(page.ids))
assert page.sections == [f'slide-{n:02d}' for n in range(1,71)]
assert len(page.slides) == 70
for n,src in enumerate(page.slides,1):
    assert src == f'assets/slides/lecture08/slide-{n:02d}.jpg'
    with Image.open(SITE/src) as im:
        assert im.size == (1920,1080)
for href in page.refs:
    if href.startswith('#'):
        assert href[1:] in page.ids
    elif not href.startswith('https://'):
        assert (SITE/href).exists()
assert not re.search(r'\{\{|학습 목표|자가\s*점검|에델|마스터|private-materials|C:/Users',html)
assert html.count('class="exam-card"') == 11
hero = re.search(r'<section class="hero">([\s\S]*?)</section>',html).group(1)
assert hero.count('button button--primary') == 3
assert 'E4n4KXxWxLc' not in hero and '4jGpna7ysWQ' not in hero
for vid in ['g07zOf2lvBo','w52fBxRGP6s','gXdeWNdR2CE']:
    assert vid in hero
order = ['overview','concept-map','concept-summary','slide-01','slide-70','course-roadmap','exam-english','glossary','asr-log','sources']
positions = [html.index(f'id="{id}"') for id in order]
assert positions == sorted(positions)
assert 'Week 07' in hero and '2026-10-14' in hero
assert 'Week 08' in html and '날짜 미기재' in html

expected = {
    'overview':('E4n4KXxWxLc',19,'0:55'),
    'contents1':('g07zOf2lvBo',175,'9:19'),
    'contents2':('w52fBxRGP6s',427,'22:49'),
    'problem_solving':('gXdeWNdR2CE',570,'26:58'),
    'summary':('4jGpna7ysWQ',20,'1:01'),
}
segments = 0
for name,(vid,count,last) in expected.items():
    raw = (ROOT/f'transcripts/lecture08/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {vid}' in raw and 'Language: en' in raw and 'Captions: auto-generated' in raw
    assert not re.search('[가-힣]',raw)
    stamps = re.findall(r'^\[(\d+:\d{2})\]',raw,re.M)
    assert len(stamps) == count and stamps[-1] == last
    seconds = [60*int(t.split(':')[0])+int(t.split(':')[1]) for t in stamps]
    assert seconds == sorted(seconds)
    segments += count
assert segments == 1211

checks = 0
def check(actual,expected,tol=1e-8):
    global checks
    assert isclose(actual,expected,rel_tol=1e-10,abs_tol=tol),(actual,expected)
    checks += 1

# Example 1: solve momentum with upward-positive signed components.
s45,c45,s30,c30 = sin(radians(45)),cos(radians(45)),sin(radians(30)),cos(radians(30))
vb = 300/(7.5*s30*c45/s45 + 7.5*c30)
va = 7.5*s30*vb/(2.5*s45)
check(2.5*va*c45+7.5*vb*c30,300)
check(2.5*va*s45-7.5*vb*s30,0)
check(va,62.11657082460497)
check(vb,29.282032302755084)
t1 = .5*10*30**2
t2 = .5*2.5*va**2+.5*7.5*vb**2
check(t2,8038.475772933678)
assert t2>t1
assert f'{va:.3f}' in html and '62.2' in html

# Example 2: independent two-by-two solution, including B's negative y component.
a,b,c,d = sin(radians(7.4)),sin(radians(49.3)),cos(radians(7.4)),-cos(radians(49.3))
rx,ry = 4*c30-2*c45,4*s30-2*s45
det = a*d-b*c
pa,pb = (rx*d-b*ry)/det,(a*ry-rx*c)/det
check(pa,2.130674628621777)
check(pb,2.3418891060432876)
check(a*pa+b*pb+2*c45,4*c30)
check(c*pa+d*pb+2*s45,4*s30)
ratio = (pa**2+pb**2+4)/16
check(ratio,.8765136848785484)
check(sqrt((4*c30/3)**2+(4*s30/3)**2),4/3)
assert f'{pa:.3f}' in html and f'{pb:.3f}' in html

# Example 3: varied positive masses, lengths, and lower/equal initial speeds.
g = 9.81
for ma in [.01,.4,1,3,100]:
    for mb in [.03,.7,2,40]:
        for length in [.2,1,2.4]:
            for scale in [.1,.5,1]:
                v0 = scale*sqrt(2*g*length)
                vel = mb*v0/(ma+mb)
                height = ma/(ma+mb)*v0**2/(2*g)
                check(mb*v0,(ma+mb)*vel)
                check(.5*mb*v0**2,.5*(ma+mb)*vel**2+mb*g*height)
                assert 0<height<length
                if scale==1:
                    check(height,ma*length/(ma+mb))
check(.5*(sqrt(2*g))**2/(2*g),.5)

# Example 4: both polynomial roots; only one satisfies stated velocity directions.
roots = [(78+sqrt(78**2-4*20*72))/40,(78-sqrt(78**2-4*20*72))/40]
check(roots[0],2.4)
check(roots[1],1.5)
for cv in roots:
    av,byv,bxv = 3*cv-6,3*cv-6,3-cv
    check(bxv+cv,3)
    check(av-byv,0)
    check(2.4*av-2.1*byv-.9*cv,-.6*3)
    check(av**2+bxv**2+byv**2+cv**2,9)
assert 3*roots[0]-6>0 and 3*roots[1]-6<0
check(sqrt(.6**2+1.2**2),1.3416407864998738)

# Non-planar vector identities: translating centroidal frame, H and T splits.
def add(x,y): return tuple(a+b for a,b in zip(x,y))
def sub(x,y): return tuple(a-b for a,b in zip(x,y))
def mul(k,x): return tuple(k*a for a in x)
def dot(x,y): return sum(a*b for a,b in zip(x,y))
def cross(x,y):
    return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def total(xs):
    answer = (0,0,0)
    for x in xs: answer = add(answer,x)
    return answer
for k in range(1,31):
    masses = [1+k/3,2,3+k/7]
    rs = [(k,.2,3),(-2,k/4,1),(1,-2,-k/5)]
    vs = [(k/7,-1,2),(.3,k/3,0),(-1,2,k/9)]
    mass = sum(masses)
    rg = mul(1/mass,total(mul(m,r) for m,r in zip(masses,rs)))
    vg = mul(1/mass,total(mul(m,v) for m,v in zip(masses,vs)))
    rp,vp = [sub(r,rg) for r in rs],[sub(v,vg) for v in vs]
    hg = total(cross(r,mul(m,v)) for r,m,v in zip(rp,masses,vs))
    hgp = total(cross(r,mul(m,v)) for r,m,v in zip(rp,masses,vp))
    ho = total(cross(r,mul(m,v)) for r,m,v in zip(rs,masses,vs))
    split = add(cross(rg,mul(mass,vg)),hg)
    for x,y,z,w in zip(hg,hgp,ho,split):
        check(x,y); check(z,w)
    check(sum(.5*m*dot(v,v) for m,v in zip(masses,vs)),
          .5*mass*dot(vg,vg)+sum(.5*m*dot(v,v) for m,v in zip(masses,vp)))

# Content regression boundaries: adjacent corrections and condition distinctions.
for n in [8,12,22,23,27,36,44,45,49,50,53,62,65,66]:
    body = re.search(rf'<section class="source-section" id="slide-{n:02d}"[\s\S]*?</section>',html).group()
    assert '교정' in body,(n,'missing adjacent correction')
for required in ['v₀=√(2gℓ)','v₀²&lt;2gℓ','dHG/dt','1.341641','62.116571','20c²−78c+72','동시에 쿠션에 닿는다고 가정하는 것이 아닙니다']:
    assert required in html,required
print(f'LECTURE08_VERIFIED slides=70 dimensions=1920x1080 transcripts=5 segments={segments} exam_cards=11 math_checks={checks}')
print(f'NUMERICS explosion=({va:.6f},{vb:.6f}) pool=({pa:.6f},{pb:.6f}) pool_energy_ratio={ratio:.9f} elastic_B_speed={sqrt(1.8):.9f}')
