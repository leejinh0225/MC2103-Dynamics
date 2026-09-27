"""Verify Lecture 6 sources, template invariants, and independent arithmetic."""
from pathlib import Path
from html.parser import HTMLParser
from math import sqrt, sin, cos, acos, radians, degrees, isclose
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
html = (SITE/'lecture06.html').read_text(encoding='utf-8')

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
        self.sections = []
        self.ids = []
        self.refs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'section' and 'source-section' in a.get('class','').split():
            self.sections.append(a['id'])
        if tag == 'img':
            assert a.get('alt')
            assert (a['width'],a['height']) == ('1920','1080')
            self.slides.append(a['src'])
        if tag == 'a':
            self.refs.append(a.get('href',''))

page = Parser()
page.feed(html)
assert len(page.ids) == len(set(page.ids))
assert page.sections == [f'slide-{n:02d}' for n in range(1,112)]
assert len(page.slides) == 111
for n,src in enumerate(page.slides,1):
    assert src == f'assets/slides/lecture06/slide-{n:02d}.jpg'
    with Image.open(SITE/src) as im:
        assert im.size == (1920,1080)
for href in page.refs:
    if href.startswith('#'):
        assert href[1:] in page.ids
    elif not href.startswith('https://'):
        assert (SITE/href).exists()
assert not re.search(r'\{\{|학습 목표|자가\s*점검|에델|마스터|private-materials',html)
assert html.count('class="exam-card"') == 14
hero = re.search(r'<section class="hero">([\s\S]*?)</section>',html).group(1)
assert hero.count('button button--primary') == 3
assert 'TyDEbI-RBGE' not in hero and 'EQmTc_5-4hQ' not in hero
assert html.index('id="overview"') < html.index('id="concept-map"') < html.index('id="concept-summary"') < html.index('id="slide-01"') < html.index('id="slide-111"') < html.index('id="exam-english"') < html.index('id="glossary"') < html.index('id="asr-log"') < html.index('id="sources"')

expected = {'overview':('TyDEbI-RBGE',9,'0:59'), 'contents1':('0gohr-4TtS0',263,'37:24'), 'contents2':('K3mFnZandvc',186,'25:37'), 'problem_solving':('-flNXvW8oTU',262,'34:13'), 'summary':('EQmTc_5-4hQ',13,'1:26')}
segment_count = 0
for name,(vid,count,last) in expected.items():
    raw = (ROOT/f'transcripts/lecture06/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {vid}' in raw and 'Language: en' in raw
    assert not re.search('[가-힣]',raw)
    stamps = re.findall(r'^\[(\d+:\d{2})\]',raw,re.M)
    assert len(stamps) == count and stamps[-1] == last
    seconds = [60*int(t.split(':')[0])+int(t.split(':')[1]) for t in stamps]
    assert seconds == sorted(seconds)
    segment_count += count

g = 9.81
net1 = (300*g - .25*200*g)*2
v1 = sqrt(2*net1/500)
assert net1 == 4905 and isclose(v1,4.4294469,abs_tol=1e-6)
spring_work = .5*20000*(.12**2-.16**2)
mu_k = (187.5+spring_work)/(60*g*.64)
back_energy = -spring_work-mu_k*60*g*.64
back_speed = sqrt(2*back_energy/60)
assert isclose(spring_work,-112) and isclose(back_energy,36.5)
assert isclose(back_speed,1.10302614,abs_tol=1e-7)
v2_squared = 2*g*12
normal2 = 1000*g+1000*v2_squared/6
crest_radius = 2*g*7.5/g
assert isclose(normal2,49050) and isclose(crest_radius,15)
d = (.5*(2**2-1**2)/g+.25*7)/(sin(radians(30))-.25*cos(radians(30)))
assert isclose(d,6.712338019,abs_tol=1e-8)
collar_potential2 = .5*200*(sqrt(.2**2+.15**2)-.1)**2+10*g*(-.15)
collar_speed = sqrt(2*(1-collar_potential2)/10)
assert isclose(collar_potential2,-12.465) and isclose(collar_speed,1.6410363,abs_tol=1e-6)
R,r0,v0,rmin = 6.37e6,6.87e6,10250,6.57e6
mu = g*R**2
ra = r0/(2*mu/(r0*v0**2)-1)
vmax = sqrt(v0**2+2*mu*(1/rmin-1/r0))
angle = degrees(acos(rmin*vmax/(r0*v0)))
assert isclose(ra-R,60332503.7348,abs_tol=.01)
assert isclose(angle,11.44405636,abs_tol=1e-7)
print(f'LECTURE06_VERIFIED slides=111 dimensions=1920x1080 transcripts=5 segments={segment_count} exam_cards=14')
print(f'NUMERICS v_blocks={v1:.6f} mu_k={mu_k:.6f} rebound={back_speed:.6f} N2={normal2} rho3={crest_radius} d={d:.6f} collar={collar_speed:.6f} altitude_km={(ra-R)/1000:.6f} angle={angle:.6f}')
