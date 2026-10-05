"""Validate Lecture 7 source coverage, fixed layout, raw captions, and arithmetic."""
from pathlib import Path
from html.parser import HTMLParser
from math import sqrt, sin, cos, radians, atan2, degrees, isclose
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT/'site'
html = (SITE/'lecture07.html').read_text(encoding='utf-8')

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
            assert a.get('alt') and (a['width'],a['height'])==('1920','1080')
            self.slides.append(a['src'])
        if tag == 'a':
            self.refs.append(a.get('href',''))

page = Parser()
page.feed(html)
assert len(page.ids)==len(set(page.ids))
assert page.sections==[f'slide-{n:02d}' for n in range(1,75)]
assert len(page.slides)==74
for n,src in enumerate(page.slides,1):
    assert src==f'assets/slides/lecture07/slide-{n:02d}.jpg'
    with Image.open(SITE/src) as im:
        assert im.size==(1920,1080)
for href in page.refs:
    if href.startswith('#'):
        assert href[1:] in page.ids
    elif not href.startswith('https://'):
        assert (SITE/href).exists()
assert not re.search(r'\{\{|학습 목표|자가\s*점검|에델|마스터|private-materials',html)
assert html.count('class="exam-card"')==9
hero = re.search(r'<section class="hero">([\s\S]*?)</section>',html).group(1)
assert hero.count('button button--primary')==3
assert 'N5RhmnCqtZg' not in hero and '-2JYBx5dGEo' not in hero
order = ['overview','concept-map','concept-summary','slide-01','slide-74','course-roadmap','exam-english','glossary','asr-log','sources']
positions = [html.index(f'id="{id}"') for id in order]
assert positions==sorted(positions)

expected = {
    'overview':('N5RhmnCqtZg',17,'0:55'),
    'contents1':('VY_wTpAjoI8',93,'5:15'),
    'contents2':('jvt8mX2OSfs',248,'14:38'),
    'problem_solving':('PdgyxxL0DeA',672,'34:39'),
    'summary':('-2JYBx5dGEo',27,'1:13'),
}
segments = 0
for name,(vid,count,last) in expected.items():
    raw = (ROOT/f'transcripts/lecture07/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {vid}' in raw and 'Language: en' in raw and 'Captions: auto-generated' in raw
    assert not re.search('[가-힣]',raw)
    stamps = re.findall(r'^\[(\d+:\d{2})\]',raw,re.M)
    assert len(stamps)==count and stamps[-1]==last
    seconds = [60*int(t.split(':')[0])+int(t.split(':')[1]) for t in stamps]
    assert seconds==sorted(seconds)
    segments += count

g = 9.81
def check(actual,expected,tol=1e-5):
    assert isclose(actual,expected,rel_tol=0,abs_tol=tol),(actual,expected)
t = (100/3.6)/(7000/1800-g*sin(radians(5)))
check(t,9.155825736)
fx = .12*(36*cos(radians(40))+24)/.015
fy = .12*36*sin(radians(40))/.015
check(fx,412.620799618)
check(fy,185.122831590)
check(sqrt(fx*fx+fy*fy),452.245936470)
check(degrees(atan2(fy,fx)),24.16344753)
for mc,answer in [(24,(.764140062,-18.339361492,23.692449851,9.926470588,.779411765)),(25,(.742307489,-18.557687224,23.861847269,9.642857143,.785714286))]:
    speed = 10*3*cos(radians(30))/(10+mc)
    jx = 10*(speed-3*cos(radians(30)))
    t2 = .5*(10+mc)*speed**2
    actual = (speed,jx,sqrt(jx*jx+15**2),t2,1-t2/45)
    for a,e in zip(actual,answer): check(a,e)
a,b = -3*sqrt(3)/10,2*sqrt(3)/5
check(.5*a+b,sqrt(3)/4)
check(.5*b-a,sqrt(3)/2)
ax,ay = -a*.5+.5*cos(radians(30)),-a*cos(radians(30))-.25
check(ax,b)
check(ay,.2)
check(ax*ax+ay*ay+b*b,1)
v2 = sqrt(4*g)
v3 = 30*v2/40
x3 = 10*g/20000
t3 = .5*40*v3*v3
h = (30*g+sqrt((30*g)**2+4*10000*t3))/(2*10000)
check(v3,4.698137929)
check(t3,441.45)
check(h,.225336773)
check(h+x3,.230241773)
check(t3+40*g*h,10000*((x3+h)**2-x3**2))
theta = radians(20)
u = sqrt((800*.1**2+2*2*g*1.6*(sin(theta)-.2*cos(theta)))/2)
j = 1.8*u/(1/2+cos(theta)**2)
a,b = u-j/2,j*cos(theta)
check(2*u*cos(theta),2*a*cos(theta)+b)
check(b*cos(theta)-a,.8*u)
v40sq = b*b-2*g*(1-cos(radians(40)))
check(u,2.972697460)
check(j,3.868958390)
check(b,3.635631649)
check(sqrt(v40sq),2.937279262)
check(g*cos(radians(40))+v40sq,16.142505452)
for required in ['24 kg','25 kg','77.94%','0.225337','16.142505','공식 답이 아닙니다']:
    assert required in html
print(f'LECTURE07_VERIFIED slides=74 dimensions=1920x1080 transcripts=5 segments={segments} exam_cards=9')
print(f'NUMERICS car_t={t:.6f} baseball_F={sqrt(fx*fx+fy*fy):.6f} pan_h={h:.6f} group_v={sqrt(v40sq):.6f} group_T={g*cos(radians(40))+v40sq:.6f}')
