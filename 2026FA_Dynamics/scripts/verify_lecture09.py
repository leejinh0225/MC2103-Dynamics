"""Check English source coverage and independently cross-check Lecture 9 worked results."""
from math import cos, sin, isclose
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
html = (root / 'site/lecture09.html').read_text(encoding='utf-8')
expected = {
    'overview': ('7eQKoc8KhL4', 20, '1:06'),
    'contents1': ('c18PFwr6QPA', 354, '18:20'),
    'contents2': ('JChKRZ1SMhk', 182, '9:25'),
    'problem_solving': ('FpJjwilEOMM', 363, '18:09'),
    'summary': ('f_lQxmcZCdc', 24, '1:09')
}
for name, (vid, count, last) in expected.items():
    raw = (root / f'transcripts/lecture09/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {vid}\nLanguage: en\nCaptions: auto-generated' in raw and not re.search('[가-힣]', raw)
    cues = re.findall(r'^\[(\d+:\d\d)\]', raw, re.M)
    assert len(cues) == count and cues[-1] == last, name
    seconds = [60*int(t.split(':')[0])+int(t.split(':')[1]) for t in cues]
    assert seconds == sorted(seconds) and vid in html

sections = dict(re.findall(r'<section class="source-section" id="slide-(\d+)"[^>]*>([\s\S]*?)</section>', html))
assert list(sections) == [f'{n:02d}' for n in range(1, 45)]
for num in [6, 15, 21, 30, 31, 35, 36, 39, 40, 42]:
    s = sections[f'{num:02d}']
    assert s.index('</figure>') < s.index('원본 교정 · 적용 조건') < s.index('핵심 해설')
for key in ['<sup>N</sup>v<sup>P</sup>=Lθ̇ a₁', '<sup>A</sup>v<sup>P</sup>=0',
            '<sup>N</sup>a<sup>B</sup>=(r̈−rθ̇²)a₁+(2ṙθ̇+rθ̈)a₂', 'RᵧRₓ j=Rᵧ k=i', 'RₓRᵧ j=Rₓ j=k']:
    assert key in html, key
assert not re.search(r'\{\{|[NABC]\|[vaω]\||D_[NABC]|학습 목표|자가\s*점검|private-materials|마스터|에델', html)
hero = re.search(r'<section class="hero">([\s\S]*?)</section>', html)[1]
assert re.findall(r'button button--primary" href="https://www.youtube.com/watch\?v=([^"]+)', hero) == [
    expected[k][0] for k in ['contents1', 'contents2', 'problem_solving']]


def verify_motion(position, u, exact_velocity, exact_acceleration):
    h = 0.0004
    p0, pp, pm = position(u), position(u+h), position(u-h)
    for i in range(2):
        assert isclose((pp[i]-pm[i])/(2*h), exact_velocity[i], abs_tol=3e-6)
        assert isclose((pp[i]-2*p0[i]+pm[i])/h**2, exact_acceleration[i], abs_tol=5e-6)


for t in [-0.6, 0.0, 0.7, 1.4]:
    # Compare actual changes of the Cartesian position to expressions in the rotating basis.
    angle = lambda t: 0.4 + t - 0.3*t*t
    th, w, alpha = angle(t), 1-0.6*t, -0.6
    c, s = cos(th), sin(th)
    radial_transverse = lambda x, y: (x*c-y*s, x*s+y*c)
    L = 1.7
    verify_motion(lambda u: (L*sin(angle(u)), -L*cos(angle(u))), t,
                  radial_transverse(L*w, 0), radial_transverse(L*alpha, L*w*w))
    for radius, dr, ddr in [(lambda u: 2.1, 0, 0), (lambda u: 2+0.8*u+0.4*u*u, 0.8+0.8*t, 0.8)]:
        r = radius(t)
        verify_motion(lambda u: (radius(u)*cos(angle(u)), radius(u)*sin(angle(u))), t,
                      radial_transverse(dr, r*w), radial_transverse(ddr-r*w*w, 2*dr*w+r*alpha))
        verify_motion(lambda u: (radius(u), 0), t, (dr, 0), (ddr, 0))


def rx(v):
    x,y,z = v
    return (x,-z,y)


def ry(v):
    x,y,z = v
    return (z,y,-x)


j = (0,1,0)
assert ry(rx(j)) == (1,0,0) and rx(ry(j)) == (0,0,1)
print('LECTURE09_VERIFIED slides=44 captions=5 cues=943; pendulum, slider and finite-rotation checks passed')
