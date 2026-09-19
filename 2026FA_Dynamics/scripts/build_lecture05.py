"""Fill the fixed Lecture 1 template with source-grounded Lecture 5 content."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
records = []

def p(text):
    return '<p>' + text + '</p>'

def card(title, *body, kind='card'):
    return f'<div class="{kind}"><h3>{title}</h3>' + ''.join(p(x) for x in body) + '</div>'

def formula(text):
    return '<span class="formula">' + text + '</span>'

def table(headers, rows):
    return '<table class="term-table"><thead><tr>' + ''.join('<th>'+x+'</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows) + '</tbody></table>'

def add(title, evidence, *body, eq='', extra='', correction='', role='Concept'):
    blocks = card('원본 교정 · 적용 조건', correction, kind='callout') if correction else ''
    blocks += card('핵심 해설' if role == 'Concept' else '슬라이드 안내', *body, kind='card' if role == 'Concept' else 'quiet-card')
    if eq:
        blocks += card('식과 기호', formula(eq))
    records.append((title, evidence, blocks + extra, role))

summary = ''.join([
    card('1. 중심을 향한 힘은 운동을 바꾸지만, 중심에 대한 각운동량은 바꾸지 않습니다.',
         'Central force(중심력)는 line of action(작용선)이 항상 같은 fixed point(고정점) O를 지나는 force(힘)입니다. Inward(안쪽) 또는 outward(바깥쪽) 모두 가능하며, gravitational force(중력)는 inward(안쪽) 중심력의 예입니다. 중심력이라고 해서 force magnitude(힘의 크기)가 constant(일정)하거나 orbit(궤도)이 circular(원형)이어야 하는 것은 아닙니다.',
         'Angular momentum(각운동량)은 <b>H</b><sub>O</sub> = <b>r</b> × m<b>v</b>로 정의합니다. <b>r</b>은 O에서 입자로 향하는 position vector(위치벡터), m은 mass(질량), <b>v</b>는 inertial velocity(관성계 속도)입니다. Fixed inertial origin(고정 관성계 원점)과 constant mass(일정 질량)에 대해 Σ<b>M</b><sub>O</sub> = d<b>H</b><sub>O</sub>/dt가 성립합니다. 중심력은 moment arm(모멘트팔)이 0이므로 Σ<b>M</b><sub>O</sub> = 0이고, 따라서 <b>H</b><sub>O</sub>가 conserved(보존)됩니다. Force(힘)가 0이라는 뜻은 아닙니다.',kind='callout'),
    card('2. 보존되는 것은 rv 전체가 아니라, r과 횡방향 속도의 곱입니다.',
         'φ를 <b>r</b>과 <b>v</b>의 included angle(끼인각)이라 하면 H<sub>O</sub> = mrv sinφ입니다. Planar motion(평면운동)의 진행 방향을 θ 증가 방향으로 잡으면 v<sub>θ</sub> = rθ̇, h = H<sub>O</sub>/m = rv<sub>θ</sub> = r²θ̇입니다. h는 specific angular momentum(단위 질량당 각운동량)이며 단위는 m²/s입니다. Altitude(고도)를 뜻하는 기호가 아닙니다.',
         '두 위치의 관계는 r<sub>A</sub>v<sub>A</sub>sinφ<sub>A</sub> = r<sub>B</sub>v<sub>B</sub>sinφ<sub>B</sub>입니다. Perigee(근지점)와 apogee(원지점)처럼 radial velocity(반지름 속도) ṙ = 0인 점에서만 v = v<sub>θ</sub>이므로 r<sub>A</sub>v<sub>A</sub> = r<sub>B</sub>v<sub>B</sub>로 줄어듭니다. 일반 위치에서는 v = √(ṙ² + v<sub>θ</sub>²)입니다. Nonzero angular momentum(0이 아닌 각운동량)의 방향이 고정되어 orbit plane(궤도 평면)도 고정됩니다.'),
    card('3. 면적속도 일정과 각속도 일정은 다릅니다.',
         'Radius vector(반지름벡터)가 미소 각도 dθ만큼 움직일 때 swept area(휩쓴 면적)는 dA = ½r²dθ입니다. 따라서 areal velocity(면적속도)는 dA/dt = ½r²θ̇ = h/2이며 constant(일정)합니다. Equal areas in equal times(같은 시간 동안 같은 면적)가 Kepler’s second law(케플러 제2법칙)입니다.',
         '가까운 곳에서는 θ̇ = h/r²가 커지고, 먼 곳에서는 작아집니다. 즉 같은 면적을 같은 시간에 휩쓸지만 같은 angle(각도)이나 같은 path length(경로 길이)를 이동하는 것은 아닙니다. 예를 들어 r이 두 배라면 v<sub>θ</sub>는 절반, θ̇는 ¼입니다. 이 비율 예는 보존식에서 계산한 시험용 보강입니다.'),
    card('4. 지표면 고도와 지구 중심까지의 거리를 먼저 구별합니다.',
         'Newton’s law of universal gravitation(뉴턴의 만유인력 법칙)은 force magnitude(힘의 크기) F = GMm/r²입니다. M은 central body mass(중심 천체 질량), m은 satellite mass(위성 질량), G는 gravitational constant(만유인력상수)입니다. r은 두 중심 사이의 거리이므로 altitude(고도)가 z이고 Earth radius(지구 반지름)가 R이면 r = R + z입니다.',
         '계산을 줄이기 위해 μ = GM인 gravitational parameter(중력 매개변수)를 사용합니다. Surface gravity(지표 중력가속도)를 g라고 하면 μ = gR²이고, 지표 밖의 gravitational acceleration(중력가속도)은 μ/r²입니다. 고도 전체에서 g = 9.81 m/s²라고 두면 안 됩니다. 이번 모델은 구형 지구, 고정된 지구 중심, 일정 질량, 중력만 작용하는 free flight(자유비행)를 사용하고 air drag(공기저항)와 다른 천체의 영향은 무시합니다. 이 모델의 한계 설명은 편집자 보강입니다.'),
    card('5. 시간 대신 각도를 변수로 바꾸면 궤도 모양이 나옵니다.',
         'Polar coordinates(극좌표)의 radial equation(반지름 운동방정식)은 m(r̈ − rθ̇²) = −F이고 transverse equation(횡방향 운동방정식)은 m(rθ̈ + 2ṙθ̇) = 0입니다. 두 번째 식이 h = r²θ̇ 일정과 같습니다. u = 1/r로 치환하고 prime(프라임)을 θ에 대한 미분으로 정의하면 ṙ = −hu′, r̈ = −h²u²u″입니다.',
         '첫 번째 식에 대입하면 u″ + u = F/(mh²u²)입니다. Inverse-square gravity(거리 제곱에 반비례하는 중력) F = μmu²에서는 우변이 μ/h²라는 상수가 됩니다. 따라서 u = μ/h² + A cosθ + B sinθ가 해입니다. 이 식은 외워야 하는 새 법칙이 아니라 Newton’s second law(뉴턴 제2법칙)에서 유도된 결과입니다. h ≠ 0인 궤도에 적용하며 pure radial motion(순수 반지름 운동)은 별도로 풉니다.'),
    card('6. 이심률은 궤도 형태를 분류합니다.',
         'θ = 0을 periapsis(근점; 지구 궤도에서는 근지점)에 두면 r = p/(1 + ε cosθ), p = h²/μ입니다. ε는 eccentricity(이심률)인 0 이상의 무차원 수이며, 지구 중심은 ellipse center(타원 중심)가 아니라 focus(초점)에 있습니다. ε = 0은 circle(원), 0 &lt; ε &lt; 1은 ellipse(타원), ε = 1은 parabola(포물선), ε &gt; 1은 hyperbola(쌍곡선)입니다.',
         'Ellipse(타원)는 bound orbit(묶인 궤도)이고, parabola(포물선)와 hyperbola(쌍곡선)는 이상적인 비충돌 모형에서 escape trajectory(탈출 궤적)입니다. Ellipse(타원)의 perigee radius(근지점 거리)는 r<sub>p</sub> = p/(1+ε), apogee radius(원지점 거리)는 r<sub>a</sub> = p/(1−ε)입니다. 원본 29장의 원 조건 ε &lt; 0은 ε = 0으로 교정합니다.'),
    card('7. 수평 발사 조건은 적분상수를 결정합니다.',
         'Parallel to the surface(지표면에 평행하게)라는 조건은 초기 radial velocity(반지름 속도)가 ṙ<sub>0</sub> = 0이라는 뜻입니다. 따라서 h = r<sub>0</sub>v<sub>0</sub>이고, 발사점을 θ = 0으로 잡은 u = μ/h² + C cosθ에서 C = 1/r<sub>0</sub> − μ/h²입니다. C의 단위는 m⁻¹이며 initial conditions(초기조건)로 정해집니다.',
         '시험용 보강: 발사점이 반드시 perigee(근지점)인 것은 아닙니다. v<sub>0</sub> &gt; v<sub>circ</sub>이면 C &gt; 0으로 근지점에서 시작하고, 0 &lt; v<sub>0</sub> &lt; v<sub>circ</sub>이면 C &lt; 0으로 apogee(원지점)에서 시작합니다. 후자에서도 물리적인 eccentricity(이심률)는 ε = |C|h²/μ ≥ 0입니다. 발사점 기준 signed coefficient(부호 있는 계수)와 근점 기준 eccentricity(이심률)를 혼동하지 않습니다.'),
    card('8. 원 궤도 속력과 탈출 속력은 서로 다른 경계입니다.',
         'Circular speed(원 궤도 속력)는 v<sub>circ</sub> = √(μ/r<sub>0</sub>)이고, escape speed(탈출 속력)는 v<sub>esc</sub> = √(2μ/r<sub>0</sub>) = √2 v<sub>circ</sub>입니다. 같은 위치에서 tangential launch(횡방향 발사)를 가정할 때 v<sub>0</sub> = v<sub>circ</sub>이면 원, v<sub>circ</sub> &lt; v<sub>0</sub> &lt; v<sub>esc</sub>이면 더 먼 원지점까지 가는 타원, v<sub>0</sub> = v<sub>esc</sub>이면 포물선, v<sub>0</sub> &gt; v<sub>esc</sub>이면 쌍곡선입니다.',
         '0 &lt; v<sub>0</sub> &lt; v<sub>circ</sub>도 수학적으로 타원이지만 발사점보다 안쪽으로 내려가며, 지구와 충돌하는 궤도일 수 있습니다. Escape(탈출)는 유한한 위치에서 gravity(중력)가 사라진다는 뜻이 아니라, 추가 추력 없이 무한히 멀어질 수 있다는 뜻입니다. Circular motion(원운동)의 속력 조건에는 ṙ<sub>0</sub> = 0도 필요합니다.'),
    card('9. 타원 궤도의 주기는 전체 면적을 면적속도로 나눕니다.',
         'Semimajor axis(장반경) a = (r<sub>p</sub> + r<sub>a</sub>)/2, semiminor axis(단반경) b = √(r<sub>p</sub>r<sub>a</sub>)이면 ellipse area(타원 면적)는 πab입니다. Period(주기) τ = πab/(h/2) = 2πab/h입니다. r<sub>p</sub>, r<sub>a</sub>에는 altitude(고도)가 아닌 중심까지의 거리를 대입합니다.',
         '시험용 보강: p = b²/a와 h² = μp를 결합하면 τ = 2π√(a³/μ), 즉 τ² = (4π²/μ)a³을 얻습니다. 같은 central body(중심 천체)라면 τ² ∝ a³인 Kepler’s third law(케플러 제3법칙)가 됩니다. 동일한 μ 조건 없이 지구 위성과 태양 주위 행성의 비례상수를 같게 놓지 않습니다.'),
    card('10. 두 예제는 주어진 정보에 따라 출발식이 다릅니다.',
         'Sample Problem 1(예제 1)은 두 apses(근점·원점)의 고도가 모두 주어져 있습니다. r<sub>A</sub> = 6370 + 400 = 6770 km, r<sub>B</sub> = 6370 + 4000 = 10370 km로 바꾸고 r<sub>A</sub>v<sub>A</sub> = r<sub>B</sub>v<sub>B</sub>를 쓰면 v<sub>B</sub> = 30000(6770/10370) ≈ 19590 km/h입니다. 이 값은 제시된 두 지점 조건으로 얻는 원본의 각운동량 풀이입니다.',
         'Sample Problem 2(예제 2)는 초기 altitude(고도) 500 km와 speed(속력) 36900 km/h만 주어집니다. r<sub>0</sub> = 6.87×10⁶ m, v<sub>0</sub> = 10250 m/s, h ≈ 70.4×10⁹ m²/s, μ ≈ 398×10¹² m³/s²를 구합니다. C ≈ 65.3×10⁻⁹ m⁻¹, r<sub>a</sub> = 1/(μ/h²−C) ≈ 66700 km이므로 maximum altitude(최대고도)는 약 60300 km입니다. 이어 a ≈ 36.8×10⁶ m, b ≈ 21.4×10⁶ m를 사용하면 τ ≈ 70.3×10³ s, 약 19 h 31 min입니다. 중간값은 충분한 자릿수로 유지한 뒤 마지막에 반올림합니다.'),
])

add('Lecture 5 · 중심력에 의한 운동','MC2103 · Fall 2026',
    'Motion under Central Force(중심력에 의한 운동)를 다루는 Lecture 5의 표지입니다. 강의 인덱스 기준 Week 04, 날짜는 2026-09-23입니다.',role='Title')
add('Lecture 5-1 · 위성 운동으로 확장하기','Overview 00:17–00:59',
    'Overview(도입 영상)는 지난 단원의 Newton’s law(뉴턴 법칙)를 satellite(위성)와 planet(행성)에 적용할 수 있는지 묻습니다. Angular momentum(각운동량)의 보존으로 궤도와 escape speed(탈출 속력)를 계산하는 것이 이번 단원의 연결점입니다.',role='Divider')
add('원본의 도입 참고 영상','원본 링크 슬라이드',
    '<a href="https://youtu.be/QAfL3b9Qs3A" target="_blank" rel="noreferrer">슬라이드에 수록된 참고 영상 열기</a>. 이 링크는 인덱스의 Overview(도입 영상)와 다른 참고 링크입니다. 이 노트의 영상 근거는 인덱스에 지정된 5개 강의 영상입니다.',role='Video link')
add('Lecture 5-2 · 각운동량과 보존 법칙','Contents 1',
    'Angular momentum(각운동량)의 정의, moment(힘의 모멘트)와의 관계, central force(중심력)에서의 보존을 다룹니다.',role='Divider')
add('위성 궤도에서 무엇이 보존되는지 찾습니다.','Contents 1 00:19–00:37',
    'Satellite(위성)는 지구에서 멀어지거나 가까워지며 speed(속력)와 direction(방향)을 바꿀 수 있습니다. 따라서 constant velocity(일정한 속도)를 전제로 풀 수 없습니다. 대신 지구 중심에 대한 angular momentum(각운동량)이 conserved(보존)된다는 사실을 이용합니다.',
    '그림의 r은 지구 중심에서 satellite(위성)까지의 거리이고 R은 Earth radius(지구 반지름)입니다. 두 값의 차이가 altitude(고도)입니다. 원 안에 그려진 지구 중심과 orbit center(궤도 중심)를 같다고 가정하지 않는 것이 이후 ellipse(타원) 해석의 출발점입니다.')
add('극좌표 가속도를 뉴턴 법칙에 대입합니다.','Contents 1 00:37–00:56',
    'Polar coordinates(극좌표)는 outward radial direction(바깥쪽 반지름 방향) e<sub>r</sub>와 increasing-angle transverse direction(각도 증가 횡방향) e<sub>θ</sub>를 사용합니다. ΣF<sub>r</sub>과 ΣF<sub>θ</sub>는 실제 force(힘)를 이 두 축에 투영한 signed components(부호 있는 성분)입니다.',
    'Radial acceleration(반지름 가속도)은 r̈ 자체가 아니라 r̈ − rθ̇²이고, transverse acceleration(횡방향 가속도)은 rθ̈ + 2ṙθ̇입니다. 좌표의 unit vectors(단위벡터)도 회전하므로 추가 항이 생깁니다. Lecture 3의 kinematics(운동학) 식에 mass(질량)를 곱한 것이며 새로운 force(힘)를 더하는 과정이 아닙니다.',
    eq='ΣF<sub>r</sub> = m(r̈ − rθ̇²)<br>ΣF<sub>θ</sub> = m(rθ̈ + 2ṙθ̇)')
add('횡방향 운동방정식과 각운동량 변화는 같은 관계입니다.','Contents 1 00:56–02:05',
    'Planar motion(평면운동)의 signed angular momentum(부호 있는 각운동량 성분)은 H<sub>O</sub> = mr²θ̇입니다. Constant mass(일정 질량)에서 product rule(곱의 미분법)을 적용하면 dH<sub>O</sub>/dt = m(2rṙθ̇ + r²θ̈)입니다. 이 식에서 r을 묶으면 mr(rθ̈ + 2ṙθ̇), 즉 rΣF<sub>θ</sub>가 됩니다.',
    'rΣF<sub>θ</sub>는 O에 대한 resultant moment(합모멘트)입니다. 이 관계 자체는 moment(모멘트)가 있어도 성립합니다. 그중 ΣF<sub>θ</sub> = 0인 특별한 경우에 H<sub>O</sub>가 constant(일정)합니다. “각운동량 식을 쓰는 것”과 “각운동량이 보존된다고 놓는 것”은 다릅니다.',
    eq='d(mr²θ̇)/dt = mr(rθ̈ + 2ṙθ̇) = rΣF<sub>θ</sub>')
add('각운동량은 위치벡터와 선운동량의 외적입니다.','Contents 1 02:15–03:13',
    'Linear momentum(선운동량)은 m<b>v</b>입니다. 이를 위치와 함께 표현한 angular momentum about O(O점에 대한 각운동량)는 <b>H</b><sub>O</sub> = <b>r</b> × m<b>v</b>입니다. “About O(O점에 대한)”는 필수 정보입니다. 같은 입자라도 기준점이 달라지면 position vector(위치벡터)가 달라져 angular momentum(각운동량)이 달라질 수 있습니다.',
    'Cross product(외적)의 순서는 중요합니다. m<b>v</b> × <b>r</b>로 뒤집으면 direction(방향)이 반대입니다. Right-hand rule(오른손 법칙)로 <b>r</b>에서 <b>v</b> 쪽으로 손가락을 굽힐 때 엄지가 <b>H</b><sub>O</sub> 방향입니다. 단위는 kg·m²/s입니다. 이 단락의 단위·오른손 법칙 설명은 정의를 풀어 쓴 시험용 보강입니다.',
    eq='<b>H</b><sub>O</sub> ≡ <b>r</b> × m<b>v</b>')
add('반지름에 수직인 속도 성분만 각운동량을 만듭니다.','Contents 1 03:25–03:46 · 07:08',
    'φ는 position vector(위치벡터)와 velocity vector(속도벡터)의 included angle(끼인각)입니다. Cross product magnitude(외적의 크기)는 H<sub>O</sub> = rmv sinφ입니다. Radial velocity(반지름 속도)는 <b>r</b>과 parallel(평행)하므로 외적에 기여하지 않고, transverse velocity(횡방향 속도) v<sub>θ</sub> = v sinφ만 기여합니다.',
    '따라서 진행 방향을 θ 증가 방향으로 정하면 H<sub>O</sub> = rmv<sub>θ</sub> = mr²θ̇입니다. 벡터 <b>H</b><sub>O</sub>는 <b>r</b>과 m<b>v</b>가 만드는 plane(평면)에 perpendicular(수직)합니다. 일반적인 3D calculation(3차원 계산)에서는 determinant(행렬식)를 전개해 성분을 구할 수 있습니다.',
    eq='H<sub>O</sub> = rmv sinφ = rmv<sub>θ</sub> = mr²θ̇<br><b>H</b><sub>O</sub> = m(yv<sub>z</sub>−zv<sub>y</sub>)<b>i</b> + m(zv<sub>x</sub>−xv<sub>z</sub>)<b>j</b> + m(xv<sub>y</sub>−yv<sub>x</sub>)<b>k</b>',
    extra=card('시험용 보강 · 크기와 부호','반대 방향으로 θ가 감소한다면 mr²θ̇는 법선축에 대한 signed component(부호 있는 성분)이며 magnitude(크기)는 mr²|θ̇|입니다. 이 노트의 위성 예제는 h &gt; 0이 되도록 각도 증가 방향을 택합니다.'))
add('정의를 미분하면 힘의 모멘트가 나옵니다.','Contents 1 03:56–04:55',
    'Fixed point(고정점) O를 기준으로 position vector(위치벡터)를 미분한 d<b>r</b>/dt는 <b>v</b>입니다. Constant mass(일정 질량)를 가정하고 외적을 product rule(곱의 미분법)로 미분하면 <b>v</b> × m<b>v</b> + <b>r</b> × m<b>a</b>가 됩니다. 첫 항은 parallel vectors(평행 벡터)의 외적이므로 0입니다.',
    '남은 m<b>a</b>를 Newton’s second law(뉴턴 제2법칙)의 Σ<b>F</b>로 바꾸면 <b>r</b> × Σ<b>F</b>입니다. 이것이 O에 대한 sum of moments(모멘트의 합) Σ<b>M</b><sub>O</sub>입니다. Angular momentum(각운동량) 자체가 0인 것이 아니라 첫 번째 미분 항만 0이 된다는 점을 구분합니다.',
    eq='d<b>H</b><sub>O</sub>/dt = <b>v</b> × m<b>v</b> + <b>r</b> × m<b>a</b><br>= 0 + <b>r</b> × Σ<b>F</b> = Σ<b>M</b><sub>O</sub>')
add('합모멘트는 각운동량의 시간 변화율입니다.','Contents 1 05:09–05:42',
    'The sum of moments(모멘트의 합)가 rate of change of angular momentum(각운동량의 시간 변화율)과 같다는 명제입니다. Linear motion(선운동)의 Σ<b>F</b> = d(m<b>v</b>)/dt와 구조가 비슷하지만, 여기서는 force(힘)가 아니라 moment about O(O에 대한 모멘트)가 angular momentum(각운동량)을 변화시킵니다.',
    '시험용 보강: Σ<b>M</b><sub>O</sub> = 0이면 각운동량 벡터가 일정합니다. 반면 Σ<b>F</b> = 0이면 선운동량 벡터가 일정합니다. 중심력 문제에서는 대개 Σ<b>F</b> ≠ 0이므로 선운동량은 변하지만 각운동량은 보존됩니다. 가속하는 임의의 기준점에는 위 유도식을 조건 확인 없이 적용하지 않습니다.',
    eq='Σ<b>M</b><sub>O</sub> = d<b>H</b><sub>O</sub>/dt')
add('중심력은 항상 같은 고정점을 지나는 힘입니다.','Contents 1 05:42–06:12',
    'Central force(중심력)는 fixed point(고정점) O를 향하거나 O에서 멀어지는 방향으로 작용합니다. 핵심은 방향이 언제나 <b>r</b>과 collinear(한 직선 위)라는 점입니다. 그림의 화살표는 attractive force(인력)의 예이고, outward repulsive force(바깥쪽 척력)도 정의에 포함됩니다.',
    'Central force(중심력)라는 조건만으로 inverse-square law(역제곱 법칙)가 정해지는 것은 아닙니다. 모든 중심력은 O에 대해 zero moment(0의 모멘트)를 만들지만, 이후 conic orbit(원뿔곡선 궤도)은 특별히 F ∝ 1/r²인 중력에서 얻습니다. 이 둘의 적용 범위를 분리해야 합니다.')
add('중심력의 모멘트팔이 0이므로 각운동량이 보존됩니다.','Contents 1 06:12–06:35',
    'Moment arm(모멘트팔)은 O에서 line of action(작용선)까지의 perpendicular distance(수직거리)입니다. Central force(중심력)의 작용선은 O를 통과하므로 이 거리가 0입니다. 벡터로도 <b>r</b> × <b>F</b> = <b>0</b>이므로 d<b>H</b><sub>O</sub>/dt = <b>0</b>입니다.',
    '따라서 angular momentum(각운동량)의 magnitude(크기)와 direction(방향)이 모두 constant(일정)합니다. 영상 스크립트의 “momentum itself is zero”는 주변의 moment arm(모멘트팔) 설명과 원본 수식에 비추어 moment(힘의 모멘트)가 0이라는 의미로 처리합니다. <b>H</b><sub>O</sub>는 일반적으로 0이 아닌 일정한 벡터입니다.',
    eq='Σ<b>M</b><sub>O</sub> = <b>0</b> ⇒ <b>H</b><sub>O</sub> = <b>r</b> × m<b>v</b> = constant')
add('보존 법칙은 두 위치의 운동과 궤도 평면을 연결합니다.','Contents 1 06:44–07:08',
    '서로 다른 시각의 r, v, φ가 각각 달라도 mrv sinφ의 값은 같습니다. Constant mass(일정 질량)를 약분하면 rv sinφ = r<sub>0</sub>v<sub>0</sub>sinφ<sub>0</sub>입니다. 여기서 φ는 위치벡터와 속도벡터 사이 각도이며, polar angle(극각) θ와 다른 기호입니다.',
    'Specific angular momentum(단위 질량당 각운동량) h = H<sub>O</sub>/m = r²θ̇를 정의하면 모든 후속 식에서 m이 사라집니다. <b>H</b><sub>O</sub>가 nonzero(0이 아니고) 고정되어 있으면 <b>r</b>은 항상 이 벡터에 수직이므로 motion(운동)은 O를 지나는 하나의 plane(평면)에 놓입니다.',
    eq='rv sinφ = r<sub>0</sub>v<sub>0</sub>sinφ<sub>0</sub><br>h = H<sub>O</sub>/m = r²θ̇ = constant',
    extra=card('시험용 보강 · h = 0인 경우','Pure radial motion(순수 반지름 운동)에서는 <b>r</b>과 <b>v</b>가 평행해 h = 0입니다. 보존 법칙은 여전히 맞지만 고유한 orbit plane(궤도 평면)의 법선은 정해지지 않습니다. h로 나누는 이후의 궤도 미분방정식은 이 경우에 적용하지 않습니다.'))
add('아주 작은 부채꼴의 면적을 시간으로 나눕니다.','Contents 1 07:17–08:30',
    'Radius vector(반지름벡터)가 dθ만큼 회전할 때 swept area(휩쓴 면적) dA를 생각합니다. 미소 구간에서는 삼각형의 밑변을 r, 높이를 r dθ로 볼 수 있어 dA = ½r²dθ입니다. r이 변해도 미소 극한에서 이 식이 성립합니다.',
    '양변을 dt로 나누면 dA/dt = ½r²θ̇입니다. 이를 areal velocity(면적속도)라 부릅니다. 일반 velocity(속도)의 단위 m/s와 달리 면적속도의 단위는 m²/s입니다. 초당 몇 미터 이동하는지가 아니라 지구 중심에서 연결한 선이 초당 얼마의 면적을 쓸어가는지 나타냅니다.',
    eq='dA = ½r²dθ<br>dA/dt = ½r²θ̇')
add('각운동량 보존은 면적속도 일정으로 읽을 수 있습니다.','Contents 1 08:41–09:00',
    'Central force(중심력)에서 h = r²θ̇는 constant(일정)합니다. 앞 장의 dA/dt = ½r²θ̇와 결합하면 dA/dt = h/2도 일정합니다. 두 구간의 elapsed time(경과시간)이 같다면 swept area(휩쓴 면적)도 같습니다.',
    '시험용 보강: ΔA = (h/2)Δt이므로 면적 비율과 시간 비율은 같습니다. 전체 ellipse area(타원 면적)의 ¼을 휩쓰는 데는 전체 period(주기)의 ¼이 걸립니다. 그러나 polar angle(극각) 90°를 움직이는 시간이 반드시 주기의 ¼인 것은 아닙니다. 지구는 타원 중심이 아니라 focus(초점)에 있기 때문입니다.',
    eq='dA/dt = h/2 = constant<br>ΔA = (h/2)Δt')
add('Lecture 5-3 · 만유인력과 궤도','Contents 2',
    'Newton’s law of gravitation(뉴턴의 만유인력 법칙)을 사용해 trajectory(궤적)의 형태와 escape speed(탈출 속력), period(주기)를 계산하는 구간입니다.',role='Divider')
add('중력은 중심력의 중요한 사례입니다.','Contents 2 00:17–00:25',
    'Sun–planet(태양–행성)이나 Earth–satellite(지구–위성) 사이의 gravitational force(중력)는 두 중심을 잇는 방향으로 작용하는 attractive force(인력)입니다. 따라서 중심 천체를 고정된 것으로 근사하면 그 중심에 대한 angular momentum(각운동량)이 보존됩니다.',
    '편집자 보강: 실제로 두 천체는 서로 끌어당겨 함께 움직입니다. 이번 강의는 M이 m보다 매우 크다고 보고 central body(중심 천체)의 motion(운동)을 무시하는 모델입니다. 정확한 two-body relative motion(두 물체의 상대운동)에서는 중력 매개변수 G(M+m)가 등장하지만 이번 예제에는 강의와 같은 GM을 사용합니다.')
add('만유인력의 크기는 중심 사이 거리의 제곱에 반비례합니다.','Contents 2 00:35–01:10',
    '두 mass(질량) M과 m 사이의 거리 r에 대해 F = GMm/r²입니다. 두 물체가 받는 force(힘)는 equal in magnitude(크기가 같고) opposite in direction(방향이 반대)입니다. 다만 서로 다른 물체에 작용하므로 한 위성의 free-body diagram(자유물체도)에서 서로 상쇄하지 않습니다.',
    '원본의 G = 66.73×10⁻¹² m³/(kg·s²)는 강의에서 사용하는 근삿값입니다. r이 두 배가 되면 F는 ¼이 되고, 단위는 kg·m/s² = N이 됩니다. F는 양의 magnitude(크기)이며 outward radial direction(바깥쪽 반지름 방향)을 양으로 잡으면 force component(힘 성분)는 F<sub>r</sub> = −F입니다.',
    eq='F = GMm/r²<br><b>F</b> = −(GMm/r²)<b>e</b><sub>r</sub>')
add('지표 중력으로 GM을 구하되, 궤도 전체에 g를 고정하지 않습니다.','Contents 2 01:23–02:03',
    'Earth’s surface(지표면)에서는 r = R이므로 weight(중량) W = GMm/R²입니다. 다른 표현 W = mg와 같게 놓고 m을 약분하면 g = GM/R²입니다. 따라서 지구의 mass(질량)를 따로 몰라도 GM = gR²를 계산할 수 있습니다.',
    '시험용 보강: μ ≡ GM을 gravitational parameter(중력 매개변수)라고 쓰면 궤도 계산이 간결해집니다. 원본 예제의 R = 6.37×10⁶ m, g = 9.81 m/s²를 사용하면 μ = 3.98059389×10¹⁴ m³/s²입니다. 높은 곳의 acceleration magnitude(가속도 크기)는 μ/r² = g(R/r)²이므로 g보다 작습니다.',
    eq='g = GM/R²<br>μ ≡ GM = gR²<br>F/m = μ/r² = g(R/r)²')

add('횡방향 힘이 없다는 조건으로 시간을 각도로 바꿉니다.','Contents 2 02:13–04:02',
    'Attractive central force(끌어당기는 중심력)의 magnitude(크기)를 F &gt; 0으로 정의하면 ΣF<sub>r</sub> = −F, ΣF<sub>θ</sub> = 0입니다. Radial equation(반지름 운동방정식)은 m(r̈ − rθ̇²) = −F입니다. Transverse equation(횡방향 운동방정식)은 rθ̈ + 2ṙθ̇ = 0이며, r을 곱하면 d(r²θ̇)/dt = 0입니다.',
    '따라서 θ̇ = h/r²입니다. Trajectory(궤적)의 모양은 r이 θ에 따라 어떻게 변하는지 알면 되므로, 시간 t를 없애고 u(θ) = 1/r을 새 변수로 둡니다. 이때 dot(점)은 t에 대한 미분, prime(프라임)은 θ에 대한 미분입니다. 표기상의 차이를 놓치면 r̈와 u″를 같은 미분으로 잘못 취급하게 됩니다.',
    eq='m(r̈ − rθ̇²) = −F<br>m(rθ̈ + 2ṙθ̇) = 0<br>h = r²θ̇,  θ̇ = hu²',
    extra=card('시험용 보강 · 생략된 연쇄법칙',
        'r = u⁻¹이므로 dr/dθ = −u⁻²u′입니다. Chain rule(연쇄법칙)을 쓰면 ṙ = (dr/dθ)θ̇ = (−u⁻²u′)(hu²) = −hu′입니다. h가 constant(일정)이므로 다시 시간 미분하면 r̈ = −h(du′/dθ)θ̇ = −h²u²u″입니다.',
        formula('ṙ = −hu′<br>r̈ = −h²u²u″ = −(h²/r²)d²(1/r)/dθ²')))
add('중심력의 궤도 방정식을 유도합니다.','Contents 2 04:11–04:54',
    '앞 장에서 얻은 r̈ = −h²u²u″와 rθ̇² = (1/u)(hu²)² = h²u³을 radial equation(반지름 운동방정식)에 대입합니다. 그러면 −mh²u²(u″ + u) = −F입니다. 양변을 −mh²u²로 나누면 원본의 궤도 미분방정식이 됩니다.',
    'Force law(힘의 법칙) F(r)를 알면 F(1/u)로 바꿔 이 differential equation(미분방정식)을 풉니다. Initial conditions(초기조건)는 integration constants(적분상수)를 정합니다. 여기까지는 중력뿐 아니라 r의 함수로 주어지는 다른 중심력에도 사용할 수 있으나, h ≠ 0이고 r &gt; 0이어야 합니다.',
    eq='u″ + u = F/(mh²u²),  u = 1/r',
    extra=card('시험용 보강 · 부호와 해의 의미','원본의 F는 inward force magnitude(안쪽 힘의 크기)입니다. Signed radial force(부호 있는 반지름 힘) F<sub>r</sub>를 사용하면 우변은 −F<sub>r</sub>/(mh²u²)입니다. 또한 u(θ)는 orbit shape(궤도 모양)를 주며 position as a function of time(시간에 따른 위치)까지 바로 주지는 않습니다. 시간은 dt = r²dθ/h를 추가로 적분해 구합니다.'))
add('역제곱 중력에서는 미분방정식의 우변이 상수가 됩니다.','Contents 2 05:02–06:15',
    'Earth’s gravity(지구 중력)만 작용할 때 F = GMm/r² = μmu²입니다. 이를 앞 장의 F/(mh²u²)에 대입하면 m과 u²가 약분되어 μ/h²만 남습니다. μ = GM은 지구에 대한 상수이고 h는 central force(중심력) 때문에 conserved(보존)되는 상수입니다.',
    '즉 궤도 식은 u″ + u = μ/h²라는 constant-forcing differential equation(상수 우변 미분방정식)이 됩니다. 강의에서 “h가 일정하다”는 것은 편의상 새로 가정한 조건이 아니라 이미 보존 법칙에서 얻은 결과입니다. 원 궤도를 가정한 적이 없으므로 이 단계에서 r은 변할 수 있습니다.',
    eq='F = μmu² ⇒ u″ + u = μ/h²')
add('방정식의 해는 초점이 지구 중심인 원뿔곡선입니다.','Contents 2 06:22–08:03',
    '시험용 보강 · 해를 구하는 과정: constant particular solution(상수 특수해) u<sub>p</sub> = μ/h²와 homogeneous solution(동차해) A cosθ + B sinθ를 더하면 일반해입니다. 각도 원점을 적절히 회전시키면 A cosθ + B sinθ = C cosθ로 쓸 수 있습니다. 이때 θ = 0을 periapsis(근점)에 두면 C ≥ 0입니다.',
    '따라서 1/r = (μ/h²)(1 + ε cosθ)이며 eccentricity(이심률) ε = Ch²/μ입니다. Conic section(원뿔곡선)의 polar equation(극방정식)과 같은 모양입니다. 여기서 O는 central body center(중심 천체 중심)이자 focus(초점)이며, 일반적인 ellipse center(타원 중심)와는 다릅니다.',
    eq='u = μ/h² + A cosθ + B sinθ<br>r = p/(1 + ε cosθ),  p = h²/μ,  ε = Ch²/μ ≥ 0',
    extra=card('시험용 보강 · 기호와 좌표 선택','p는 semilatus rectum(반통경)으로 길이 단위, C는 inverse length(길이의 역수) 단위, ε는 dimensionless(무차원)입니다. Parabola(포물선)는 초점이 하나입니다. 영상의 “usually two foci”를 모든 원뿔곡선에 공통인 정의로 옮기지 않습니다. 임의의 발사점을 θ = 0으로 고정하면 C가 음수일 수 있으며, 이 경우는 30·32장에서 구별합니다.'))
add('이심률 하나로 궤도 형태를 분류합니다.','Contents 2 08:10–08:19',
    'Eccentricity(이심률) ε는 conic orbit(원뿔곡선 궤도)의 형태를 정합니다. ε = 0은 circle(원), 0 &lt; ε &lt; 1은 ellipse(타원), ε = 1은 parabola(포물선), ε &gt; 1은 hyperbola(쌍곡선)입니다. Circle(원)은 ellipse(타원)의 특별한 경우입니다.',
    '같은 force law(힘의 법칙)라도 initial position(초기 위치)과 initial velocity(초기 속도)가 다르면 h와 ε가 달라져 궤도 모양이 바뀝니다. 단, “중심력이면 언제나 타원·포물선·쌍곡선”이라는 결론은 틀립니다. 이번 분류는 inverse-square gravity(역제곱 중력)의 방정식을 풀어서 나온 결과입니다.',
    extra=table(['Eccentricity(이심률)','Trajectory(궤적)','특성'],[
        ('ε = 0','Circle(원)','중심까지 거리 일정'),('0 &lt; ε &lt; 1','Ellipse(타원)','Bound(묶인), 유한한 근점·원점 거리'),('ε = 1','Parabola(포물선)','Escape threshold(탈출 경계)'),('ε &gt; 1','Hyperbola(쌍곡선)','Unbound(묶이지 않은) 궤적')]))
add('같은 지점에서 출발해도 초기 속력에 따라 경로가 달라집니다.','Contents 2 08:27–09:55',
    '그림의 A에서 tangential initial velocity(횡방향 초기 속도)를 주면 중력은 항상 지구 중심 O를 향합니다. Initial speed(초기 속력)에 따라 먼 곳으로 계속 가거나, 돌아오는 ellipse(타원)를 만들거나, circle(원)을 만들 수 있습니다. 그림은 서로 다른 initial conditions(초기조건)의 궤도를 겹쳐 비교한 것입니다.',
    'θ = 0을 perigee(근지점) A로 두는 경우에는 r이 가장 작습니다. θ가 커질수록 1 + ε cosθ가 작아지며 r이 증가합니다. ε가 1 이상이면 어떤 방향에서 이 분모가 0에 접근할 수 있어 r이 무한히 커지는 escape trajectory(탈출 궤적)가 가능합니다.',
    eq='1/r = (μ/h²)(1 + ε cosθ)')
add('쌍곡선에서는 유한한 극각의 극한에서 거리가 무한대로 갑니다.','Contents 2 10:03–10:18',
    'Hyperbola(쌍곡선)는 ε &gt; 1입니다. r = p/(1+ε cosθ)에서 r → ∞가 되는 asymptotic direction(점근 방향)을 구하려면 denominator(분모)를 0으로 놓습니다. 따라서 cosθ<sub>∞</sub> = −1/ε입니다.',
    '예를 들어 ε = 2이면 θ<sub>∞</sub> = ±120°입니다. 이 수치 예는 식을 적용한 시험용 보강입니다. 물리적으로 가능한 궤적 구간은 r &gt; 0, 즉 1+ε cosθ &gt; 0인 범위입니다. 분모가 음수인 값을 그대로 음의 거리로 해석하지 않습니다.',
    eq='ε &gt; 1<br>1 + ε cosθ<sub>∞</sub> = 0<br>θ<sub>∞</sub> = ±cos⁻¹(−1/ε)')
add('포물선은 닫힌 궤도와 탈출 궤도의 경계입니다.','Contents 2 10:18–10:24',
    'Parabola(포물선)는 ε = 1이며 r = p/(1 + cosθ)입니다. θ → 180°일 때 cosθ → −1이므로 r → ∞입니다. Ellipse(타원)와 달리 유한한 apogee(원지점)나 orbital period(공전 주기)가 없습니다.',
    '시험용 보강: Ideal gravitational model(이상 중력 모델)에서 parabolic escape(포물선 탈출)는 무한히 멀어질 때 speed(속력)가 0으로 접근하는 최소 에너지 탈출입니다. Hyperbolic escape(쌍곡선 탈출)는 무한대에서도 남는 speed(속력)가 있습니다. 포물선에서 θ = 180°의 위치에 유한 시간 안에 도착한다는 뜻은 아닙니다.',
    eq='ε = 1<br>1 + cosθ<sub>∞</sub> = 0 ⇒ θ<sub>∞</sub> = 180°')
add('타원은 유한한 거리로 닫히고, 원은 이심률이 정확히 0입니다.','Contents 2 10:24–10:46 · 원본 29·32장',
    '0 ≤ ε &lt; 1이면 1 + ε cosθ ≥ 1−ε &gt; 0이므로 모든 θ에서 r이 finite(유한)합니다. ε가 0보다 크면 r은 달라지고 ellipse(타원)가 됩니다. ε = 0일 때만 r = p라는 constant radius(일정 반지름)가 되어 circle(원)이 됩니다.',
    '근점 기준 좌표에서는 θ = 0에 perigee(근지점), θ = 180°에 apogee(원지점)가 있습니다. 같은 orbit(궤도)에서 근지점은 speed(속력)가 가장 크고 원지점은 가장 작습니다. 두 점에서 radial velocity(반지름 속도)는 0이고 h = rv가 같습니다.',
    eq='r<sub>p</sub> = p/(1+ε),  r<sub>a</sub> = p/(1−ε)<br>Circle(원): ε = 0 ⇒ r = p',
    correction='원본의 “circle, for ε &lt; 0”은 ε = 0으로 교정합니다. Contents 2 10:37–10:46의 “less than or equal to zero”도 채택하지 않습니다. 같은 영상 09:47–09:55, 원본 32장의 ε = 0, 그리고 r = p/(1+ε cosθ)의 θ 의존성을 대조한 결과입니다. Negative eccentricity(음의 이심률)는 표준 분류가 아닙니다.')
add('자유비행을 시작하는 위치와 속도로 적분상수를 정합니다.','Contents 2 10:55–11:36',
    '그림은 powered flight(추력 비행) 뒤 burnout(연소 종료) A에서 free flight(자유비행)가 시작되는 상황입니다. 강의의 도식에서는 initial velocity(초기 속도)가 반지름에 perpendicular(수직)하여 h = r<sub>0</sub>v<sub>0</sub>입니다. 모든 발사에서 이 식을 조건 없이 쓰면 안 됩니다. 일반적으로는 h = r<sub>0</sub>v<sub>0</sub>sinφ<sub>0</sub>입니다.',
    'A를 θ = 0으로 정하면 cos0 = 1이고 1/r<sub>0</sub> = μ/h² + C입니다. 따라서 C = 1/r<sub>0</sub> − μ/h²입니다. 이 initial-condition equation(초기조건 식)이 특정 궤도를 선택하며, 원본처럼 근지점에서 시작하는 경우 C ≥ 0입니다.',
    eq='h = r<sub>0</sub>v<sub>0</sub>  (ṙ<sub>0</sub> = 0)<br>C = 1/r<sub>0</sub> − μ/h²<br>= 1/r<sub>0</sub> − μ/(r<sub>0</sub>v<sub>0</sub>)²',
    extra=card('시험용 보강 · 일반해에서 사인 항이 사라지는 이유','u = μ/h² + A cosθ + B sinθ이면 u′(0) = B입니다. ṙ<sub>0</sub> = −hB이므로 horizontal launch(수평 발사)의 ṙ<sub>0</sub> = 0은 B = 0을 뜻합니다. 이때 A = C입니다. 수평이 아닌 초기 속도라면 B를 버릴 수 없고 두 초기 속도 성분을 모두 반영해야 합니다.'))
add('탈출 속력은 무한히 멀어질 수 있는 최소 초기 속력입니다.','Contents 2 11:45–13:23',
    '지구 표면과 충돌하지 않는 tangential launch(횡방향 발사)를 생각합니다. 근지점 기준 eccentricity(이심률) ε ≥ 1이면 parabola(포물선) 또는 hyperbola(쌍곡선)입니다. C ≥ μ/h²와 C = 1/r<sub>0</sub> − μ/h²를 합치면 1/r<sub>0</sub> ≥ 2μ/h²가 됩니다.',
    'h² = r<sub>0</sub>²v<sub>0</sub>²를 대입하면 v<sub>0</sub>² ≥ 2μ/r<sub>0</sub>입니다. Equality(등호)일 때가 escape threshold(탈출 경계)이고, 이를 escape speed(탈출 속력)라고 합니다. 원본의 velocity(속도)라는 명칭에도 불구하고 √(2μ/r<sub>0</sub>) 자체는 magnitude(크기)인 속력입니다.',
    eq='v<sub>esc</sub> = √(2μ/r<sub>0</sub>)<br>v<sub>0</sub> = v<sub>esc</sub>: parabola(포물선)<br>v<sub>0</sub> &gt; v<sub>esc</sub>: hyperbola(쌍곡선)',
    extra=card('오해 방지','Escape(탈출)는 gravity(중력)가 어느 경계 바깥에서 갑자기 0이 된다는 뜻이 아닙니다. Ideal model(이상 모델)에서는 중력이 계속 작용해도 물체가 다시 돌아오지 않고 r → ∞로 갈 수 있습니다. 지구 이외의 천체·대기·추력을 고려하는 실제 임무의 필요 속도를 이 식 하나로 결정하지 않습니다.'))
add('원 궤도 속력보다 느린 발사도 타원일 수 있습니다.','Contents 2 13:32–14:09',
    'Circle(원)이 되려면 ε = 0, 즉 C = 0이어야 합니다. 1/r<sub>0</sub> = μ/(r<sub>0</sub>v<sub>0</sub>)²에서 v<sub>circ</sub> = √(μ/r<sub>0</sub>)를 얻습니다. 같은 결과는 circular motion(원운동)의 inward acceleration(안쪽 가속도) v²/r과 μ/r²를 같게 놓아도 얻습니다.',
    'v<sub>circ</sub> &lt; v<sub>0</sub> &lt; v<sub>esc</sub>이면 A가 perigee(근지점)인 ellipse(타원)입니다. 반면 0 &lt; v<sub>0</sub> &lt; v<sub>circ</sub>이면 A가 apogee(원지점)인 ellipse(타원)입니다. 후자는 지구 표면을 가로지를 수 있으므로 “탈출 속력보다 느리면 항상 안전한 위성 궤도”라는 뜻이 아닙니다.',
    eq='v<sub>circ</sub> = √(μ/r<sub>0</sub>)<br>v<sub>esc</sub> = √2 v<sub>circ</sub>',
    extra=card('시험용 보강 · C의 부호와 물리적인 이심률','발사점을 θ = 0으로 고정하면 Ch²/μ = r<sub>0</sub>v<sub>0</sub>²/μ − 1은 음수일 수 있습니다. 이때 ε = |C|h²/μ가 실제 eccentricity(이심률)이고, periapsis(근점) 기준 각도는 180° 이동해야 합니다. C의 음수 부호는 궤도의 방향 기준을 나타낼 뿐 circle(원)을 뜻하지 않습니다.'))
add('면적속도는 일정하지만, 지구는 타원 중심에 있지 않습니다.','Contents 2 14:21–14:30',
    '그림에서 C는 ellipse center(타원 중심), O는 Earth center(지구 중심)이자 focus(초점)입니다. Semimajor axis(장반경) a와 semiminor axis(단반경) b는 C를 기준으로 잰 타원의 크기이고, r<sub>0</sub>, r<sub>1</sub>은 O에서 근지점·원지점까지 잰 거리입니다.',
    'Areal velocity(면적속도) h/2는 O에서 출발한 radius vector(반지름벡터)가 휩쓰는 면적의 변화율입니다. C를 기준으로 한 각도가 균일하게 증가한다고 가정하면 안 됩니다. 한 바퀴 동안 O에서 이어진 반지름벡터가 전체 ellipse area(타원 면적) πab를 휩쓴다는 것이 다음 period(주기) 식의 근거입니다.',
    eq='dA/dt = h/2 = constant')
add('주기는 타원 면적을 일정한 면적속도로 나눈 값입니다.','Contents 2 14:44–15:00',
    '한 번의 revolution(공전)에 걸리는 period(주기) τ는 total swept area(전체 휩쓴 면적) πab를 constant areal velocity(일정 면적속도) h/2로 나누어 구합니다. 단위도 m² ÷ (m²/s) = s이므로 time(시간)이 됩니다.',
    'Perigee radius(근지점 거리) r<sub>p</sub>와 apogee radius(원지점 거리) r<sub>a</sub>를 알면 a = (r<sub>p</sub>+r<sub>a</sub>)/2, b = √(r<sub>p</sub>r<sub>a</sub>)입니다. 강의는 이 두 거리를 r<sub>0</sub>, r<sub>1</sub>로 표시합니다. Earth radius(지구 반지름)를 뺀 altitude(고도)를 넣지 않습니다.',
    eq='τ = πab/(h/2) = 2πab/h<br>a = (r<sub>p</sub> + r<sub>a</sub>)/2<br>b = √(r<sub>p</sub>r<sub>a</sub>)',
    extra=card('시험용 보강 · 단반경 공식의 기하학','Focus distance(중심에서 초점까지 거리) c = (r<sub>a</sub>−r<sub>p</sub>)/2입니다. Ellipse(타원)의 b² = a²−c²에 대입하면 [(r<sub>p</sub>+r<sub>a</sub>)²−(r<sub>a</sub>−r<sub>p</sub>)²]/4 = r<sub>p</sub>r<sub>a</sub>이므로 b = √(r<sub>p</sub>r<sub>a</sub>)가 됩니다.'))
add('행성 궤도에도 같은 중력 모형을 적용합니다.','Contents 2 15:09–15:19',
    'Earth–satellite(지구–위성)에 사용한 inverse-square gravity(역제곱 중력)와 angular momentum conservation(각운동량 보존)은 Sun–planet(태양–행성)에도 적용할 수 있습니다. 중심을 태양으로 옮기고 central mass(중심 질량) M을 태양 질량으로 바꿉니다.',
    '이때 gravitational parameter(중력 매개변수) μ도 달라집니다. 같은 형식의 방정식을 쓴다고 해서 지구와 태양의 숫자를 섞는 것은 아닙니다. 강의는 이 결과를 Kepler’s laws(케플러 법칙)와 연결합니다.')
add('케플러의 세 법칙은 궤도 모양·면적·주기의 관계입니다.','Contents 2 15:19–16:09',
    'First law(제1법칙): 각 planet(행성)은 태양을 한 focus(초점)에 둔 ellipse(타원)를 그립니다. 여기서 타원은 bound planetary orbit(묶인 행성 궤도)의 서술이며, 모든 천체 궤도가 타원이라는 말은 아닙니다.',
    'Second law(제2법칙): 태양에서 planet(행성)으로 그은 radius vector(반지름벡터)는 equal areas in equal times(같은 시간에 같은 면적)를 휩씁니다. 이것이 dA/dt = h/2 일정과 같습니다. Third law(제3법칙): 같은 중심 천체에 대해 orbital period squared(주기의 제곱)는 semimajor axis cubed(장반경의 세제곱)에 proportional(비례)합니다.',
    eq='τ² ∝ a³  (same central body: 같은 중심 천체)',
    extra=card('시험용 보강 · 제3법칙의 유도',
        'r<sub>p</sub> = p/(1+ε), r<sub>a</sub> = p/(1−ε)에서 a = p/(1−ε²), b² = p²/(1−ε²)이므로 b² = ap입니다. h² = μp = μb²/a를 주기 식에 넣으면 τ² = 4π²a²b²/h² = 4π²a³/μ입니다. 따라서 두 궤도의 μ가 같을 때 τ₁/τ₂ = (a₁/a₂)<sup>3/2</sup>입니다.',
        formula('τ = 2π√(a³/μ)<br>τ²/a³ = 4π²/μ')))

add('Lecture 5-4 · 위성 문제풀이','Problem Solving',
    '두 위치의 angular momentum(각운동량)을 비교하는 예제와, initial conditions(초기조건)로 최대고도·주기를 구하는 예제를 다룹니다.',role='Divider')
add('예제 1 · 최대고도에서의 속력을 구합니다.','Problem Solving 00:17–01:09',
    'Satellite(위성)가 altitude(고도) 400 km에서 parallel to the surface(지표면에 평행하게) 30000 km/h로 출발합니다. Maximum altitude(최대고도)는 4000 km이고 Earth radius(지구 반지름)는 6370 km라고 주어져 있습니다. Determine the velocity(속도를 구하라)가 요구사항입니다.',
    '그림 A의 horizontal launch(수평 발사)는 initial radial velocity(초기 반지름 속도) ṙ<sub>A</sub> = 0을 뜻합니다. B는 maximum radial distance(최대 중심 거리)인 apogee(원지점)이므로 ṙ<sub>B</sub> = 0입니다. 두 위치 모두 <b>r</b>과 <b>v</b>가 perpendicular(수직)하며, A에서는 위쪽, B에서는 아래쪽으로 움직이는 그림입니다.',
    eq='r<sub>A</sub> = 6370 + 400 = 6770 km<br>r<sub>B</sub> = 6370 + 4000 = 10370 km')
add('예제 1 · 두 지점의 각운동량을 같게 놓습니다.','Problem Solving 01:17–01:32',
    'Central force(중심력)만 작용한다고 두면 angular momentum about Earth’s center(지구 중심에 대한 각운동량)가 conserved(보존)됩니다. 두 지점의 radius(중심까지 거리)와 A에서의 speed(속력)가 모두 주어졌으므로, 궤도 전체의 differential equation(미분방정식)을 다시 풀 필요는 없습니다.',
    '일반식 mr<sub>A</sub>v<sub>A</sub>sinφ<sub>A</sub> = mr<sub>B</sub>v<sub>B</sub>sinφ<sub>B</sub>에서 두 각도가 90°이므로 sine factors(사인 인자)는 1입니다. Mass(질량)는 양변에서 약분됩니다. 따라서 위성의 질량 정보가 없어도 풀 수 있습니다.',
    eq='r<sub>A</sub>v<sub>A</sub> = r<sub>B</sub>v<sub>B</sub><br>v<sub>B</sub> = v<sub>A</sub>(r<sub>A</sub>/r<sub>B</sub>)')
add('예제 1 · 고도가 아닌 중심까지의 거리를 비율에 넣습니다.','Problem Solving 01:39–02:38',
    'v<sub>B</sub> = 30000 × 6770/10370 = 19585.34… km/h입니다. 원본은 약 19590 km/h로 제시합니다. r<sub>A</sub>/r<sub>B</sub>가 dimensionless(무차원)이므로 두 거리를 모두 km로 사용하면 속력의 km/h 단위를 그대로 유지할 수 있습니다.',
    '결과는 A보다 먼 B에서 lower speed(더 낮은 속력)를 갖습니다. 방향까지 요구되면 원본 그림 기준 downward tangential direction(아래쪽 접선 방향)이라고 씁니다. 400/4000을 사용하면 고도 비율을 넣은 잘못된 답이 됩니다.',
    eq='v<sub>B</sub> = (30000 km/h) × (6770/10370)<br>≈ 19590 km/h, downward at B(B에서 아래쪽)',
    extra=card('편집자 보강 · 원본 입력값의 물리적 일관성',
        '위 답은 문제에 주어진 두 apses(근점·원점)의 고도와 angular momentum conservation(각운동량 보존)을 그대로 사용하는 강의의 풀이입니다. 다만 R = 6370 km, g = 9.81 m/s²인 gravity-only model(중력만 작용하는 모델)에 초기 30000 km/h를 궤도 방정식까지 적용하면 maximum altitude(최대고도)는 약 3394 km이며, 주어진 4000 km와 일치하지 않습니다. 따라서 원본의 모든 수치가 하나의 정확한 중력 궤도를 동시에 나타내는 것은 아닙니다.',
        '검산 방법은 다음 예제와 같은 h = r<sub>A</sub>v<sub>A</sub>, C = 1/r<sub>A</sub>−μ/h², r<sub>a</sub> = 1/(μ/h²−C)입니다. 이 노트는 원본 값을 임의로 교체하지 않고, 예제 1을 주어진 두 위치 사이의 각운동량 계산으로 보존합니다.'))
add('가까워지면 증가하는 속도 성분과 추력의 방향을 구별합니다.','Problem Solving 02:45–03:34',
    'Angular momentum(각운동량)이 conserved(보존)되는 동안 transverse speed(횡방향 속력)는 v<sub>θ</sub> = h/r입니다. 따라서 r이 줄어들면 v<sub>θ</sub>는 증가합니다. Pure gravity(중력만 작용)인 위성이 안쪽으로 떨어지는 구간에서는 전체 speed(속력)도 증가하지만, 이는 중력이 하는 일과도 연결되는 설명입니다.',
    '원본은 thruster(추진기)로 지구에 가까워지는 상황을 언급합니다. “Thruster(추진기)를 쓰면 언제나 angular momentum(각운동량)이 보존된다”로 일반화하지 않습니다. Pure radial thrust(순수 반지름 방향 추력)는 지구 중심에 대한 moment(모멘트)가 0이지만 transverse thrust(횡방향 추력)는 angular momentum(각운동량)을 바꿀 수 있습니다.',
    eq='v<sub>θ</sub> = h/r<br>v = √(ṙ² + v<sub>θ</sub>²)',
    correction='적용 범위 보강: h 일정에서 곧바로 얻는 관계는 rv<sub>θ</sub> = h이지 일반적인 rv = h가 아닙니다. 원본의 “velocity increases”를 모든 추력 상황의 전체 속력에 대한 결론으로 확대하지 않습니다. 근거는 원본 9·14장의 H<sub>O</sub> = rmv sinφ와 모멘트 식입니다.')
add('예제 2 · 최대고도와 한 바퀴 도는 시간을 구합니다.','Problem Solving 03:41–04:09',
    'Satellite(위성)는 altitude(고도) 500 km에서 parallel to the surface(지표면에 평행하게) v<sub>0</sub> = 36900 km/h로 출발합니다. Determine(구하라)의 대상은 maximum altitude(최대고도)와 periodic time(공전 주기)입니다. 원본의 지구 반지름은 뒤의 계산에서 R = 6370 km로 사용됩니다.',
    '예제 1과 달리 반대쪽 거리 r<sub>a</sub>가 아직 주어지지 않았습니다. Angular momentum conservation(각운동량 보존)만 쓰면 r<sub>a</sub>v<sub>a</sub> = h라는 식 하나에 두 미지수가 남습니다. 따라서 gravitational orbit equation(중력 궤도 방정식)까지 사용해야 합니다.',
    eq='z<sub>0</sub> = 500 km, v<sub>0</sub> = 36900 km/h<br>Find(구할 값): z<sub>max</sub>, τ')
add('예제 2 · 초기조건, 원지점 거리, 타원 면적 순서로 풉니다.','Problem Solving 04:19–05:00',
    '먼저 altitude(고도)를 r<sub>0</sub> = R + z<sub>0</sub>로 바꾸고 speed(속력)를 m/s로 변환합니다. Tangential launch(횡방향 발사) 조건으로 h = r<sub>0</sub>v<sub>0</sub>를 구한 뒤, θ = 0에서 C = 1/r<sub>0</sub> − μ/h²를 결정합니다.',
    '이번 수치는 v<sub>circ</sub> ≈ 7612 m/s &lt; 10250 m/s &lt; v<sub>esc</sub> ≈ 10765 m/s이므로 A가 perigee(근지점)인 ellipse(타원)입니다. 이 조건 검사는 식에서 계산한 시험용 보강입니다. 따라서 opposite apsis(반대쪽 apsis) θ = 180°가 apogee(원지점)이며 1/r<sub>a</sub> = μ/h² − C입니다. 마지막에 r<sub>a</sub>에서 R을 빼고 a, b를 구해 τ = 2πab/h를 적용합니다.',
    eq='r<sub>0</sub>, v<sub>0</sub> → h, μ → C → r<sub>a</sub><br>z<sub>max</sub> = r<sub>a</sub> − R<br>r<sub>0</sub>, r<sub>a</sub> → a, b → τ')
add('예제 2 · 궤도 방정식에 초기점과 반대점을 대입합니다.','Problem Solving 05:13–05:30',
    '발사점 A를 θ = 0으로 택했으므로 orbit equation(궤도 방정식)은 1/r = μ/h² + C cosθ입니다. θ = 0에서는 cosθ = 1, θ = 180°에서는 cosθ = −1입니다. 두 점을 구분하는 것은 새로운 방정식이 아니라 같은 방정식에 서로 다른 angle(각도)을 대입하는 것입니다.',
    '지구 중심 O에서 반대점 A′까지의 r<sub>1</sub>이 이 노트의 r<sub>a</sub>입니다. 원본의 그림 속 maximum altitude(최대고도) 화살표와 r<sub>1</sub>을 동일한 길이로 읽지 않도록 주의합니다. 둘은 Earth radius(지구 반지름)만큼 다릅니다.',
    eq='θ = 0: 1/r<sub>0</sub> = μ/h² + C<br>θ = 180°: 1/r<sub>a</sub> = μ/h² − C')
add('예제 2 · 적분상수는 약 65.3×10⁻⁹ m⁻¹입니다.','Problem Solving 05:22–05:38',
    '다음 원본 46장에서 계산하는 r<sub>0</sub>, h, μ를 사용합니다. r<sub>0</sub> = 6.87×10⁶ m이므로 1/r<sub>0</sub> ≈ 145.560×10⁻⁹ m⁻¹입니다. 중간 자릿수를 유지하면 μ/h² ≈ 80.276×10⁻⁹ m⁻¹입니다. 두 값을 빼면 C ≈ 65.284×10⁻⁹ m⁻¹, 즉 원본의 65.3×10⁻⁹ m⁻¹입니다.',
    'C &gt; 0이고 ε = Ch²/μ ≈ 0.813이므로 이번 궤도는 ellipse(타원)입니다. 작은 두 inverse-distance values(거리 역수 값)를 빼므로 중간값을 지나치게 반올림하면 나중에 reciprocal(역수)을 취할 때 오차가 커집니다. 표시 숫자는 요약값이고 계산에는 원래 자릿수를 유지합니다.',
    eq='1/r<sub>0</sub> ≈ 145.560×10⁻⁹ m⁻¹<br>μ/h² ≈ 80.276×10⁻⁹ m⁻¹<br>C = 1/r<sub>0</sub> − μ/h²<br>≈ 65.284×10⁻⁹ m⁻¹',
    correction='원본 대입식의 분모 (70.4 m²/s)²에는 ×10⁹가 빠져 있습니다. 올바른 크기는 (70.4×10⁹ m²/s)²입니다. 근거는 원본 46장의 h = r<sub>0</sub>v<sub>0</sub> 계산과 이 장의 최종 C 값입니다. 슬라이드 이미지는 수정하지 않았습니다.')
add('예제 2 · 단위 변환과 h, GM 계산을 확인합니다.','Problem Solving 05:38–05:46',
    'r<sub>0</sub> = (6370+500) km = 6.87×10⁶ m입니다. v<sub>0</sub> = 36900 km/h × (1000 m/km)/(3600 s/h) = 10250 m/s입니다. 두 값의 곱은 h = 7.04175×10¹⁰ m²/s, 강의의 반올림 표기로 70.4×10⁹ m²/s입니다.',
    'μ = GM = gR²에는 위성의 초기 거리 r<sub>0</sub>가 아니라 Earth radius(지구 반지름) R이 들어갑니다. g가 지표면에서의 gravitational acceleration(중력가속도)이기 때문입니다. 따라서 μ = 9.81×(6.37×10⁶)² = 3.98059389×10¹⁴ m³/s² ≈ 398×10¹² m³/s²입니다.',
    eq='r<sub>0</sub> = 6.87×10⁶ m<br>v<sub>0</sub> = 10.25×10³ m/s<br>h = r<sub>0</sub>v<sub>0</sub> = 70.4175×10⁹ m²/s<br>μ = gR² = 398.059389×10¹² m³/s²',
    correction='원본의 h = v<sub>0</sub>v<sub>0</sub>는 h = r<sub>0</sub>v<sub>0</sub>로 교정합니다. 같은 줄의 실제 대입은 거리×속도이며, h의 단위 m²/s와 일치합니다. v<sub>0</sub>²의 단위 m²/s²와는 다릅니다.')
add('예제 2 · 중심 거리에서 지구 반지름을 빼야 최대고도입니다.','Problem Solving 05:46–05:54',
    'θ = 180°를 대입하면 1/r<sub>a</sub> = μ/h² − C입니다. 충분한 자릿수를 유지한 계산에서는 약 14.991×10⁻⁹ m⁻¹이므로 r<sub>a</sub> ≈ 6.67025×10⁷ m = 66702.5 km입니다. 원본의 반올림 결과는 66700 km입니다.',
    '이 값은 지구 중심으로부터의 거리입니다. Maximum altitude(최대고도)는 z<sub>max</sub> = r<sub>a</sub> − R ≈ 66702.5 − 6370 = 60332.5 km입니다. 원본과 같은 유효숫자 수준으로 쓰면 약 60300 km입니다. 최종 보고에는 거리인지 고도인지 반드시 구별합니다.',
    eq='r<sub>a</sub> = 1/(μ/h² − C) ≈ 66700 km<br>z<sub>max</sub> = r<sub>a</sub> − R ≈ 60300 km',
    correction='이 장의 분모에도 h의 ×10⁹가 누락되어 있습니다. (70.4×10⁹ m²/s)²로 읽습니다. 또한 마지막 줄의 “k”는 수치와 문맥상 km 단위로 처리합니다. 원본 46장의 값과 단위로 교차 확인했습니다.')
add('예제 2 · 타원의 크기를 구하면 주기는 약 19시간 31분입니다.','Problem Solving 05:54–06:21',
    'a = (r<sub>0</sub> + r<sub>a</sub>)/2 ≈ (6.87+66.7)×10⁶/2 = 36.8×10⁶ m입니다. b = √(r<sub>0</sub>r<sub>a</sub>) ≈ √(6.87×66.7)×10⁶ = 21.4×10⁶ m입니다. 원본 문장의 “altitudes at the perigee and apogee”를 문자 그대로 고도 대입으로 해석하면 안 됩니다. 표시된 식은 중심 거리 r<sub>0</sub>, r<sub>a</sub>를 사용합니다.',
    'τ = 2πab/h ≈ 2π(36.8×10⁶)(21.4×10⁶)/(70.4×10⁹) ≈ 70.3×10³ s입니다. 약 19시간 31분으로 원본 답과 같습니다. 이 시간은 perigee(근지점)에서 apogee(원지점)까지가 아니라 한 바퀴의 orbital period(공전 주기)입니다.',
    eq='a ≈ 36.8×10⁶ m,  b ≈ 21.4×10⁶ m<br>τ = 2πab/h ≈ 70.3×10³ s ≈ 19 h 31 min',
    extra=card('시험용 보강 · 정밀 검산과 반 바퀴 시간','중간 반올림을 하지 않으면 τ ≈ 70264.22 s = 19 h 31 min 4 s입니다. τ = 2π√(a³/μ)로도 같은 값을 얻습니다. Perigee-to-apogee time(근지점에서 원지점까지 시간)은 타원 면적의 절반을 휩쓰므로 τ/2, 약 9 h 45 min 32 s입니다.'))
add('궤도 공식의 출발점은 여전히 뉴턴 제2법칙입니다.','Problem Solving 06:21–06:48',
    '이 satellite(위성)는 하루보다 짧은 orbital period(공전 주기) 동안 지표에서 약 6만 km 떨어진 최대고도까지 갔다 돌아옵니다. 여기서 6만 km는 최대 altitude(고도)의 규모이며 한 바퀴의 traveled distance(이동 거리)가 아닙니다.',
    '최종 식 1/r = μ/h² + C cosθ는 독립적인 경험 공식이 아닙니다. Newton’s second law(뉴턴 제2법칙) → polar equations(극좌표 방정식) → angular momentum conservation(각운동량 보존) → orbit differential equation(궤도 미분방정식) → initial conditions(초기조건)의 순서로 얻었습니다. 공식을 사용할 때 가정과 좌표 기준까지 함께 기억해야 하는 이유입니다.')
add('참고문헌','원본 참고문헌',
    'Beer, Johnston, Cornwell, Self, Sanghi, <cite>Vector Mechanics for Engineers: Dynamics</cite>, 12th Edition, Chapter 12. 원본에 수록된 참고문헌 페이지를 그대로 보존합니다.',role='References')

assert len(records) == 50, len(records)

exam_items = [
    ('Define angular momentum about O(O점에 대한 각운동량을 정의하라).',
     'The angular momentum of a particle about O is H_O = r × mv, where r is measured from O to the particle. Its direction is perpendicular to the plane containing r and v, according to the right-hand rule.',
     'About O(O점에 대한), cross product(외적), perpendicular(수직), right-hand rule(오른손 법칙)을 포함한 정의입니다. 벡터 기호는 실제 답안에서 화살표나 굵은 표기로 구별합니다.'),
    ('Why is angular momentum conserved under a central force(중심력에서 각운동량이 보존되는 이유)?',
     'A central force acts along a line through the fixed point O. Therefore, its moment about O is zero. Since ΣM_O = dH_O/dt, the angular momentum vector remains constant.',
     'Fixed point(고정점), zero moment(0의 모멘트), remains constant(일정하게 유지됨)를 순서대로 연결합니다. Force(힘) 자체가 0이라고 쓰지 않습니다.'),
    ('Does conserved angular momentum imply constant speed(각운동량 보존은 일정 속력을 뜻하는가)?',
     'No. Conservation gives h = rv sinφ = rv_θ, not constant v. In a noncircular gravitational orbit, the speed changes with position while h remains constant.',
     'Conserved(보존되는) 물리량과 constant speed(일정 속력)를 구별합니다. Noncircular(원형이 아닌) 궤도에서는 각운동량이 같아도 속력은 달라질 수 있습니다.'),
    ('State the condition for r_Av_A = r_Bv_B(이 관계식의 조건을 말하라).',
     'The angular momentum must be conserved, and the velocity must be perpendicular to the radius vector at both points. These conditions hold at the perigee and apogee of a gravitational elliptical orbit.',
     'Perpendicular to(…에 수직), at both points(두 점 모두에서)가 핵심 조건입니다. 일반 위치에서는 sinφ 또는 transverse component(횡방향 성분)가 필요합니다.'),
    ('Explain equal areas in equal times(같은 시간에 같은 면적을 설명하라).',
     'The area swept by the radius vector satisfies dA/dt = r²θ̇/2 = h/2. Since h is constant under a central force, equal time intervals correspond to equal swept areas.',
     'Swept area(휩쓴 면적)는 distance traveled(이동 거리)나 angle swept(휩쓴 각도)와 다릅니다. Equal(같은) 대상이 무엇인지 정확히 씁니다.'),
    ('Derive the orbit equation for inverse-square gravity(역제곱 중력의 궤도식을 유도하라).',
     'Let u = 1/r and h = r²θ̇. Then ṙ = −hu′ and r̈ = −h²u²u″, where primes denote differentiation with respect to θ. Substitution into m(r̈ − rθ̇²) = −μmu² gives u″ + u = μ/h².',
     'Substitute(대입하라), with respect to θ(θ에 관하여), prime(프라임)의 정의를 포함합니다. h ≠ 0인 궤도를 다루는 유도입니다.'),
    ('Classify an orbit by eccentricity(이심률로 궤도를 분류하라).',
     'Using the nonnegative eccentricity ε, the orbit is a circle for ε = 0, an ellipse for 0 < ε < 1, a parabola for ε = 1, and a hyperbola for ε > 1. The force center is a focus of the conic.',
     'Nonnegative(음이 아닌), focus(초점)를 명시합니다. “ε &lt; 0이면 원”이라는 원본 오탈자를 답안에 옮기지 않습니다.'),
    ('Find the circular and escape speeds(원 궤도 속력과 탈출 속력을 구하라) at radius r_0.',
     'For tangential motion, the circular speed is v_circ = √(μ/r_0). The escape speed is v_esc = √(2μ/r_0) = √2 v_circ. A speed equal to v_esc corresponds to the parabolic escape threshold.',
     'At radius r_0(r_0의 중심 거리에서), tangential(횡방향), equal to(…와 같은), threshold(경계)를 구별합니다. r_0에는 altitude(고도)가 아니라 R + altitude(고도)를 넣습니다.'),
    ('Determine the speed at maximum altitude(최대고도에서 속력을 구하라) in Sample Problem 1.',
     'Using the two apsis distances specified in the problem, conservation of angular momentum gives r_Av_A = r_Bv_B. Thus v_B = 30000(6370 + 400)/(6370 + 4000) ≈ 19590 km/h. The velocity is tangent to the orbit, downward at B in the figure.',
     'Specified in the problem(문제에 지정된) 두 지점의 조건을 사용하는 원본 풀이입니다. 수치의 gravity-only consistency(중력만 작용하는 궤도 일관성)는 원본 40장 아래에서 별도로 검토했습니다.'),
    ('Determine the maximum altitude(최대고도를 구하라) in Sample Problem 2.',
     'r_0 = 6.87×10⁶ m and v_0 = 10250 m/s give h = r_0v_0 ≈ 7.04×10¹⁰ m²/s. With μ = gR² and C = 1/r_0 − μ/h², the apogee radius is r_a = 1/(μ/h² − C) ≈ 66700 km. The maximum altitude is r_a − R ≈ 60300 km.',
     'Apogee radius(원지점 중심 거리)와 maximum altitude(최대고도)를 별개의 줄로 적으면 R을 빼는 마지막 단계를 놓치지 않습니다.'),
    ('Determine the orbital period(공전 주기를 구하라) of the ellipse(타원).',
     'The semiaxes are a = (r_p + r_a)/2 and b = √(r_pr_a). Since the areal velocity is h/2, the period is τ = πab/(h/2) = 2πab/h. For Sample Problem 2, τ ≈ 7.03×10⁴ s, or about 19 h 31 min.',
     'Semiaxes(반축), areal velocity(면적속도), period(주기)의 관계를 설명합니다. 이것은 one complete revolution(완전한 한 바퀴)의 시간입니다.'),
    ('State Kepler’s third law(케플러 제3법칙을 서술하라).',
     'For orbits around the same central body in the fixed-center gravitational model, the square of the period is proportional to the cube of the semimajor axis: τ² = (4π²/μ)a³.',
     'Same central body(같은 중심 천체), proportional to(…에 비례), semimajor axis(장반경)를 포함합니다. 원본의 정성적 법칙을 식으로 표현한 시험용 보강입니다.'),
]

terms = [
    ('central force','중심력','작용선이 같은 고정점을 지나는 힘'),('force center / fixed point','힘의 중심 / 고정점','중심력의 모든 작용선이 지나는 기준점'),
    ('angular momentum','각운동량','H_O = r × mv; 기준점을 명시해야 하는 벡터'),('linear momentum','선운동량','mv; 각운동량과 다른 물리량'),
    ('moment / torque','힘의 모멘트 / 토크','기준점에 대한 r × F'),('moment arm','모멘트팔','기준점과 힘의 작용선 사이 수직거리'),
    ('line of action','작용선','힘 벡터를 포함하는 직선'),('cross product','외적','두 벡터에 수직인 벡터를 만드는 곱'),
    ('right-hand rule','오른손 법칙','외적의 방향을 정하는 규칙'),('perpendicular / parallel','수직인 / 평행한','각각 90° / 나란한 방향 관계'),
    ('conserved / constant','보존되는 / 일정한','시간에 따라 변하지 않음; 벡터라면 크기와 방향 모두 확인'),('specific angular momentum','단위 질량당 각운동량','h = H_O/m, 단위 m²/s'),
    ('radial / transverse','반지름 방향의 / 횡방향의','극좌표의 바깥 방향 / 각도 증가 방향'),('inward / outward','안쪽으로 / 바깥쪽으로','힘의 중심 쪽 / 중심에서 멀어지는 쪽'),
    ('areal velocity','면적속도','단위 시간당 휩쓴 면적, dA/dt = h/2'),('swept area','휩쓴 면적','중심에서 입자로 그은 선이 움직이며 덮는 면적'),
    ('equal areas in equal times','같은 시간에 같은 면적','케플러 제2법칙; 같은 거리나 각도가 아님'),('gravitational force','중력','두 질량 사이의 인력'),
    ('inverse-square law','역제곱 법칙','크기가 거리의 제곱에 반비례하는 법칙'),('gravitational parameter','중력 매개변수','μ = GM; 단위 m³/s²'),
    ('altitude / radial distance','고도 / 중심까지 거리','지표에서 잰 높이 / r = R + 고도'),('free flight / powered flight','자유비행 / 추력 비행','이 모형에서 중력만 작용 / 추력이 작용하는 구간'),
    ('burnout','연소 종료','로켓 추력 비행이 끝나는 시점'),('tangential launch','횡방향 발사','초기 속도가 중심까지의 반지름에 수직인 발사'),
    ('parallel to the surface','지표면에 평행하게','이 문제에서 초기 반지름 속도 ṙ_0 = 0'),('initial condition','초기조건','특정 해를 정하는 초기 위치·속도'),
    ('integration constant','적분상수','미분방정식의 일반해에서 초기조건으로 정하는 상수'),('trajectory / orbit','궤적 / 궤도','입자가 지나가는 위치의 곡선'),
    ('conic section','원뿔곡선','원·타원·포물선·쌍곡선'),('focus / foci','초점 / 초점들','원뿔곡선의 기하학적 기준점; 타원 중심과 구별'),
    ('eccentricity','이심률','궤도 형태를 정하는 음이 아닌 무차원 수'),('circle / circular','원 / 원형의','ε = 0, 중심까지 거리 일정'),
    ('ellipse / elliptic','타원 / 타원형의','여기서는 0 < ε < 1인 닫힌 궤도'),('parabola / parabolic','포물선 / 포물선형의','ε = 1인 탈출 경계'),
    ('hyperbola / hyperbolic','쌍곡선 / 쌍곡선형의','ε > 1인 묶이지 않은 궤적'),('bound / unbound','묶인 / 묶이지 않은','닫힌 궤도로 돌아옴 / 무한히 멀어질 수 있음'),
    ('perigee / apogee','근지점 / 원지점','지구 중심에 가장 가까운 점 / 가장 먼 점'),('periapsis / apoapsis','근점 / 원점','임의의 중심 천체에 대한 가장 가까운 점 / 가장 먼 점'),
    ('semimajor / semiminor axis','장반경 / 단반경','타원 중심에서 잰 긴 반축 a / 짧은 반축 b'),('semilatus rectum','반통경','원뿔곡선 극방정식의 p = h²/μ'),
    ('escape speed / circular speed','탈출 속력 / 원 궤도 속력','√(2μ/r) / √(μ/r)'),('period / periodic time','주기 / 공전 주기','완전한 한 바퀴에 필요한 시간'),
    ('revolution','공전 한 바퀴','궤도상의 한 완전 주회'),('asymptote / asymptotic','점근선 / 점근적인','멀리 갈수록 접근하는 직선 / 그러한 극한 성질'),
    ('finite / infinite','유한한 / 무한한','거리의 범위와 극한을 표현'),('magnitude / signed component','크기 / 부호 있는 성분','벡터의 길이 / 특정 축에 투영한 값'),
    ('determine / evaluate','구하라 / 계산하라','문제의 미지수 또는 식의 값을 구하는 지시'),('substitute / differentiate / integrate','대입하라 / 미분하라 / 적분하라','풀이 단계의 동사'),
    ('proportional to','…에 비례하는','두 양의 비가 일정함'),('maximum altitude','최대고도','이 문제에서 원지점 중심 거리에서 지구 반지름을 뺀 값'),
]

audit = [
    ('Contents 1 02:26·03:46','mess / MB','mass(질량) / m<b>v</b>','원본 8–9장의 정의'),
    ('Contents 1 04:38–05:18','y cross m a / Romans','<b>r</b> × m<b>a</b> / moments(힘의 모멘트)','원본 10–11장의 미분식'),
    ('Contents 1 05:58–06:29','center Force / movement arm / momentum itself is zero','central force(중심력) / moment arm(모멘트팔) / 모멘트가 0','원본 12–13장. 각운동량은 0이 아니라 일정'),
    ('Contents 1 08:30 및 Contents 2 14:21–15:00','area velocity / area of velocity','areal velocity(면적속도)','원본 15·33·34장'),
    ('Contents 2 01:31·02:32·06:01','horse / Polar protein systems / math math','Earth(지구) / polar coordinate system(극좌표계) / mass(질량)','원본 20–23장의 대상과 기호'),
    ('Contents 2 07:57','usually two foci','모든 원뿔곡선에 초점이 둘이라는 정의로 사용하지 않음','포물선은 초점 하나; 원본은 중심 천체가 한 초점임을 말함'),
    ('원본 29 · Contents 2 10:37–10:46','원 조건 ε < 0 / less than or equal to zero','ε = 0','원본 32, 영상 09:47–09:55, 궤도식의 각도 의존성'),
    ('원본 24–32','ε = Ch²/μ와 수평 발사점 θ = 0의 혼용 가능성','근점 기준 C ≥ 0과 발사점 기준 부호 있는 C를 구별','초기조건 식 재유도; 편집자 보강'),
    ('Contents 2 14:44·15:37','one Evolution / equal distance','one revolution(공전 한 바퀴) / equal area(같은 면적)','바로 뒤의 자체 정정과 원본 34·36장'),
    ('Problem Solving 01:09·03:54','6380 a 70 / 36 1900','6370 km / 36900 km/h','원본 38·42·46장의 수치'),
    ('Problem Solving 01:32','velocity at P','velocity at B(B점 속도)','원본 38–40장의 A·B 위치'),
    ('Problem Solving 04:51·06:04','parity / Parisi / apology','perigee(근지점) / apogee(원지점)','원본 43·48장의 용어'),
    ('원본 38–40','초기 30000 km/h와 최대고도 4000 km의 조합','원본의 각운동량 답을 유지하고 중력 궤도 입력 불일치를 별도 표시','μ = gR²로 궤도 방정식을 재계산하면 최대고도 약 3394 km'),
    ('원본 41 · Problem Solving 02:45–03:34','추력으로 가까워질 때 속도가 증가한다는 일반적 서술','반지름 추력 조건과 vθ = h/r를 명시','원본 9·14장의 외적 정의와 모멘트 관계'),
    ('원본 45·47','분모의 (70.4 m²/s)²','(70.4×10⁹ m²/s)²','원본 46의 h값과 최종 수치'),
    ('원본 46','h = v₀v₀','h = r₀v₀','같은 줄의 거리×속도 대입과 m²/s 단위'),
    ('원본 47·48','고도 계산의 k 단위 / altitudes를 a,b에 사용한다는 문장','km / a,b에는 지구 중심 거리 사용','원본 46–48의 실제 대입식'),
    ('원본 45–48','반올림된 C, h, a, b','원본 최종 답과 중간 반올림 없는 검산을 구별','g=9.81, R=6370 km로 재계산'),
    ('Problem Solving 06:48','Newton’s second one','Newton’s second law(뉴턴 제2법칙)','원본 49장의 마지막 문장'),
]

roadmap = '''<section class="editorial-section section-divider" id="course-roadmap" aria-labelledby="roadmap-title">
<p class="section-kicker">Summary video · Course roadmap</p>
<h2 class="section-title" id="roadmap-title">Summary 영상 후반: 다음 단원은 일과 에너지입니다.</h2>
<p class="section-lead">Summary 00:17–00:43은 이번 강의의 central force(중심력), angular momentum conservation(각운동량 보존), 궤도와 탈출 조건을 복습하므로 앞의 핵심 개념 요약에 반영했습니다. 00:43 이후는 다음 단원 예고이므로 현재 개념 요약과 구분합니다.</p>
</section>
<section class="editorial-section" id="roadmap-detail" aria-labelledby="roadmap-detail-title">
<p class="section-kicker">What comes next</p>
<h2 class="section-title" id="roadmap-detail-title">힘과 운동을 에너지의 관점으로 연결합니다.</h2>
<div class="card"><h3>Work and energy principle(일과 에너지 원리)</h3><p>영상은 다음 단원에서 potential energy(위치에너지)와 kinetic energy(운동에너지)를 다룬다고 예고합니다. 이번 강의의 궤도 계산에 필요한 새로운 필수 공식으로 제시한 내용은 아닙니다. 현재 강의 인덱스의 다음 항목은 Week 05 · 2026-09-30 · Lecture 6입니다.</p></div>
<div class="evidence"><span>Summary 00:43–00:59</span><span>강의 인덱스 대조</span></div>
</section>'''

template = (SITE / 'templates/lecture-page.template.html').read_text(encoding='utf-8')
source_pattern = r'<section class="source-section"[\s\S]*?</section>'
source_template = re.search(source_pattern, template).group()
sections = []
for n, (title, evidence, blocks, role) in enumerate(records, 1):
    section = source_template
    values = {'NN': f'{n:02d}', 'SLIDE_ROLE': role, 'SLIDE_HEADING': title,
              'LECTURE_SLUG': 'lecture05', 'DESCRIPTIVE_ALT_TEXT': f'Lecture 5 원본 슬라이드 {n:02d}: {escape(title)}',
              'CURRENT_PAGE': str(n), 'PAGE_COUNT': '50', 'TRANSCRIPT_TIME_OR_SLIDE_ROLE': evidence,
              'SLIDE_EXPLANATION_BLOCKS': blocks}
    for key, value in values.items():
        section = section.replace('{{'+key+'}}', value)
    sections.append(section)
template = re.sub(source_pattern, lambda _: '\n\n'.join(sections), template, count=1)
exam_html = ''.join('<div class="exam-card"><h3>'+q+'</h3><div class="answer"><span class="answer__label">Model answer</span>'+escape(a)+'</div><p style="margin-top: 12px">'+ko+'</p></div>' for q, a, ko in exam_items)
template = re.sub(r'<div class="exam-card">\s*<h3>\{\{EXAM_QUESTION\}\}</h3>[\s\S]*?</div>\s*</div>', lambda _: exam_html+'\n          </div>', template, count=1)
videos = [('Overview','e6CYZ3fRRn8'),('Contents 1','LO3tJFnPtGc'),('Contents 2','XNCbWvN9bg4'),('Problem Solving','r786FbIQots'),('Summary','2Mi9L9DWCDE')]
toc = [('overview','전체 개요'),('concept-map','개념 지도'),('concept-summary','핵심 개념 요약')] + [(f'slide-{i:02d}',f'{i:02d} · {row[0]}') for i,row in enumerate(records,1)] + [('course-roadmap','Summary · 다음 단원 안내'),('exam-english','시험 영어'),('glossary','용어집'),('asr-log','원본·스크립트 교정'),('sources','출처')]
values = {
    'LECTURE_NUMBER':'Lecture 5', 'LECTURE_TITLE':'Motion under Central Force',
    'ONE_SENTENCE_DESCRIPTION':'4주차 중심력 운동: 원본 50장과 영어 영상 5개를 종합한 한국어 수업 대체 노트',
    'WEEK':'Week 04', 'DATE_OR_날짜_미기재':'2026-09-23', 'PAGE_COUNT':'50',
    'LECTURE_PROMISE':'Central force(중심력)와 angular momentum(각운동량)을 연결하고, 위성의 orbit(궤도)·escape speed(탈출 속력)·period(주기)를 유도와 예제로 설명합니다.',
    'VIDEO_SET':'Overview · Contents 1·2 · Problem Solving · Summary',
    'ALL_CONTENTS_AND_PROBLEM_SOLVING_BUTTONS':'\n'.join(f'<a class="button button--primary" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상 열기</a>' for label,vid in videos[1:4]),
    'ORIGINAL_PDF_URL':'https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/lecture05_note.pdf',
    'LECTURE_NOTE_FILENAME':'lecture05_note.pdf',
    'CORE_RELATIONSHIP_HEADLINE':'힘의 방향에서 보존량을 찾고, 보존량으로 궤도를 풉니다.',
    'CORE_RELATIONSHIP_EXPLANATION':'같은 고정점을 향하는 central force(중심력)는 그 점에 대해 moment(모멘트)를 만들지 않습니다. 이 성질이 angular momentum conservation(각운동량 보존)과 constant areal velocity(일정 면적속도)로 이어지고, 중력의 역제곱 법칙과 결합하면 위성의 궤도 모양과 주기를 계산할 수 있습니다.',
    'CONCEPT_MAP_HEADLINE':'중심력, 각운동량, 궤도는 하나의 유도로 연결됩니다.',
    'CONCEPT_MAP_BLOCKS':'<div class="grid-3">'+card('Central force(중심력)','작용선이 fixed point(고정점) O를 지나므로 moment about O(O점에 대한 모멘트)가 0입니다.')+card('Conservation(보존)','Angular momentum(각운동량)과 areal velocity(면적속도)가 일정합니다. 속도와 거리가 서로 연결됩니다.')+card('Orbit(궤도)','Inverse-square gravity(역제곱 중력)와 initial conditions(초기조건)로 궤도 모양, 최대고도, 탈출 속력, 주기를 구합니다.')+'</div>',
    'STANDALONE_CONCEPT_SUMMARY':summary,
    'DISTINCT_SUMMARY_VIDEO_SECTION_IF_NEEDED':roadmap,
    'EXAM_SECTION_TITLE':'중심력과 위성 궤도를 설명하는 영어 답안',
    'BILINGUAL_GLOSSARY_TABLE':table(['영어(한국어)','의미와 사용'],[(f'{en}({ko})',escape(meaning)) for en,ko,meaning in terms]),
    'AUDIT_SECTION_TITLE':'원본 슬라이드·자동생성 스크립트 교정 기록',
    'ASR_CORRECTION_TABLE':p('원본 PDF와 영어 자동생성 스크립트는 그대로 보존했습니다. 아래는 본문에 채택한 해석과 검산 근거입니다. 스크립트의 잘못된 단어가 실제 발화인지 자동인식 오류인지는 음성을 별도로 판독하지 않은 경우 단정하지 않습니다.')+table(['위치','원문 또는 문제','본문 처리','근거'],audit),
    'SOURCE_LIST_AND_PROVENANCE_NOTE':'<ul class="plain-list"><li>원본 PDF: Lecture 5, MC2103, Fall 2026, 50장.</li>'+''.join(f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상</a> · 영어 자동생성 스크립트, 2026-09-20 확보.</li>' for label,vid in videos)+'<li>주차·날짜: Teams에서 보존한 강의 인덱스, Week 04 · 2026-09-23.</li></ul>'+p('영상 5개의 영어 원문 자막을 전부 확인했습니다. 타임스탬프는 관련 설명 구간이며 정확한 슬라이드 전환 시각을 뜻하지 않습니다. Overview는 단원 도입, Contents 1·2는 개념 설명, Problem Solving은 두 예제, Summary 앞부분은 실제 개념 복습입니다. Summary 후반의 다음 단원 예고는 독립된 섹션으로 분리했습니다.')+p('μ = GM 표기, 생략된 미분·기하학 유도, 초기조건의 적용 범위, 수치 검산과 원본 조건의 일관성 검토는 시험용 보강 또는 편집자 보강으로 명시했습니다. 원본의 ε, h 및 지수 오탈자는 해당 슬라이드 바로 아래와 교정 기록에 함께 표시했습니다. 계산에는 원본의 g = 9.81 m/s²와 R = 6370 km를 사용하고 중간 반올림을 최소화했습니다.'),
    'TABLE_OF_CONTENTS_LINKS':''.join(f'<li><a href="#{id}">{label}</a></li>' for id,label in toc),
}
for key, value in values.items():
    template = template.replace('{{'+key+'}}', value)
template = template.replace('이 부분만 읽어도 렉처의 핵심 정의, 개념 관계, 가정과 풀이 흐름을 이해할 수 있도록 작성합니다.', '중심력의 정의에서 각운동량 보존, 궤도 방정식, 탈출 속력과 주기, 두 예제까지 연결한 독립형 요약입니다. 원본 슬라이드와 본강의·Summary의 개념 복습을 종합했으며, 상세 유도는 아래 슬라이드별 설명에서 이어집니다.')
template = re.sub(r'\s*<!--[\s\S]*?-->', '', template)
template = '\n'.join(line.rstrip() for line in template.splitlines())+'\n'
assert not re.search(r'\{\{[^}]+\}\}', template)
(SITE/'lecture05.html').write_text(template, encoding='utf-8')
print(f'BUILT lecture05.html: {len(records)} source sections, {len(exam_items)} exam cards, {len(terms)} terms')
