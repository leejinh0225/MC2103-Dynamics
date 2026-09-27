"""Populate the fixed Lecture 1 template with reviewed Lecture 6 sources."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
records = []

def p(text):
    if text.startswith('<table'):
        return text
    return '<p>' + text + '</p>'

def card(title, *body, kind='card'):
    return f'<div class="{kind}"><h3>{title}</h3>' + ''.join(p(x) for x in body) + '</div>'

def formula(text):
    return '<span class="formula">' + text + '</span>'

def table(headers, rows):
    return '<table class="term-table"><thead><tr>' + ''.join('<th>'+x+'</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows) + '</tbody></table>'

def add(n, title, evidence, *body, eq='', extra='', correction='', role='Concept'):
    assert n == len(records) + 1, (n, len(records))
    blocks = card('원본 교정 · 적용 조건', correction, kind='callout') if correction else ''
    blocks += card('핵심 해설' if role == 'Concept' else '슬라이드 안내', *body, kind='card' if role == 'Concept' else 'quiet-card')
    if eq:
        blocks += card('식과 기호', formula(eq))
    records.append((title, evidence, blocks + extra, role))

summary = ''.join([
    card('1. 시간 대신 이동 전후의 상태를 연결합니다.',
         'Work–energy principle(일·에너지 원리)은 force(힘)가 displacement(변위)를 따라 한 work(일)를 kinetic energy(운동에너지)의 변화와 연결합니다. Constant mass(일정 질량)의 particle(입자)에 대해 T₁ + ΣU₁→₂ = T₂, T = ½mv²입니다. U는 work(일), T는 kinetic energy(운동에너지), m은 mass(질량), v는 speed(속력)입니다. 이 강의에서는 potential energy(위치에너지)를 U가 아니라 V로 씁니다.',
         'Newton’s second law(뉴턴 제2법칙) ΣFₜ = maₜ에 aₜ = v dv/ds를 대입하고 이동 경로를 따라 적분하면 얻는 식입니다. 따라서 새로운 독립 법칙이 아니라 같은 운동방정식의 적분형입니다. Time(시간)이나 acceleration(가속도)의 중간 이력 없이 두 위치의 speed(속력)를 연결하기에 편리합니다. Vector direction(벡터 방향)과 zero-work reaction(일을 하지 않는 반력)은 이 스칼라 식 하나로 정해지지 않습니다.',kind='callout'),
    card('2. 일의 부호는 힘의 크기가 아니라 변위와의 내적으로 정합니다.',
         '미소 work(일)는 dU = <b>F</b>·d<b>r</b> = F cosα ds입니다. α는 force(힘)와 displacement(변위)의 끼인각, ds는 경로를 따라 이동한 미소 거리입니다. Acute angle(예각)이면 positive work(양의 일), obtuse angle(둔각)이면 negative work(음의 일), perpendicular(수직)이면 zero work(0인 일)입니다. Work(일)는 방향 없는 scalar(스칼라)이지만 부호는 있습니다. 단위는 J = N·m입니다.',
         'Finite displacement(유한 변위)에서는 U₁→₂ = ∫<b>F</b>·d<b>r</b> = ∫Fₜ ds입니다. Fₜ는 signed tangential component(부호 있는 접선 성분)입니다. Constant force(일정한 힘)라면 F·Δr로 줄어들지만 variable force(변하는 힘)는 적분해야 합니다. Fₜ–s 그래프의 signed area(부호 있는 면적)가 work(일)입니다.'),
    card('3. 자주 쓰는 일의 식은 적용 조건과 함께 기억합니다.',
         table(['Force(힘)','Work(일)','조건과 부호'],[
             ('Constant force(일정한 힘)','F cosα Δx','직선 방향과 α가 일정한 경우'),
             ('Weight(중량)','mg(y₁−y₂)','g 일정, y 위쪽 양수; 하강 시 양수'),
             ('Linear spring force(선형 스프링 힘)','½k(x₁²−x₂²)','x는 natural length(자연길이)에서 잰 변형량'),
             ('Inverse-square gravity(역제곱 중력)','GMm(1/r₂−1/r₁)','r은 중심 간 거리; 멀어지면 음수'),
             ('Kinetic friction(운동마찰)','−∫μₖN ds','고정 표면을 따라 미끄러질 때; N 일정이면 −μₖNL'),
         ]),
         'Spring force(스프링 힘)의 일은 스프링이 더 변형되면 negative(음), natural length(자연길이)에 가까워지면 positive(양)입니다. 일반 기준은 x₂² &lt; x₁²일 때 양수이며, x₂ &lt; x₁만으로는 압축 상태까지 판정할 수 없습니다. Fixed smooth surface(고정된 매끈한 표면)의 normal force(수직항력), fixed-length cord(길이가 일정한 줄)의 pendulum tension(진자 장력)은 해당 변위와 수직이라 일하지 않습니다. 그렇다고 그 힘이 0이라는 뜻은 아닙니다. 마찰의 고정 표면 조건과 부호 일반화는 편집자 보강입니다.'),
    card('4. 위치에너지는 보존력이 하는 일을 두 상태의 차로 바꾼 것입니다.',
         'Conservative force(보존력)는 work(일)가 path-independent(경로에 무관)하여 시작점과 끝점으로만 정해지는 힘입니다. U₁→₂ = V₁−V₂ = −ΔV이며, closed path(닫힌 경로)를 한 바퀴 돌면 ∮<b>F</b>·d<b>r</b> = 0입니다. Potential energy(위치에너지)가 감소한 만큼 그 보존력이 positive work(양의 일)를 합니다. Kinetic friction(운동마찰)은 왕복해도 에너지를 회복시키지 않으므로 이 형태의 위치에너지로 대신할 수 없습니다.',
         'Uniform gravity(균일 중력)는 Vg = mgy, linear spring(선형 스프링)은 Ve = ½kx², inverse-square gravity(역제곱 중력)는 Vg = −GMm/r입니다. 마지막 식은 Vg(∞)=0을 기준으로 합니다. mgy의 datum(기준 높이)은 임의로 정할 수 있지만 한 문제 안에서는 일관되어야 합니다. Spring deformation(스프링 변형량) x는 기준 높이처럼 임의로 바꿀 수 없고 반드시 실제 길이−자연길이로 구합니다.'),
    card('5. 일·에너지 원리와 역학적 에너지 보존을 구분합니다.',
         '일하는 힘이 conservative(보존적)이고 나머지 constraint force(구속력)의 일이 0이면 T₁+V₁ = T₂+V₂입니다. Mechanical energy(역학적 에너지) E=T+V가 constant(일정)하지만 kinetic energy(운동에너지)와 potential energy(위치에너지)는 서로 바뀔 수 있습니다. 진자가 내려오면서 빨라지는 것은 V 감소와 T 증가의 교환입니다.',
         '시험용 보강: Nonconservative work(비보존력이 한 일) Uₙc까지 있으면 T₁+V₁+Uₙc = T₂+V₂로 씁니다. 이미 V에 넣은 gravity(중력)나 spring force(스프링 힘)의 work(일)를 Uₙc에 다시 넣으면 double counting(이중 계산)입니다. 고정 거친 표면의 kinetic friction(운동마찰)은 mechanical energy(역학적 에너지)를 thermal energy(열에너지)로 바꾸지만 에너지 자체를 없애지는 않습니다. 외부 에너지 전달까지 고려한 전체 수지를 구별합니다.'),
    card('6. 일률은 에너지의 양이 아니라 전달 속도입니다.',
         'Power(일률) ℘ = dU/dt = <b>F</b>·<b>v</b>이며 단위는 W = J/s입니다. 같은 work(일)를 더 짧은 시간에 하면 average power(평균 일률)가 큽니다. Mechanical efficiency(기계 효율) η = useful output work/input work이며 정상적인 동일 운전 조건에서는 output power/input power로도 구합니다. η는 무차원이고 퍼센트로도 씁니다.',
         '시험용 보강: η = 0.8이고 필요한 output power(출력 일률)가 2 kW라면 input power(입력 일률)는 2/0.8 = 2.5 kW입니다. 여기의 W 단위는 watt(와트), 다른 식의 W 기호는 weight(중량)이므로 문맥을 구별합니다. 원본의 1 hp ≈ 746 W를 사용합니다.'),
    card('7. 속력은 에너지로 구하고, 반력과 접촉 조건은 운동방정식으로 구합니다.',
         '수평 위치에서 released from rest(정지 상태에서 놓인) 길이 l의 pendulum(진자)은 바닥까지 높이 l을 잃으므로 v²=2gl입니다. 바닥의 inward normal direction(안쪽 법선 방향)에 Newton’s second law(뉴턴 제2법칙)를 쓰면 P−mg=mv²/l이므로 tension(장력) P=3mg입니다. 장력이 일하지 않아도 중량의 세 배가 될 수 있습니다.',
         'Roller coaster(롤러코스터) 예제에서 12 m 아래의 골짜기는 v₂≈15.34 m/s, N₂=mg+mv₂²/ρ₂=49.05 kN입니다. 7.5 m 아래의 봉우리에서는 v₃≈12.13 m/s, N₃=mg−mv₃²/ρ₃입니다. Contact maintained(접촉 유지) 조건 N₃≥0으로 ρ₃≥15 m를 얻습니다. 15 m는 N₃=0의 이론적 경계이며, 실제 설계 안전성을 보증하는 값이 아닙니다.'),
    card('8. 연결된 물체는 구속관계를 먼저 정하고 합산합니다.',
         'Inextensible cable(늘어나지 않는 케이블)과 ideal fixed pulley(이상적인 고정 도르래)로 연결된 예제 1에서는 두 블록의 displacement magnitude(변위 크기)와 speed(속력)가 같습니다. A의 tension work(장력이 한 일)는 +F꜀s, B에서는 −F꜀s이므로 두 식을 합하면 상쇄됩니다. 두 블록의 kinetic energy(운동에너지)는 둘 다 포함해야 합니다.',
         'A=200 kg, B=300 kg, μₖ=0.25, s=2 m일 때 (mBg−μₖmAg)s = ½(mA+mB)v²입니다. 중간 반올림 없이 순일은 4905 J, v≈4.43 m/s입니다. Internal forces(내력)라는 이유만으로 언제나 일이 상쇄되는 것은 아닙니다. 이 문제의 동일 장력·동일 이동거리라는 조건이 필요합니다. 이 조건 설명은 편집자 보강입니다.'),
    card('9. 스프링 문제의 핵심은 총 변형량과 실제 접촉 구간입니다.',
         '예제 2는 60 kg package(포장물)가 2.5 m/s로 출발하여 0.600 m를 간 뒤, 이미 0.120 m compressed(압축된) 스프링을 추가로 0.040 m 압축합니다. 따라서 총 압축량은 0.160 m, 마찰 이동거리는 0.640 m입니다. k=20000 N/m이므로 spring work(스프링이 한 일)는 −½k(0.160²−0.120²)=−112 J입니다.',
         'Maximum compression(최대 압축)에서 v=0이므로 187.5−μₖ(60)(9.81)(0.640)−112=0, μₖ≈0.2004입니다. Rebound(되튐)에서는 spring work(스프링이 한 일)가 +112 J, friction work(마찰이 한 일)는 여전히 −75.5 J입니다. 출발 위치로 돌아왔을 때 T=36.5 J, speed(속력)≈1.103 m/s이며 방향은 왼쪽입니다. 스프링은 원래의 사전 압축 상태로 돌아가며, 저장 에너지 전부가 아니라 추가로 저장된 112 J를 돌려줍니다.'),
    card('10. 사선 스프링은 실제 길이를 기하학으로 구합니다.',
         '예제 4의 10 kg collar(칼라)는 frictionless vertical rod(마찰 없는 수직 봉)를 따라 0.150 m 내려옵니다. 수평 간격은 0.200 m, natural length(자연길이)는 0.100 m입니다. 초기 변형량은 x₁=0.100 m, 최종 스프링 길이는 √(0.200²+0.150²)=0.250 m이므로 x₂=0.150 m입니다.',
         '초기 높이를 datum(기준 높이)으로 두면 V₁=1 J, V₂=½(200)(0.150²)+(10)(9.81)(−0.150)=−12.465 J입니다. T₁=0이므로 1=5v₂²−12.465, v₂≈1.641 m/s downward(아래쪽)입니다. Negative potential energy(음의 위치에너지)는 기준보다 낮다는 뜻일 수 있으며 계산 오류가 아닙니다.'),
    card('11. 중력 궤도에서는 에너지와 각운동량을 함께 보존합니다.',
         'Conservative central force(보존 중심력)인 중력만 작용하면 specific mechanical energy(단위 질량당 역학적 에너지) ε=½v²−μ/r와 specific angular momentum(단위 질량당 각운동량) h=rv sinφ가 일정합니다. 여기서 μ=GM, φ는 outward radial vector(바깥쪽 반지름벡터)와 velocity(속도)의 끼인각입니다. ε 표기는 편집자 보강이며 지난 렉처의 eccentricity(이심률)와 다른 기호 용도입니다.',
         '예제 5는 r₀=(6370+500) km, v₀=36900 km/h=10250 m/s입니다. 수평 발사에서는 h=r₀v₀이고 apogee(원지점)에서도 φ=90°이므로 r₀v₀=rₐvₐ입니다. 에너지 식과 합치면 rₐ=r₀/[2μ/(r₀v₀²)−1]을 얻습니다. μ=gR²로 끝까지 계산한 maximum altitude(최대고도)는 약 60333 km입니다. 원본 반올림 답은 약 60400 km입니다.',
         'Launch-angle error(발사각 오차) 한계에서는 rmin=(6370+200) km를 두고 에너지로 vmax를 구한 뒤 sinφ₀=rmin vmax/(r₀v₀)를 씁니다. 계산하면 sinφ₀≈0.980119, 수평 기준 허용 오차는 약 ±11.44°입니다. 원본은 ±11.5°로 제시하므로 원본 답과 검산값을 구분합니다. Radius(중심 거리)에 altitude(고도)만 대입하면 안 됩니다.'),
    card('12. 풀이 순서는 계·기준점·일의 분류·검산입니다.',
         '먼저 system(계)과 initial/final states(처음·나중 상태)를 정합니다. Free-body diagram(자유물체도)로 모든 force(힘)를 확인하고 cable constraint(케이블 구속조건), spring deformation(스프링 변형량), height change(높이 변화)를 구합니다. 다음으로 모든 힘의 일을 직접 넣을지, conservative work(보존력이 한 일)를 V로 바꿀지 정합니다.',
         '마찰이 있으면 이동 방향이 바뀌는 구간을 분리하고, normal force(수직항력)가 constant(일정)인지 확인합니다. 속력을 구한 뒤 force(힘)나 contact condition(접촉 조건)이 필요하면 Newton’s second law(뉴턴 제2법칙)를 추가합니다. 마지막으로 단위, 일의 부호, v²≥0, 스프링의 실제 길이, 궤도의 중심 거리를 검산합니다. 이 풀이 순서는 원본 예제들을 종합한 시험용 보강입니다.'),
])

add(1,'Lecture 6 · 일과 에너지 원리','강의 인덱스 · Week 05 · 2026-09-30',
    'Work and Energy Principle(일과 에너지 원리)를 다루는 강의 표지입니다. 앞선 force–acceleration(힘–가속도) 해석을 force–displacement(힘–변위)의 적분 관계로 확장합니다.',role='Title')
add(2,'Lecture 6-1 · 도입','Overview 00:17–00:59',
    'Overview(도입 영상)는 자전거에 일을 가하면 에너지가 변한다는 예와 skid mark(타이어 미끄럼 자국)의 길이로 braking speed(제동 시작 속력)를 추정할 수 있는지라는 질문을 제시합니다. 핵심은 force(힘)·distance(거리)·speed(속력)의 연결입니다.',role='Divider')
add(3,'원본에 수록된 보조 영상 링크','원본 PDF의 링크 슬라이드',
    '원본 링크: <a href="https://youtu.be/AfJnrI3myhk" target="_blank" rel="noreferrer">슬라이드 3의 보조 영상 열기</a>. 현재 강의 인덱스의 본강의 5편과는 별도 링크이며, 이 영상의 내용을 본문 근거로 사용하지 않았습니다.',role='Video link')
add(4,'Lecture 6-2 · 일과 운동에너지','Contents 1',
    '이후 슬라이드는 work(일)의 정의와 각 힘의 일을 다룬 뒤 work–energy principle(일·에너지 원리)을 유도합니다.',role='Divider')
add(5,'내려오는 롤러코스터의 에너지 전환','Contents 1 00:17–00:26',
    'Roller coaster(롤러코스터)가 내려오면 gravitational potential energy(중력 위치에너지)가 줄어들고 kinetic energy(운동에너지)가 증가할 수 있습니다. 사진은 height(높이)와 speed(속력)가 연결된다는 출발점입니다.',
    'Friction(마찰)과 air resistance(공기저항)를 neglect(무시)하는 모델에서는 줄어든 위치에너지가 그대로 운동에너지로 바뀝니다. 저항이 있으면 일부는 thermal energy(열에너지)로 전환됩니다. 이 적용 조건 설명은 편집자 보강입니다.')
add(6,'충돌은 운동량 방법으로 이어집니다.','Contents 1 00:26–00:47',
    'Impact test(충돌 시험)는 짧은 time interval(시간 구간)에 큰 force(힘)가 작용하는 예입니다. 다음 단원의 impulse–momentum method(충격량·운동량 방법)가 유용한 상황으로 소개됩니다.',
    '이번 Lecture 6의 계산 중심은 work–energy(일·에너지)입니다. 사진의 파괴 과정 전체에 mechanical energy conservation(역학적 에너지 보존)을 곧바로 적용한다는 뜻은 아닙니다.')
add(7,'출발점은 여전히 뉴턴 제2법칙입니다.','Contents 1 00:35–01:07',
    'Particle(입자)의 운동은 resultant force(합력)와 mass(질량), acceleration(가속도)의 관계로 설명했습니다. Work–energy principle(일·에너지 원리)은 이 관계를 버리는 것이 아니라 적분하여 다른 미지수에 맞게 사용하는 방법입니다.',eq='Σ<b>F</b> = m<b>a</b>')
add(8,'변위로 적분할지, 시간으로 적분할지 선택합니다.','Contents 1 01:07–01:43',
    'Work–energy method(일·에너지 방법)는 force(힘)·mass(질량)·velocity(속도)·displacement(변위)를 연결합니다. Impulse–momentum method(충격량·운동량 방법)는 같은 힘을 time(시간)에 대해 적분하여 velocity(속도) 변화와 연결합니다.',
    '두 방법은 서로 모순되는 규칙이 아닙니다. 주어진 데이터가 이동거리인지, 작용시간인지에 따라 편한 적분형이 달라집니다. Impulse(충격량)의 상세 해석은 다음 렉처에서 다룹니다.')
add(9,'문제의 미지수에 맞는 원리를 고릅니다.','Contents 1 01:43–02:16',
    'Force(힘)나 acceleration(가속도)가 직접 미지수이면 Newton’s second law(뉴턴 제2법칙), 두 위치에서의 speed(속력)를 연결하면 work–energy(일·에너지), force–time data(힘–시간 자료)가 주어지면 impulse–momentum(충격량·운동량)을 우선 검토합니다.',
    '이 구분은 배타적인 선택이 아닙니다. 진자 장력과 곡선 트랙의 normal force(수직항력)는 energy(에너지)로 speed(속력)를 구한 뒤 Newton’s second law(뉴턴 제2법칙)를 함께 사용합니다.',eq='T₁ + ΣU₁→₂ = T₂')
add(10,'일은 힘과 미소 변위의 내적입니다.','Contents 1 02:16–03:58',
    'Position vector(위치벡터) <b>r</b> 자체가 아니라 infinitesimal displacement(미소 변위) d<b>r</b>와 force(힘)를 dot product(내적)합니다. ds=|d<b>r</b>|이고 α는 두 벡터의 끼인각입니다. 이동 방향으로 투영한 force component(힘 성분)만 work(일)에 기여합니다.',
    '직교 좌표에서는 x·y·z 방향의 각 force component(힘 성분)와 해당 signed displacement(부호 있는 변위)를 곱하여 더합니다. 힘이 크더라도 변위와 perpendicular(수직)이면 이 내적은 0입니다.',eq='dU = <b>F</b>·d<b>r</b> = F cosα ds<br>= Fₓ dx + Fᵧ dy + Fz dz')
add(11,'일은 부호 있는 스칼라입니다.','Contents 1 03:58–04:30',
    'Work(일)는 scalar quantity(스칼라량)입니다. Vector direction(벡터 방향)은 없지만 positive/negative(양/음)의 sign(부호)은 있습니다. 양의 일은 그 힘이 운동에너지를 증가시키는 쪽으로 기여하고, 음의 일은 감소시키는 쪽으로 기여한다는 뜻입니다.',
    'SI unit(SI 단위)는 joule(줄), J입니다. N·m은 torque(토크)의 단위 차원과 같지만 work(일)는 내적, torque(토크)는 외적이므로 같은 물리량은 아닙니다. 이 비교는 시험용 보강입니다.',eq='1 J = 1 N·m = 1 kg·m²/s²')
add(12,'유한한 이동에서는 경로 전체를 적분합니다.','Contents 1 04:30–06:15',
    '각 미소 구간의 work(일)를 더한 것이 line integral(선적분)입니다. F의 magnitude(크기)나 α가 위치에 따라 달라져도 같은 정의를 사용합니다. Fₜ=F cosα는 signed tangential force(부호 있는 접선력)입니다.',
    '일반적인 force field(힘의 장)에서 work(일)는 endpoint displacement(끝점 사이 변위)만으로 계산되지 않습니다. 실제 path(경로)를 따라 ∫Fₜ ds를 계산해야 합니다. 뒤의 conservative force(보존력)는 특별히 경로 의존성이 없는 경우입니다.',eq='U₁→₂ = ∫₁² <b>F</b>·d<b>r</b><br>= ∫ₛ₁ˢ² Fₜ ds')
add(13,'접선력–거리 그래프의 면적이 일입니다.','Contents 1 06:15–06:41',
    '가로축 s는 path coordinate(경로 좌표), 세로축 Fₜ는 tangential component(접선 성분)입니다. 두 위치 사이 곡선 아래 signed area(부호 있는 면적)가 work(일)입니다. 곡선이 축 아래에 있으면 해당 부분은 negative work(음의 일)로 더합니다.',
    '시험용 보강: 직사각형이면 constant force(일정한 힘), 삼각형·사다리꼴이면 linearly varying force(선형으로 변하는 힘)의 적분을 면적으로 계산할 수 있습니다. 힘의 전체 크기 F가 아니라 Fₜ를 그린 그래프인지 먼저 확인합니다.')
add(14,'일정한 힘의 직선 이동: 투영 성분을 사용합니다.','Contents 1 06:41–08:18',
    'A₁에서 A₂로의 rectilinear motion(직선운동)에서 force(힘)가 x축과 α를 이룹니다. 실제로 일을 하는 성분은 F cosα이며, 이동량은 Δx입니다. 따라서 정답은 b입니다.',eq='U₁→₂ = (F cosα)Δx')
add(15,'정답 b: 수직 성분은 일을 하지 않습니다.','Contents 1 08:18–08:26',
    '원본의 정답 표시를 보존했습니다. F sinα는 경로에 perpendicular(수직)이므로 work(일)에 기여하지 않습니다. FΔx는 α=0일 때만 맞고, work(일)가 0이 되는 것은 α=90° 또는 변위가 0인 경우입니다.')
add(16,'중량이 한 일은 높이 변화로 계산합니다.','Contents 1 08:26–09:40',
    'y축을 upward positive(위쪽 양수)로 잡으면 weight(중량)는 Fᵧ=−W=−mg입니다. 따라서 dU=−Wdy이고, constant gravity(일정 중력)에서는 U₁→₂=−W(y₂−y₁)입니다. 경로가 굽어도 중력의 x·z 성분이 없어서 vertical displacement(수직 변위)만 필요합니다.',
    'Upward motion(상승 운동)은 Δy&gt;0이므로 negative work(음의 일), downward motion(하강 운동)은 Δy&lt;0이므로 positive work(양의 일)입니다. 곡선의 전체 길이를 W에 곱하지 않습니다.',eq='Ug = W(y₁−y₂) = mg(y₁−y₂)')
add(17,'높은 곳에서 낮은 곳으로 이동하면 중력은 양의 일을 합니다.','Contents 1 09:40–10:50',
    '그림의 y₂가 y₁보다 높습니다. Moving from y₂ to y₁(y₂에서 y₁로 이동)하는 b의 경우 weight(중량)와 하강 변위의 수직 성분이 같은 방향이므로 positive work(양의 일)입니다.')
add(18,'정답 b: 시작점과 끝점의 순서를 확인합니다.','Contents 1 10:50–11:04',
    '이 장은 앞 문제의 정답 공개입니다. Work by weight(중량이 한 일)는 W×낙하 높이이므로 위에서 아래로 이동할 때 양수입니다. 같은 두 지점을 반대로 이동하면 부호만 반대가 됩니다.')
add(19,'스프링의 힘은 자연길이에서의 변형에 비례합니다.','Contents 1 11:04–13:20',
    'Linear spring(선형 스프링)의 restoring force(복원력)는 signed deformation(부호 있는 변형량) x에 대해 Fₓ=−kx입니다. k는 spring constant(스프링 상수), 단위는 N/m입니다. x=0은 undeformed position(변형되지 않은 위치)입니다.',
    '원본처럼 오른쪽으로 stretched(늘어난) 스프링은 물체를 왼쪽으로 당깁니다. 늘어나는 동안 스프링이 물체에 한 work(일)는 음수입니다. 힘이 x에 따라 달라지므로 끝점의 힘 하나에 이동거리를 곱할 수 없습니다.',eq='Us = −∫ₓ₁ˣ² kx dx<br>= ½kx₁² − ½kx₂²')
add(20,'스프링 일의 식과 그래프는 같은 계산입니다.','Contents 1 13:20–14:04',
    'F=kx 그래프의 slope(기울기)는 k입니다. x₁에서 x₂까지 증가할 때 그래프 아래 면적은 ½k(x₂²−x₁²)이고, 스프링이 물체에 한 work(일)는 그 음수입니다. 그래프가 힘의 크기인지 signed force(부호 있는 힘)인지 구별해야 합니다.')
add(21,'자연길이로 돌아오는 스프링은 양의 일을 합니다.','Contents 1 14:04–14:54',
    'Stretched spring(늘어난 스프링)이 x₁에서 더 작은 양의 x₂로 돌아오면 stored energy(저장 에너지)가 줄고 물체에 positive work(양의 일)를 합니다. 힘이 반대 방향이라서 항상 음의 일이라는 해석은 틀립니다. 비교 대상은 힘과 현재의 이동 방향입니다.',
    correction='원본의 x₂&lt;x₁은 그림처럼 x₁,x₂≥0인 신장 구간의 표현입니다. 압축까지 포함한 일반 조건은 x₂²&lt;x₁², 즉 변형의 절댓값이 감소하는 경우입니다. 예를 들어 −0.1 m에서 −0.2 m로 더 압축되면 x₂&lt;x₁이지만 스프링 일은 음수입니다. 이 일반화는 편집자 보강입니다.')
add(22,'사다리꼴 면적으로 스프링의 일을 계산합니다.','Contents 1 14:54–15:30',
    '선형 스프링은 두 끝점의 force magnitude(힘의 크기) 평균과 변형 증가량의 곱으로 면적을 구할 수 있습니다. F₁=kx₁, F₂=kx₂, Δx=x₂−x₁이면 아래 식이 적분과 같습니다. 원본 그림은 양의 신장량이 증가하는 경우입니다.',eq='Us = −½(F₁+F₂)Δx<br>= −½k(x₁+x₂)(x₂−x₁)')
add(23,'변형량의 방향과 이동 방향은 같지 않을 수 있습니다.','Contents 1 15:30–15:42',
    'A₀는 natural position(자연 상태 위치), A₁·A₂는 stretched positions(늘어난 위치)입니다. 그림의 spring force(스프링 힘)는 왼쪽이지만 물체가 항상 오른쪽으로 움직여야 하는 것은 아닙니다. 늘릴 때와 돌아올 때를 나누어 force–displacement angle(힘–변위 끼인각)을 판단합니다.')
add(24,'A₀에서 A₁: 스프링을 늘리는 구간','Contents 1 15:42–16:24',
    'Displacement(변위)는 오른쪽, spring force(스프링 힘)는 왼쪽입니다. 따라서 스프링이 블록에 한 work(일)는 negative(음)입니다. 블록이 스프링에 한 일과 주체를 바꾸어 생각하지 않습니다.',eq='U₀→₁ = −½kx₁²')
add(25,'A₀에서 A₁의 정답은 음의 일입니다.','Contents 1 16:24–16:35',
    '정답 b인 negative work(음의 일)를 표시한 원본입니다. 스프링에 elastic potential energy(탄성 위치에너지)가 저장되는 동안, 스프링이 블록에 하는 일은 그 저장량의 음수입니다.')
add(26,'A₂에서 A₀: 스프링이 복원되는 구간','Contents 1 16:35–17:07',
    'Stretched spring(늘어난 스프링)의 힘과 물체의 이동이 모두 왼쪽입니다. 스프링은 물체에 positive work(양의 일)를 하며 stored energy(저장 에너지)를 돌려줍니다.',eq='U₂→₀ = ½kx₂²')
add(27,'A₂에서 A₀의 정답은 양의 일입니다.','Contents 1 17:07–17:23',
    '원본의 정답 a를 보존했습니다. Spring force(스프링 힘)의 방향이 앞 문제와 같아도 displacement(변위)의 방향이 바뀌었으므로 work(일)의 부호가 바뀝니다.')
add(28,'거리에 따라 달라지는 중력의 일','Contents 1 17:23–19:43',
    '질량 M인 중심 천체가 fixed(고정)되어 있고, 질량 m인 입자가 움직입니다. Gravitational force(중력)의 크기는 GMm/r²이며 inward(안쪽)입니다. 따라서 dU=−GMm/r² dr입니다. 여기의 dr은 radial distance change(중심 거리 변화), d<b>r</b>은 전체 미소 변위벡터이므로 구별합니다.',
    '적분하면 출발·도착의 중심 거리만 남습니다. Outward motion(바깥쪽 운동)은 r₂&gt;r₁이므로 negative work(음의 일), inward motion(안쪽 운동)은 positive work(양의 일)입니다. 단순히 식 앞에 음수가 있다는 이유로 항상 음의 일이라고 말할 수 없습니다.',eq='Ug = GMm(1/r₂−1/r₁)')
add(29,'고정 경사면의 수직항력은 일을 하지 않습니다.','Contents 1 19:43–21:28',
    '블록은 B에서 A로 경사면을 따라 이동하지만 normal force(수직항력)는 면에 수직입니다. 두 벡터의 angle(각도)이 90°여서 dot product(내적)가 0입니다. 정답은 b입니다.',eq='UN = ∫<b>N</b>·d<b>r</b> = 0')
add(30,'수직항력이 0이라는 뜻은 아닙니다.','Contents 1 21:28–21:42',
    '정답 NO(아니오)는 work(일)가 없다는 뜻입니다. Normal force(수직항력)는 실제로 존재하며 kinetic friction(운동마찰)의 크기를 정할 수도 있습니다. 편집자 보강: 표면 자체가 움직여 힘의 작용점에 법선 방향 변위가 생기면 이 zero-work(0인 일) 결론을 일반화할 수 없습니다.')
add(31,'같은 경사면에서도 중량은 일을 합니다.','Contents 1 21:42–23:19',
    'Weight(중량)는 수직 아래를 향하고 B→A 변위는 경사면 아래를 향합니다. 두 방향은 정확히 평행하지 않아도 acute angle(예각)을 이루므로 positive work(양의 일)가 있습니다. 경로와 평행한 weight component(중량 성분)만 계산에 들어갑니다.')
add(32,'정답 YES: 수직 낙하 높이가 0이 아닙니다.','Contents 1 23:19–23:29',
    'B와 A의 elevation(높이)이 다르므로 gravity work(중력이 한 일)는 0이 아닙니다. 경사면 이동거리 L, 경사각 θ라면 낙하 높이는 L sinθ이므로 W L sinθ입니다.',eq='Ug = W(yB−yA) = WL sinθ')
add(33,'중력이 한 일의 부호는 양수입니다.','Contents 1 23:29–23:46',
    '질문은 앞 장에서 존재를 확인한 gravity work(중력이 한 일)의 sign(부호)입니다. B→A는 downhill(내리막)이므로 yA&lt;yB이며 W(yB−yA)&gt;0입니다.')
add(34,'정답 positive: 다른 힘의 일과 구별합니다.','Contents 1 23:46–23:56',
    'Positive(양수)는 gravity(중력) 하나가 한 일의 부호입니다. Friction(마찰)이 함께 있다면 그 일도 별도로 더해야 total work(전체 일)를 얻습니다. 중력이 양의 일을 했다고 전체 일이 반드시 양수인 것은 아닙니다.')
add(35,'일을 하지 않는 힘의 두 가지 조건','Contents 1 23:56–24:39',
    '첫째는 point of application(힘의 작용점)의 displacement(변위)가 0인 경우, 둘째는 힘이 그 변위에 perpendicular(수직)인 경우입니다. 고정된 frictionless pin(마찰 없는 핀)의 반력은 첫째, 고정된 smooth surface(매끈한 표면)의 반력과 수평 이동 중 중량은 둘째에 해당합니다.',
    '시험용 보강: 조건은 물체가 움직이는가가 아니라 <em>그 힘의 작용점이 어떻게 움직이는가</em>입니다. Fixed support(고정 지지점)인지 moving support(움직이는 지지점)인지에 따라 결론이 달라집니다.')
add(36,'뉴턴 제2법칙의 접선 성분을 적분형으로 바꿉니다.','Contents 1 24:39–28:28',
    'Normal component(법선 성분)는 순간 변위에 수직이므로 work(일)에 직접 기여하지 않습니다. Tangential component(접선 성분)에 대해 ΣFₜ=maₜ이고, chain rule(연쇄법칙)로 aₜ=dv/dt=(dv/ds)(ds/dt)=v dv/ds입니다.',
    '양변에 ds를 곱하면 ΣFₜ ds=mv dv입니다. 왼쪽은 미소 total work(전체 일), 오른쪽은 speed(속력)의 변화로 표현한 양입니다. Inertial frame(관성계)과 constant mass(일정 질량)를 전제로 합니다. 이 전제 명시는 편집자 보강입니다.',eq='ΣFₜ ds = mv dv')
add(37,'일은 운동에너지의 변화입니다.','Contents 1 28:28–30:22',
    '이동 시작 A₁의 speed(속력) v₁부터 A₂의 v₂까지 적분합니다. ∫v dv의 원시함수는 ½v²이므로 두 끝점의 값을 빼야 합니다. 이 ½mv²를 kinetic energy(운동에너지) T로 정의하면 일·에너지 원리를 얻습니다.',
    '여러 force(힘)가 있으면 각 힘의 work(일)를 합합니다. T≥0이지만 ΔT는 negative(음)일 수 있으므로 감속 상황에서도 식은 그대로 성립합니다.',eq='ΣU₁→₂ = ½mv₂² − ½mv₁²<br>T₁ + ΣU₁→₂ = T₂',
    correction='원본 적분 결과의 마지막 항이 ½mv₁²만으로 보입니다. 올바른 정적분 결과는 ½mv₂²−½mv₁²입니다. 같은 슬라이드의 U₁→₂=T₂−T₁ 및 영상 설명과 일치하도록 교정합니다.')
add(38,'운동에너지와 일은 같은 단위를 갖습니다.','Contents 1 30:22–30:45',
    'Kinetic energy(운동에너지) ½mv²의 단위는 kg·m²/s²=J입니다. Work(일)와 차원이 같기 때문에 T₁+ΣU=T₂처럼 직접 더할 수 있습니다.',
    '시험용 보강: km/h로 주어진 speed(속력)는 m/s로 변환한 뒤 제곱합니다. 36 km/h=10 m/s이므로 제곱 항의 단위 변환을 빠뜨리면 에너지 오차가 크게 증폭됩니다.')
add(39,'수평 위치에서 놓은 진자의 조건','Contents 1 30:45–31:27',
    'Bob(진자 추)가 A₁에서 released from rest(정지 상태에서 놓임)이고 cord length(줄 길이)는 l입니다. A₁은 지지점 높이, A₂는 그보다 l만큼 아래입니다. 따라서 v₁=0, 낙하 높이는 l입니다. 힘은 weight(중량) W와 tension(장력) P입니다.',
    correction='원본의 “magnitude and sign but not direction” 문구는 work(일)의 성질을 설명한 문장으로, bob(진자 추)나 velocity(속도)의 정의가 아닙니다. 진자 조건에 대한 설명으로 채택하지 않습니다.')
add(40,'장력을 몰라도 바닥의 속력은 구할 수 있습니다.','Contents 1 31:27–34:13',
    'Fixed-length cord(길이가 일정한 줄)의 tension(장력) P는 경로에 normal(수직)이어서 일을 하지 않습니다. Weight(중량)가 한 일 Wl만 더하면 T₁=0에서 T₂=½(W/g)v₂²로 바뀝니다.',
    'm=W/g를 대입한 뒤 W가 약분되어 v₂=√(2gl)입니다. 같은 l과 initial rest(초기 정지) 조건이면 이상 모델의 바닥 속력은 mass(질량)에 무관합니다.',eq='0 + Wl = ½(W/g)v₂²<br>v₂ = √(2gl)')
add(41,'에너지 방법은 중간 가속도를 건너뜁니다.','Contents 1 34:13–34:54',
    '시시각각 달라지는 acceleration(가속도)를 먼저 구해 시간에 대해 적분할 필요 없이 시작·끝 상태를 연결합니다. Work(일)와 kinetic energy(운동에너지)는 scalar(스칼라)이므로 각 힘의 일을 부호와 함께 더하면 됩니다.',
    'Zero-work force(일을 하지 않는 힘)가 에너지 식에서 사라지는 점이 계산을 단순하게 합니다. 다만 그 힘의 존재 자체가 사라지는 것은 아니며 다음 장처럼 다른 질문에는 다시 필요합니다.')
add(42,'장력과 가속도에는 추가 운동방정식이 필요합니다.','Contents 1 34:54–35:17',
    '진자의 tension(장력)은 에너지 식에서 0의 일을 하므로 그 식에 미지수로 나타나지 않습니다. 따라서 work–energy principle(일·에너지 원리)만으로 P를 직접 결정할 수 없습니다.',
    '먼저 speed(속력)를 구한 다음 normal acceleration(법선 가속도) aₙ=v²/l을 계산하고 ΣFₙ=maₙ을 적용합니다. 이 원리는 곡선 트랙의 normal force(수직항력) 문제에서도 그대로 반복됩니다.')
add(43,'바닥의 장력은 중량의 세 배입니다.','Contents 1 35:17–37:22',
    'A₂에서 center of curvature(곡률중심)는 위쪽입니다. Upward positive(위쪽 양수)로 ΣFₙ=P−W=m v₂²/l입니다. v₂²=2gl과 m=W/g를 넣으면 P=W+2W=3W입니다.',
    'Weight(중량)의 두 배까지만 버티는 줄은 이 이상 모델의 3W 요구량보다 약합니다. 원본의 질문은 정하중만 보고 줄을 선정해서는 안 된다는 의미입니다. 실제 재료·충격·안전계수까지 판단하는 설계 기준은 이 계산에 포함되지 않습니다.',eq='P − W = (W/g)v₂²/l<br>P = 3W',
    correction='원본의 ΣEₙ 표기는 문맥상 ΣFₙ입니다. 자막의 “row times velocity squared”를 ρv²로 읽지 않고, 원본 분수와 단위에 따라 aₙ=v²/ρ로 해석합니다.')

add(44,'Lecture 6-3 · 위치에너지와 보존력','Contents 2',
    'Power(일률)와 efficiency(효율)를 짚은 뒤 potential energy(위치에너지), conservative force(보존력), conservation of mechanical energy(역학적 에너지 보존)로 이어집니다.',role='Divider')
add(45,'일률은 단위 시간당 하는 일입니다.','원본 45 · Contents 2 00:17–00:58',
    'Power(일률)는 work rate(일을 하는 비율), 즉 dU/dt입니다. dU=<b>F</b>·d<b>r</b>를 시간으로 나누면 ℘=<b>F</b>·<b>v</b>입니다. ℘ 기호는 진자 장력 P와 혼동을 피하기 위한 편집 표기입니다.',
    '시험용 보강: Constant power(일정 일률)와 constant force(일정한 힘)는 다릅니다. 힘과 속도가 같은 방향일 때 ℘=Fv이므로, 동일한 힘이어도 speed(속력)가 커지면 instantaneous power(순간 일률)는 커집니다. Average power(평균 일률)는 ΔU/Δt입니다.',eq='℘ = dU/dt = <b>F</b>·<b>v</b>')
add(46,'효율은 유용한 출력과 입력의 비입니다.','Contents 2 00:34–01:43',
    'Power(일률)의 SI 단위는 watt(와트), W=J/s입니다. 원본의 mechanical horsepower(기계적 마력)는 1 hp=550 ft·lbf/s≈746 W입니다. 자막의 “zero per second”와 “what”은 이 맥락에서 joule per second(초당 줄)와 watt(와트)로 읽습니다.',
    'Efficiency(효율) η는 useful output work(유용한 출력 일)를 input work(입력 일)로 나눈 값입니다. 같은 시간 구간의 에너지 전달 또는 정상 운전에서는 output power/input power로 표현합니다. 손실이 있으면 유용한 출력은 입력보다 작습니다.',eq='η = Uout/Uin = ℘out/℘in',
    extra=card('시험용 보강 · 입력을 구할 때 나눕니다.','필요한 output power(출력 일률)를 알아도 전원·엔진의 input power(입력 일률)는 더 큽니다. ℘in=℘out/η이므로 80% 효율을 80이 아닌 0.80으로 대입합니다.'))
add(47,'튀는 공의 높이가 점점 낮아지는 이유','Contents 2 01:43–02:17',
    '공이 떨어지는 동안 gravitational potential energy(중력 위치에너지)가 kinetic energy(운동에너지)로 바뀝니다. 충돌 뒤 다시 올라오면 그 반대 전환이 일어납니다. 사진에서는 되튄 높이가 점점 작아집니다.',
    '편집자 보강: 실제 impact(충돌)에서 변형·열·소리 등으로 mechanical energy(역학적 에너지) 일부가 전환될 수 있어 되돌아오는 운동에너지가 감소합니다. 사진만으로 손실량이나 coefficient of restitution(반발계수)의 수치를 정할 수는 없습니다.')
add(48,'일을 위치에너지 차이로 표현할 수 있는 힘','Contents 2 02:17–05:24',
    '출발점과 도착점이 같다면 어떤 path(경로)를 따라가도 work(일)가 같을 때 V₁−V₂로 쓸 수 있습니다. Weight(중량)와 ideal spring force(이상적 스프링 힘)는 이 성질이 있습니다. Kinetic friction(운동마찰)은 path length(경로 길이)에 따라 소모량이 달라집니다.',
    '원본 표의 normal force(수직항력)는 고정된 매끈한 면을 따르는 운동에서 work(일)가 0이어서 별도의 위치에너지 항으로 모델링하지 않는 경우입니다. “일이 0인 모든 힘은 비보존력”이라는 일반 정의로 확장하지 않습니다.')
add(49,'보존력 분류표의 답과 적용 범위','Contents 2 05:24–06:21',
    '원본의 선택은 Weight(중량): Yes, Friction(마찰): No, Normal force(수직항력): No, Spring force(스프링 힘): Yes입니다. 이 장에서는 중력·스프링에 대해 potential energy(위치에너지)를 정의하고, 이상 구속 반력의 일은 0으로 제외합니다.',
    '편집자 보강: 접촉 조건에 따라 달라지는 normal reaction(법선 반력)은 일반적인 position-only force field(위치만의 힘의 장)와 다릅니다. 표를 외우기보다 실제 work(일)가 0인지, 경로에 무관한 상태함수 V를 정의할 수 있는지를 나누어 판단합니다.')
add(50,'균일 중력의 위치에너지는 mgy입니다.','Contents 2 06:21–09:11',
    'Weight(중량)가 일정할 때 U₁→₂=W y₁−W y₂입니다. 각 위치에서 Vg=Wy=mgy라고 정의하면 Ug=(Vg)₁−(Vg)₂로 간단히 쓸 수 있습니다. y는 선택한 datum(기준 높이)에서 위쪽으로 잰 elevation(높이)입니다.',
    '낮은 곳에서 높은 곳으로 가면 Vg가 증가하지만 gravity(중력)가 한 일은 음수입니다. Work by gravity(중력이 한 일)와 work against gravity(중력에 대항하여 한 일)를 구별해야 부호가 뒤집히지 않습니다.',eq='Vg = mgy<br>Ug = −ΔVg')
add(51,'기준 높이는 임의지만 상태마다 바꾸면 안 됩니다.','Contents 2 09:11–10:06',
    'Datum(기준 높이)을 지면으로 두어도, 출발점으로 두어도 potential energy difference(위치에너지 차이)는 같습니다. y를 모두 같은 상수만큼 이동시키면 V₁과 V₂에 같은 상수가 더해져 에너지 식에서 상쇄됩니다.',
    '시험용 보강: 바닥을 기준으로 계산할 때와 출발점을 기준으로 계산할 때 최종 speed(속력)가 달라진다면 datum(기준 높이)을 중간에 혼용했는지 확인합니다. Vg&lt;0인 상태 자체는 물리적으로 허용됩니다.',eq='Vg = Wy · 단위 J')
add(52,'큰 고도 변화에는 mgy를 그대로 쓰지 않습니다.','Contents 2 10:06–10:49',
    'Vg=mgy는 weight(중량)를 constant(일정)하게 볼 수 있는 근지표 모델입니다. Space vehicle(우주 비행체)의 r이 크게 달라지면 gravitational force(중력)가 1/r²에 따라 변하므로 그 변화까지 적분해야 합니다.',
    'Altitude(고도) z와 radius from Earth’s center(지구 중심 거리) r는 r=R+z로 연결됩니다. 다음 식의 r에 고도만 대입하면 중력을 지나치게 크게 계산합니다.')
add(53,'무한대를 기준으로 한 중력 위치에너지','Contents 2 10:49–13:45',
    'Ug=GMm/r₂−GMm/r₁을 V₁−V₂ 순서로 읽으면 Vg=−GMm/r입니다. Reference level(기준)은 r→∞에서 Vg→0이 되도록 정한 것입니다. 따라서 유한한 r에서는 Vg가 negative(음)입니다.',
    '원본의 W는 현재 높이에서의 weight(중량)가 아니라 surface weight(지표 중량)입니다. W=GMm/R²이므로 GMm=WR²이고 Vg=−WR²/r로도 표현합니다. R은 Earth radius(지구 반지름)입니다.',eq='Vg = −GMm/r = −WR²/r')
add(54,'스프링의 일도 두 상태의 차입니다.','Contents 2 13:45–15:21',
    'Us=½kx₁²−½kx₂²는 중간에 얼마나 복잡하게 움직였는지가 아니라 initial/final deformation(초기·최종 변형량)에만 의존합니다. 이 성질 때문에 ideal linear spring(이상적 선형 스프링)은 conservative(보존적)입니다.',
    '편집자 보강: 이 식은 hysteresis(이력 손실)나 damping(감쇠)이 없는 스프링 모델입니다. 실제 부품의 모든 손실을 자동으로 포함한 식은 아닙니다.',eq='Us = (Ve)₁−(Ve)₂')
add(55,'스프링 변형량의 기준은 자연길이입니다.','Contents 2 15:21–16:03',
    'Elastic potential energy(탄성 위치에너지)는 Ve=½kx²입니다. x=L−L₀에서 L은 실제 길이, L₀는 undeformed length(변형되지 않은 길이)입니다. Extension(신장)과 compression(압축) 모두 x²를 쓰므로 Ve≥0입니다.',
    'Preloaded spring(사전 하중을 받은 스프링)이 이미 x₀만큼 압축되어 있으면 추가 이동 Δx에 대해 최종 변형량은 x₀+Δx입니다. Energy increase(에너지 증가)는 ½k[(x₀+Δx)²−x₀²]이며 ½k(Δx)²가 아닙니다. 이는 뒤 예제 2를 이해하기 위한 시험용 보강입니다.',eq='Ve = ½kx², x = L−L₀')
add(56,'보존력의 정의는 경로 독립성입니다.','Contents 2 16:03–16:42',
    'Conservative force(보존력)는 point of application(작용점)이 어떤 path(경로)를 따라가도 work(일)가 두 끝점의 위치만으로 정해지는 힘입니다. 그러면 potential energy function(위치에너지 함수) V(x,y,z)를 정의할 수 있습니다.',
    'Work(일)는 이동 과정에서 전달되는 양이고, potential energy(위치에너지)는 상태에 배정한 양입니다. 둘을 같은 기호나 같은 물리적 의미로 혼용하지 않습니다.',eq='U₁→₂ = V(x₁,y₁,z₁) − V(x₂,y₂,z₂)')
add(57,'닫힌 경로에서 보존력이 한 일은 0입니다.','Contents 2 16:42–17:01',
    'Closed path(닫힌 경로)는 출발점과 도착점이 같은 경로입니다. Conservative force(보존력)에 대해 U=Vstart−Vend=0이므로 경로를 한 바퀴 적분한 값도 0입니다.',
    '시험용 보강: “어느 한 경로에서 우연히 일이 0”인 것만으로 보존력이라고 할 수 없습니다. 해당 영역의 모든 허용 경로에서 일의 path independence(경로 독립성)가 성립하는 것이 핵심입니다.',eq='∮ <b>F</b>·d<b>r</b> = 0')
add(58,'위치에너지를 미분하면 힘을 얻습니다.','Contents 2 17:01–19:52',
    '서로 가까운 두 점에서 dU=−dV입니다. Total differential(전미분) dV=(∂V/∂x)dx+(∂V/∂y)dy+(∂V/∂z)dz를 dU=Fₓdx+Fᵧdy+Fz dz와 비교하면 각 force component(힘 성분)가 위치에너지의 음의 편미분임을 알 수 있습니다.',
    'Gradient(기울기 벡터) ∇V는 V가 가장 빠르게 증가하는 방향입니다. Conservative force(보존력)는 그 반대, 즉 V가 감소하는 방향을 향합니다. 시험용 보강: V=½kx²이면 Fₓ=−kx, V=mgy이면 Fᵧ=−mg로 기존 식을 다시 얻습니다.',eq='Fₓ = −∂V/∂x, Fᵧ = −∂V/∂y, Fz = −∂V/∂z<br><b>F</b> = −∇V',
    correction='원본에서 ∂Y/∂z는 ∂V/∂z로 읽어야 합니다. 마지막 벡터 식은 단위벡터가 빠져 있으므로 <b>F</b>=−[(∂V/∂x)<b>i</b>+(∂V/∂y)<b>j</b>+(∂V/∂z)<b>k</b>]로 보완합니다.')
add(59,'두 가지 일의 표현을 같게 놓습니다.','Contents 2 19:52–20:38',
    '전체 work(일)는 work–energy principle(일·에너지 원리)에 따라 T₂−T₁입니다. 그 일이 conservative force(보존력)의 일로만 이루어졌다면 동시에 V₁−V₂입니다. 두 식을 등치하여 에너지 보존식을 유도합니다.',eq='V₁−V₂ = T₂−T₁<br>⇒ T₁+V₁ = T₂+V₂')
add(60,'역학적 에너지는 조건부로 보존됩니다.','Contents 2 20:38–21:30',
    'Mechanical energy(역학적 에너지)는 E=T+V입니다. Conservative forces(보존력들)만 일을 하고 다른 힘의 net work(순일)가 0이면 처음과 끝의 E가 같습니다. 에너지가 보존된다는 것이 speed(속력)가 일정하다는 뜻은 아닙니다.',
    '시험용 보강: Nonconservative work(비보존력이 한 일) Uₙc가 있으면 E₂−E₁=Uₙc입니다. 스프링과 중력을 V에 포함했으면 그 일을 왼쪽에 다시 추가하지 않습니다. Zero-work constraint force(일을 하지 않는 구속력)는 존재해도 이 식을 방해하지 않습니다.',eq='E = T+V<br>E₂−E₁ = Uₙc')
add(61,'마찰은 역학적 에너지를 다른 형태로 전환합니다.','Contents 2 21:30–22:24',
    '고정된 rough surface(거친 표면) 위에서 kinetic friction(운동마찰)이 작용하면 negative work(음의 일)로 mechanical energy(역학적 에너지)가 감소합니다. 그만큼 주로 thermal energy(열에너지)가 증가하므로 전체 에너지 소실로 해석하면 안 됩니다.',
    '편집자 보강: “마찰이 항상 물체의 에너지를 감소시킨다”는 말은 움직이는 conveyor belt(컨베이어 벨트) 등 모든 기준계와 계에 일반화할 수 없습니다. 이 강의의 마찰 일 식은 고정 표면 위의 미끄럼 구간에 적용합니다.')
add(62,'진자에서 운동에너지와 위치에너지가 교환됩니다.','Contents 2 22:24–23:26',
    'Lowest point(최저점) A₂를 datum(기준 높이)으로 두면 수평 A₁에서 T₁=0, V₁=Wl입니다. 최저점에서는 V₂=0이고 T₂=Wl입니다. 두 상태의 total mechanical energy(총 역학적 에너지)는 같습니다.',eq='T₁+V₁ = 0+Wl<br>T₂+V₂ = Wl+0',
    correction='원본의 바닥 위치에너지 V₀=0은 문맥상 V₂=0입니다. 왼쪽 그림에 크게 남은 T₁=0 표시는 초기 상태의 값이며 최저점 운동에너지를 0으로 두라는 뜻이 아닙니다.')
add(63,'중심력 성질은 각운동량을 보존시킵니다.','Contents 2 23:26–24:19',
    'Central force(중심력)는 fixed center(고정 중심)에 대한 moment(모멘트)가 0입니다. 따라서 angular momentum(각운동량) <b>H</b>=<b>r</b>×m<b>v</b>가 conserved(보존)됩니다. φ는 반지름벡터와 속도벡터의 끼인각이며 초기 각도는 φ₀로 구별합니다.',
    'Conservative(보존적)이라는 성질만으로 angular momentum(각운동량)이 보존되는 것은 아닙니다. Fixed-center central force(고정 중심에 대한 중심력)라는 조건이 별도로 필요합니다.',eq='r₀mv₀ sinφ₀ = rmv sinφ',
    correction='원본 좌변의 sinφ는 초기 각도 sinφ₀로 보완합니다. Contents 2 23:26의 “conservative force”는 슬라이드 제목대로 conservative central force(보존 중심력) 조건에서 해석합니다.')
add(64,'보존력 성질은 역학적 에너지를 보존시킵니다.','Contents 2 24:19–24:43',
    'Inverse-square gravity(역제곱 중력)는 conservative(보존적)이므로 T+V도 일정합니다. Satellite mass(위성 질량) m을 약분하면 단위 질량당 에너지 식으로 간단해집니다. μ=GM을 쓰는 것은 편집자 보강 표기입니다.',
    'r을 알면 이 식으로 speed(속력) v를 먼저 계산하고, 앞의 angular momentum(각운동량) 식으로 velocity direction(속도 방향)에 관한 sinφ를 구할 수 있습니다. 두 보존식은 역할이 다릅니다.',eq='½mv₀²−GMm/r₀ = ½mv²−GMm/r<br>v² = v₀²+2μ(1/r−1/r₀)')
add(65,'근지점과 원지점에서는 속도가 반지름에 수직입니다.','Contents 2 24:43–25:37',
    'Perigee(근지점)와 apogee(원지점)는 r의 minimum/maximum(최솟값/최댓값) 위치입니다. Elliptic orbit(타원 궤도)의 두 점에서 radial velocity(반지름 속도)가 0이므로 φ=90°입니다. 따라서 angular momentum(각운동량) 식에서 sinφ=1이 됩니다.',
    '중력만 작용하는 bound orbit(묶인 궤도)에서는 작은 r에서 speed(속력)가 크고 큰 r에서 작습니다. 일반 위치의 sinφ를 빼고 rv=constant라고 쓰면 안 됩니다. Radial orbit(순수 반지름 궤도)처럼 h=0인 퇴화 경우는 여기 타원 그림의 적용 범위가 아닙니다. 마지막 제한은 편집자 보강입니다.')
add(66,'Lecture 6-4 · 예제 풀이','Problem Solving',
    '연결 블록, 사전 압축 스프링, 곡선 트랙, 사선 스프링과 칼라, 위성 발사를 차례로 풉니다. 원본의 group problem(그룹 문제)도 누락하지 않고 포함합니다.',role='Divider')
add(67,'예제 1 · 두 블록과 늘어나지 않는 케이블','Problem Solving 00:17–01:02',
    'A는 horizontal plane(수평면) 위의 200 kg 블록, B는 아래로 매달린 300 kg 블록입니다. Inextensible cable(늘어나지 않는 케이블), weightless and frictionless pulley(무게와 마찰이 없는 도르래)를 가정하고 μₖ=0.25입니다. Released from rest(정지 상태에서 놓음) 후 A가 2 m 이동했을 때의 velocity(속도)를 구합니다.',
    'Fixed pulley(고정 도르래) 하나이므로 A가 오른쪽으로 2 m 이동하면 B도 아래로 2 m 이동합니다. 두 speed(속력)는 같지만 velocity vectors(속도벡터들)의 방향은 서로 다릅니다. Kinetic energy(운동에너지)에는 공통 크기 v를 사용합니다.')
add(68,'각 블록의 일을 적은 뒤 합산합니다.','Problem Solving 01:02–01:24',
    'Cable tension(케이블 장력)을 F꜀로 둡니다. A에는 +F꜀s, B에는 −F꜀s의 일이 작용합니다. 두 식을 합하면 unknown tension(미지의 장력)이 사라지므로 speed(속력)를 먼저 구할 수 있습니다.',
    '편집자 보강: 상쇄는 동일한 tension magnitude(장력 크기)와 동일한 displacement magnitude(변위 크기)에 의존합니다. 물체를 합쳐 system(계)으로 잡는 것만으로 모든 internal work(내력이 한 일)가 자동으로 0이 되는 것은 아닙니다.')
add(69,'A 블록: 장력은 양의 일, 마찰은 음의 일','Problem Solving 01:24–03:25',
    'A의 vertical acceleration(수직 가속도)은 0이고 케이블은 수평이므로 NA=mAg=1962 N입니다. Kinetic friction(운동마찰)의 크기는 fA=μₖNA=490.5 N입니다. 원본은 490 N으로 반올림합니다. 중량과 수직항력은 수평 이동에 일을 하지 않습니다.',
    'Initial kinetic energy(초기 운동에너지)는 0입니다. 오른쪽 displacement(변위) s=2 m에 대해 cable work(케이블이 한 일)는 양수, friction work(마찰이 한 일)는 음수입니다.',eq='0 + F꜀(2) − 490.5(2) = ½(200)v²')
add(70,'B 블록: 아래로 이동하므로 중량의 일은 양수','Problem Solving 03:25–04:19',
    'B에는 upward tension(위쪽 장력)과 downward weight(아래쪽 중량)가 있습니다. B의 downward displacement(하향 변위) 2 m에 대해 tension work(장력이 한 일)는 −F꜀(2), gravity work(중력이 한 일)는 +mBg(2)입니다.',eq='−F꜀(2) + 2943(2) = ½(300)v²',
    correction='원본의 300×9.81=2960 N은 산술 오기로 정확히 2943 N입니다. 아래 대입 줄의 −2940(2)는 +2940(2)로 교정해야 하며, 다음 장의 합산식도 양의 부호를 사용합니다. 본문 검산은 중간 반올림 없이 2943 N을 사용합니다.')
add(71,'두 블록의 속력은 약 4.43 m/s입니다.','Problem Solving 04:19–04:53',
    'A와 B의 식을 더하면 tension work(장력이 한 일)가 상쇄되어 4905 J=250v²입니다. 따라서 v=√(19.62)≈4.429 m/s입니다. A의 velocity(속도)는 오른쪽, B는 아래쪽으로 약 4.43 m/s입니다.',
    '원본은 rounded force(반올림된 힘) 2940 N·490 N으로 4900 J를 사용하지만 세 자리 답은 같습니다. 시험용 보강: 필요하면 A 식에 v²를 다시 대입하여 tension(장력) F꜀=1471.5 N을 구할 수 있습니다.',eq='(2943−490.5)(2) = ½(200+300)v²<br>v ≈ 4.43 m/s')
add(72,'계를 크게 잡으면 같은 상쇄를 한 번에 처리합니다.','Problem Solving 04:53–05:17',
    'A+B를 combined system(결합된 계)으로 잡으면 두 블록의 kinetic energy(운동에너지)를 더하고, 바깥에서 한 일 중 B의 gravity work(중력이 한 일)와 A의 friction work(마찰이 한 일)를 계산하면 됩니다.',
    '“Everything that moves(움직이는 모든 것)”를 포함하라는 원본 조언은 이 이상 케이블 문제에서 계산을 간단히 하는 전략입니다. 만약 massive pulley(질량 있는 도르래)의 회전까지 있다면 그 kinetic energy(운동에너지)도 추가해야 합니다. 이 한계는 편집자 보강입니다.')
add(73,'예제 1의 대안 풀이: 결합된 계','Problem Solving 05:17–05:37',
    '그림은 두 블록의 initial/final positions(초기·최종 위치)를 표시합니다. Initial speed(초기 속력)는 0, 이동거리 2 m, μₖ=0.25라는 조건을 하나의 system(계)에 적용합니다. 두 블록의 cable constraint(케이블 구속관계)는 여전히 필요합니다.')
add(74,'결합계의 초기 운동에너지와 전체 일','Problem Solving 05:37–06:03',
    '처음 두 블록 모두 stationary(정지)이므로 T₁=0입니다. External work(외력이 한 일)는 B의 낙하로 +5886 J, A의 마찰로 −981 J, 합계 4905 J입니다. 원본의 4900 J는 유효숫자를 줄인 값입니다.',eq='ΣU = −μₖmAgs + mBgs<br>= −981 + 5886 = 4905 J')
add(75,'결합계의 운동에너지는 두 물체의 합입니다.','Problem Solving 06:03–06:19',
    'Common speed(공통 속력) v가 같으므로 T₂=½mAv²+½mBv²=½(mA+mB)v²입니다. 한 물체의 kinetic energy(운동에너지)만 넣거나, 서로 다른 velocity directions(속도 방향들)을 이유로 빼면 안 됩니다.',eq='T₂ = ½(200+300)v² = 250v²',
    correction='원본 하단의 “total work” 질문 아래에는 kinetic energy(운동에너지) 식이 반복되어 있습니다. 전체 일은 앞 장의 약 4900 J이며, 이 장의 T₂ 식과 구별합니다.')
add(76,'두 풀이 방법은 같은 답으로 귀결됩니다.','Problem Solving 06:19–06:46',
    'Work–energy principle(일·에너지 원리) T₁+ΣU=T₂에 각 항을 넣으면 v≈4.43 m/s입니다. 개별 물체 방식은 tension(장력)까지 추적하기 좋고, 결합계 방식은 상쇄되는 unknown internal force(미지의 내력)를 생략하기 좋습니다.')

add(77,'예제 2 · 이미 압축된 스프링으로 포장물을 멈춥니다.','Problem Solving 06:46–07:54',
    'Mass(질량) 60 kg인 package(포장물)가 horizontal surface(수평면)를 2.5 m/s로 오른쪽으로 이동합니다. Spring constant(스프링 상수)는 20 kN/m=20000 N/m이며 cable(케이블)이 스프링을 처음부터 120 mm compressed(압축된) 상태로 유지합니다. 최초 위치와 스프링 접촉면 사이 거리는 600 mm입니다.',
    'Package(포장물)가 접촉한 뒤 spring compression(스프링 압축)이 추가로 40 mm 증가합니다. 따라서 가장 눌렸을 때의 total compression(전체 압축량)은 160 mm입니다. 그림과 뒤 풀이의 2400→3200 N 힘 변화가 이를 확인해 줍니다.',
    correction='원본의 “maximum deflection … 40 mm”는 자연길이 기준 총 변형량이 아니라 추가 압축량입니다. 자막 07:27–07:54 및 13:29–13:45와 후속 식에 따라 Δx=40 mm, x₂=120+40=160 mm로 해석합니다.')
add(78,'되돌아올 때의 속력까지 두 단계로 구합니다.','Problem Solving 07:54–08:53',
    '첫 미지수는 coefficient of kinetic friction(운동마찰계수) μₖ, 두 번째는 rebound(되튐) 후 원래 위치를 다시 지날 때의 velocity(속도)입니다. 최대로 눌린 순간 v₂=0이라는 조건이 μₖ를 결정합니다.',
    '첫 이동은 rightward(오른쪽), 복귀는 leftward(왼쪽)입니다. Friction force(마찰력)의 공간적 방향은 바뀌지만 항상 현재 미끄럼을 거스르므로 고정 표면에 대한 friction work(마찰이 한 일)는 두 구간 모두 음수입니다.')
add(79,'최대 압축점을 기준으로 구간을 나눕니다.','Problem Solving 08:53–09:38',
    'State 1(상태 1)은 최초 위치, state 2(상태 2)는 maximum compression(최대 압축), state 3(상태 3)은 되돌아온 최초 위치입니다. 1→2에서 known speed(알려진 속력) v₁=2.5와 v₂=0으로 μₖ를 구하고, 2→3에서 이미 구한 μₖ로 v₃를 구합니다.',
    'Trial speed(시험적으로 놓은 속력)를 추정할 필요 없이 각 구간에 work–energy principle(일·에너지 원리)을 한 번씩 적용합니다. Maximum compression(최대 압축)에서 순간 속도가 0이라고 equilibrium(평형)이나 acceleration(가속도) 0을 뜻하지는 않습니다.')
add(80,'마찰은 스프링에 닿기 전부터 작용합니다.','Problem Solving 09:38–12:23',
    'Initial kinetic energy(초기 운동에너지)는 ½(60)(2.5²)=187.5 J입니다. 최대로 눌린 상태에서는 T₂=0입니다. Friction(마찰)은 0.600+0.040=0.640 m 전체에 작용하고, 스프링 힘은 수평이므로 N=mg=588.6 N입니다.',
    '여기서 구한 것은 friction work(마찰이 한 일)뿐입니다. Spring work(스프링이 한 일)를 더하지 않은 상태에서 μₖ를 결정하면 안 됩니다. 영상도 11:59 이후 이 누락을 정정하고 스프링 항을 추가합니다.',eq='Uf = −μₖ(60)(9.81)(0.640)<br>= −376.704μₖ J',
    correction='원본 대입식 중 +μₖ(60)(9.81)(0.640)처럼 보이는 항에는 음수가 필요합니다. 마지막의 −377μₖ와 힘·이동 방향에 맞춰 −376.704μₖ로 계산합니다.')
add(81,'스프링 일을 추가하면 마찰계수가 결정됩니다.','Problem Solving 12:23–14:49',
    '처음 접촉할 때 spring force(스프링 힘)의 크기는 Pmin=k(0.120)=2400 N, maximum compression(최대 압축)에서는 Pmax=k(0.160)=3200 N입니다. 두 힘 사이 사다리꼴 면적에 음수를 붙이면 Us=−½(2400+3200)(0.040)=−112 J입니다.',
    '따라서 187.5−376.704μₖ−112=0이고 μₖ=75.5/376.704≈0.2004, 원본 유효숫자로 0.20입니다. 이 μₖ는 무차원입니다.',eq='Us = ½k(0.120²−0.160²) = −112 J<br>μₖ ≈ 0.2004',
    correction='원본의 Pmax 대입 줄 20000(0.120)=2400 N은 Pmin의 값이 반복된 오기입니다. 정확한 식은 Pmax=20000(0.120+0.040)=3200 N이며 바로 아래 면적 계산도 3200 N을 사용합니다.')
add(82,'복귀 중에는 스프링이 에너지를 돌려줍니다.','Problem Solving 14:49–16:28',
    '2→3에서 package(포장물)는 다시 총 0.640 m 이동합니다. Spring(스프링)은 0.160 m에서 원래 cable-limited compression(케이블에 의해 제한된 압축량) 0.120 m까지 돌아오는 0.040 m 동안 +112 J의 일을 하고, 이후 package(포장물)는 떨어져서 이동합니다.',
    '같은 friction coefficient(마찰계수)와 이동거리 때문에 Uf=−75.5 J입니다. 따라서 net work(순일)는 36.5 J이고 T₃=½(60)v₃²이므로 speed(속력)는 1.103 m/s입니다. Velocity(속도)는 왼쪽으로 1.103 m/s이며, 오른쪽 양의 좌표를 쓰면 −1.103 m/s입니다.',eq='0 + 112−75.5 = ½(60)v₃²<br>|v₃| ≈ 1.103 m/s')
add(83,'두 구간을 나누는 이유는 미지수와 운동 방향이 바뀌기 때문입니다.','Problem Solving 16:28–16:52',
    '1→2의 zero final speed(0인 최종 속력)로 μₖ를 정한 뒤 다른 구간에 사용합니다. 2→3에서는 spring work(스프링이 한 일)의 부호가 반대로 바뀌지만 friction work(마찰이 한 일)는 음수로 유지됩니다.',
    '시험용 보강: 1→3을 합치면 spring net work(스프링의 순일)는 0, friction loss(마찰 손실)는 75.5×2=151 J입니다. 187.5−151=36.5 J로 복귀 운동에너지를 독립 검산할 수 있습니다.')
add(84,'이상 스프링은 추가로 저장된 에너지를 돌려줍니다.','Problem Solving 16:52–17:15',
    'Ideal spring(이상 스프링) 자체는 dissipative element(에너지를 소산시키는 요소)가 아닙니다. 왕복 후 원래 사전 압축 상태가 되면 이번 충돌에서 추가로 저장한 112 J를 돌려줍니다. 이 예제의 왕복 mechanical energy loss(역학적 에너지 손실)는 마찰 때문입니다.',
    '원본의 “all of its energy”는 추가 저장분을 돌려준다는 의미로 제한합니다. 최초부터 저장된 ½k(0.120²)=144 J는 케이블이 유지하는 사전 압축 상태에 남습니다. 이 수치와 범위 설명은 편집자 보강입니다. Permanently at rest(영구히 정지)시키려면 추가적인 소산·고정 조건이 필요합니다.')
add(85,'예제 3 · 골짜기의 힘과 봉우리의 접촉 조건','Problem Solving 17:15–18:41',
    '1000 kg car(차량)가 point 1(1번 점)에서 starts from rest(정지 출발)하고 frictionless track(마찰 없는 트랙)을 내려옵니다. Point 2(2번 점)는 출발점보다 12 m 아래, radius of curvature(곡률반지름) ρ₂=6 m인 골짜기입니다. Point 3(3번 점)는 2번 점보다 4.5 m 높은 봉우리입니다.',
    '구할 것은 N₂인 force exerted by the track(트랙이 가하는 힘)와 3번 점에서 접촉을 유지하는 minimum radius(최소 반지름)입니다. Energy(에너지)로 speed(속력), Newton’s law(뉴턴 법칙)로 reaction(반력)을 구하는 결합 문제입니다.')
add(86,'속력을 구한 뒤 법선 방향의 힘을 씁니다.','Problem Solving 18:41–19:28',
    '먼저 1→2의 height drop(낙하 높이)로 v₂를 구하고 N₂−mg=mv₂²/ρ₂를 씁니다. 이어 1→3의 height drop(낙하 높이) 12−4.5=7.5 m로 v₃를 구하고 mg−N₃=mv₃²/ρ₃를 씁니다.',
    'Ground contact(지면 접촉)는 track(트랙)이 물체를 당길 수 없다는 조건 N₃≥0을 만족해야 합니다. Limiting case(한계 상황)는 N₃=0입니다. 문제의 “safe”는 이 입자 모형의 이탈 방지 조건으로 해석합니다.')
add(87,'2번 점의 속력: 12 m의 위치에너지가 감소합니다.','Problem Solving 19:28–20:22',
    'Normal force(수직항력)는 고정 트랙을 따르는 변위에 수직이라 일이 0입니다. Gravity work(중력이 한 일) mg(12)가 kinetic energy(운동에너지)가 됩니다. Mass(질량)는 약분됩니다.',eq='0 + mg(12) = ½mv₂²<br>v₂² = 24g = 235.44 m²/s²<br>v₂ ≈ 15.34 m/s')
add(88,'2번 점의 수직항력은 중량에 구심 요구량을 더한 값입니다.','Problem Solving 20:22–21:17',
    '골짜기에서 inward normal direction(안쪽 법선 방향)은 위쪽입니다. 따라서 N₂−W=m v₂²/ρ₂입니다. v₂²=24g, ρ₂=6 m를 대입하면 maₙ=4mg이고 N₂=5mg=49050 N=49.05 kN입니다.',
    'N₂ 자체를 centripetal force(구심 합력)와 같게 두면 W를 빠뜨립니다. 실제 inward resultant(안쪽 합력)은 N₂−W입니다.',eq='N₂ = mg + mv₂²/ρ₂ = 5mg',
    correction='원본 마지막 대입식은 N=5W=5(1000)(9.81) N으로 읽어야 합니다. N=5W(1000)(9.81)처럼 중량에 질량·가속도를 다시 곱하지 않습니다.')
add(89,'3번 점의 속력: 낙하 높이는 7.5 m입니다.','Problem Solving 21:17–22:01',
    '출발점과 3번 점의 elevation difference(높이 차이)는 12−4.5=7.5 m입니다. 중간에 골짜기를 지나도 frictionless(마찰 없는) 모델에서는 중력이 한 일이 path-independent(경로에 무관)하므로 이 높이 차이만 필요합니다.',eq='0 + mg(7.5) = ½mv₃²<br>v₃² = 15g = 147.15 m²/s²<br>v₃ ≈ 12.13 m/s')
add(90,'봉우리에서는 수직항력이 중량에서 빠집니다.','Problem Solving 22:01–22:39',
    '3번 점의 center of curvature(곡률중심)는 아래쪽이므로 downward positive(아래쪽 양수)로 W−N₃=m v₃²/ρ₃입니다. N₃=0을 경계로 두면 ρ₃=v₃²/g=15 m입니다.',
    'Contact maintained(접촉 유지)를 위해 N₃=mg−m v₃²/ρ₃≥0, 즉 ρ₃≥15 m가 필요합니다. ρ₃&lt;15 m이면 접촉 상태를 가정한 식이 negative normal force(음의 수직항력)를 요구하므로 트랙이 당기지 않는 모형에서는 이탈합니다.',eq='N₃ = mg−mv₃²/ρ₃ ≥ 0<br>ρ₃ ≥ 15 m',
    correction='원본의 이 장 제목은 속력을 에너지로 구한다고 반복되지만 실제 계산은 Newton’s second law(뉴턴 제2법칙)와 N₃=0으로 곡률반지름을 구하는 단계입니다.')
add(91,'에너지식과 운동방정식은 서로 보완합니다.','Problem Solving 22:39–23:06',
    'Work–energy(일·에너지)는 두 위치의 speed(속력)를 연결하지만 zero-work normal force(일하지 않는 수직항력)를 직접 보여 주지 않습니다. Newton’s second law(뉴턴 제2법칙)는 그 속력과 curvature(곡률)를 이용해 normal force(수직항력)를 결정합니다.',
    '이 풀이 흐름을 진자의 tension(장력) P=3W와 비교하면 같습니다. 두 경우 모두 먼저 위치 변화에서 운동에너지를 계산하고, 이후 normal acceleration(법선 가속도)을 힘과 연결합니다.')
add(92,'골짜기의 5W와 봉우리의 15 m는 다른 조건입니다.','Problem Solving 23:06–23:44',
    '골짜기의 support load(지지 하중) N₂=5W와 봉우리의 contact limit(접촉 한계) ρ₃=15 m는 서로 다른 위치의 결과입니다. 골짜기에서 실제 net acceleration(알짜 가속도)은 4g이며, 5W는 지지력의 크기입니다. 원본의 5g 비유를 5g의 알짜 가속도로 혼동하지 않습니다.',
    '봉우리에서는 ρ₃를 크게 할수록 같은 speed(속력)에 필요한 v₃²/ρ₃가 작아져 N₃가 양수가 됩니다. Height(높이)와 초기 조건이 같으면 radius(반지름)를 크게 바꾼다고 에너지식의 speed(속력)가 줄지는 않습니다. 실제 안전 여유에 필요한 반지름은 이 단순 모델만으로 확정하지 않습니다.',
    correction='자막 18:33의 “reduce the speed”는 v²/ρ인 법선 가속도 요구량의 감소로 구별합니다. 23:23–23:37의 “15 m보다 작으면 normal force가 5W보다 커진다”는 설명을 봉우리 조건에 적용하지 않습니다. 올바른 조건은 N₃=mg−mv₃²/ρ₃이며, 15 m 미만에서 접촉 가정이 깨집니다.')
add(93,'그룹 문제 · 컨베이어에 같은 속력으로 도착하기','Problem Solving 23:44–24:42',
    'Package(포장물)는 A에서 incline(경사면)을 따라 1 m/s로 출발하고, C에서 belt speed(벨트 속력) 2 m/s와 같아져야 합니다. 그림의 incline angle(경사각)은 30°, horizontal segment(수평 구간) BC는 7 m, μₖ=0.25입니다. 구하는 d는 경사면 AB의 길이입니다.',
    'A→B에서는 gravity(중력)가 양의 일, friction(마찰)이 음의 일을 합니다. B→C의 수평 구간에서는 gravity work(중력이 한 일)는 0이고 friction work(마찰이 한 일)만 남습니다. 영상은 최종 수치 답을 제공하지 않고 풀이 전략만 설명합니다.')
add(94,'그룹 문제의 완성 풀이: 구간별 마찰을 더합니다.','Problem Solving 24:42–25:14 · 계산은 시험용 보강',
    '시험용 보강: 원본 전략을 따라 구간 AB를 straight incline(직선 경사면), BC를 horizontal(수평)로 모델링하고, 도면에서 치수·곡률이 주어지지 않은 연결부의 추가 손실은 neglect(무시)합니다. 이 모델에서는 NAB=mg cos30°, NBC=mg입니다. 유한 곡률 연결부의 반력·마찰까지 엄밀히 계산하려면 별도의 기하 정보가 필요합니다.',
    'Gravity work(중력이 한 일)는 mg d sin30°, friction work(마찰이 한 일)는 −μₖmg cos30° d−μₖmg(7)입니다. 이를 ½m(2²−1²)와 같게 두고 m을 약분합니다. 정리하면 d≈6.712 m입니다. 원본에 없는 이 수치는 위 모델하의 보강 풀이이며 공식 강의 답안으로 표시하지 않습니다.',eq='g[d sin30°−μₖd cos30°−7μₖ] = ½(2²−1²)<br>d = [1.5/g+7μₖ]/[sin30°−μₖ cos30°]<br>d ≈ 6.71 m',
    extra=card('시험용 보강 · 중간 상태 검산','이 d에서 vB²≈38.335 m²/s이고 수평 구간의 마찰로 2μₖg(7)=34.335 m²/s만큼 감소하여 vC²=4 m²/s가 됩니다. 경사면의 gravity component(중력 성분)가 마찰보다 커서 AB에서 가속하고 BC에서 감속하는 흐름과 일치합니다.'))
add(95,'예제 4 · 사선으로 늘어나는 스프링과 칼라','Problem Solving 25:14–26:20',
    '10 kg collar(칼라)가 frictionless vertical rod(마찰 없는 수직 봉)를 따라 움직입니다. Spring constant(스프링 상수)는 200 N/m, undeflected length(무변형 길이)는 100 mm입니다. 초기 스프링 길이는 수평 간격 200 mm이므로 이미 100 mm stretched(늘어난) 상태입니다.',
    'Released from rest(정지 상태에서 놓음) 후 150 mm 아래의 position 2(위치 2)에서 velocity(속도)를 구합니다. 칼라의 이동거리 150 mm를 곧바로 스프링의 추가 신장량으로 사용하지 않습니다. 스프링 길이는 기하학적으로 계산합니다.')
add(96,'중력과 스프링 위치에너지를 함께 계산합니다.','Problem Solving 26:20–26:54',
    '봉의 normal reaction(법선 반력)은 horizontal(수평)이고 칼라의 displacement(변위)는 vertical(수직)이므로 일이 0입니다. Friction(마찰)이 없고 gravity(중력)와 spring force(스프링 힘)는 conservative(보존적)이므로 T₁+V₁=T₂+V₂를 사용합니다.',
    'Potential energy(위치에너지)는 V=Vg+Ve=mgy+½kx²입니다. Datum(기준 높이)은 위치 1로 두면 y₁=0, y₂=−0.150 m입니다. Spring deformation(스프링 변형량)은 각각 실제 길이에서 0.100 m를 빼서 구합니다.')
add(97,'초기 상태: 정지해 있어도 스프링 에너지는 있습니다.','Problem Solving 26:54–27:50',
    'L₁=0.200 m, L₀=0.100 m이므로 x₁=0.100 m입니다. Elastic potential energy(탄성 위치에너지)는 ½(200)(0.100²)=1 J입니다. y₁=0이어서 Vg₁=0이고 T₁=0입니다. 따라서 total mechanical energy(총 역학적 에너지)는 1 J입니다.',eq='T₁ = 0, V₁ = 1 J',
    correction='원본 그림의 최종 스프링 길이 “2500 mm”는 기하학과 다음 장의 0.25 m에 맞춰 250 mm로 읽습니다. √(200²+150²)=250 mm입니다.')
add(98,'최종 상태: 피타고라스로 스프링 길이를 구합니다.','Problem Solving 27:50–28:41',
    'L₂=√(0.200²+0.150²)=0.250 m이므로 x₂=0.250−0.100=0.150 m입니다. Ve₂=½(200)(0.150²)=2.25 J, Vg₂=(10)(9.81)(−0.150)=−14.715 J입니다. 따라서 V₂=−12.465 J입니다.',
    'Negative V₂(음의 최종 위치에너지)는 중력의 기준 높이를 위치 1로 선택한 결과입니다. 운동에너지 T₂=½(10)v₂²=5v₂²는 음수가 될 수 없습니다.',eq='L₂ = 0.250 m, x₂ = 0.150 m<br>V₂ = 2.25−14.715 = −12.465 J',
    correction='원본 Vg 대입의 (9.81)(−0.15)에는 mass(질량) 10 kg이 빠져 있습니다. (10)(9.81)(−0.15)=−14.715 J이며 원본의 최종 숫자는 이 올바른 값을 사용합니다. 그림의 2500 mm도 250 mm입니다.')
add(99,'칼라의 속도는 아래쪽으로 1.641 m/s입니다.','Problem Solving 28:41–28:57',
    '초기 1 J가 T₂+V₂와 같으므로 1=5v₂²−12.465입니다. 따라서 T₂=13.465 J, v₂=√(13.465/5)=1.641 m/s입니다. Energy(에너지) 식은 speed magnitude(속력 크기)를 주고 downward direction(아래쪽 방향)은 문제의 운동 구간에서 판단합니다.',
    '시험용 보강: 중력이 14.715 J를 내놓고 스프링이 2.25−1=1.25 J를 더 저장하므로 남은 13.465 J가 운동에너지가 됩니다. 이는 직접 work(일)를 계산한 검산입니다.',eq='v₂ = √(13.465/5) ≈ 1.641 m/s ↓')
add(100,'스프링을 일로 쓰거나 위치에너지로 씁니다.','Problem Solving 28:57–29:15',
    'Spring(스프링)을 포함하는 에너지 모델에서는 Ve를 쓰고, spring force(스프링 힘)를 외력으로 다루면 Us=Ve₁−Ve₂를 work(일)에 넣습니다. 두 방식은 같은 내용을 다른 위치에 적은 것입니다.',
    '이 예제의 직접 일 방식은 0+14.715−1.25=½(10)v₂²입니다. Ve₂−Ve₁을 이미 에너지 식에 넣고 spring work(스프링이 한 일) −1.25 J를 다시 더하면 double counting(이중 계산)이 됩니다.')
add(101,'마찰이 있다면 수직항력을 먼저 확인해야 합니다.','Problem Solving 29:15–29:39',
    '칼라와 봉 사이에 kinetic friction(운동마찰)이 있다면 mechanical energy(역학적 에너지) 보존만으로는 부족합니다. Normal reaction(법선 반력)의 크기가 spring force(스프링 힘)의 horizontal component(수평 성분)에 의해 달라져 friction work(마찰이 한 일)도 위치 함수가 됩니다.',
    '시험용 보강: 아래쪽 이동량 z≥0에 대해 L=√(0.200²+z²), spring force magnitude(스프링 힘의 크기)는 k(L−L₀), N=k(L−L₀)(0.200/L)입니다. 따라서 Uf=−∫μₖN(z) dz로 계산합니다. N=mg라고 둘 수 없는 이유는 봉의 법선 방향이 수평이기 때문입니다.')
add(102,'예제 5 · 최대고도와 발사각 오차','Problem Solving 29:39–30:34',
    'Satellite(위성)가 altitude(고도) 500 km에서 parallel to Earth’s surface(지표면에 평행하게) 36900 km/h로 발사됩니다. (a)는 maximum altitude(최대고도), (b)는 어느 위치에서도 지표면 200 km 이내로 접근하지 않게 하는 maximum allowable launch-angle error(최대 허용 발사각 오차)입니다.',
    'R=6370 km, r₀=6870 km, v₀=10250 m/s, μ=gR²를 사용합니다. Gravity only(중력만 작용), fixed Earth center(고정된 지구 중심), atmospheric drag neglected(대기저항 무시)의 입자 궤도 모형입니다. 이 이상화의 명시는 편집자 보강입니다.')
add(103,'중심력의 두 보존식을 동시에 사용합니다.','Problem Solving 30:34–31:15',
    'Part (a)(문항 a)는 초기와 maximum radius(최대 중심 거리) 위치를 연결합니다. 두 위치의 velocity(속도)가 radius(반지름)에 perpendicular(수직)이므로 h=r₀v₀=r₁v₁입니다. Energy(에너지)와 합치면 두 미지수 r₁·v₁을 구할 수 있습니다.',
    'Part (b)(문항 b)는 초기 발사점이 반드시 perigee(근지점)가 아닙니다. Boundary condition(경계 조건) rmin=6570 km를 먼저 두고 sinφ₀를 유지한 angular momentum(각운동량) 식을 써야 합니다.')
add(104,'문항 a의 에너지식: 위성 질량이 약분됩니다.','Problem Solving 31:15–31:31',
    '두 위치에서 T=½mv², V=−GMm/r를 사용합니다. 양변에 m이 공통이므로 약분합니다. 원지점까지 멀어지면 potential energy(위치에너지)는 덜 음수가 되고 speed(속력)는 작아집니다.',eq='½v₀²−μ/r₀ = ½v₁²−μ/r₁')
add(105,'문항 a의 각운동량식: 속력을 거리로 바꿉니다.','Problem Solving 31:31–31:48',
    'Initial launch(초기 발사)가 tangential(접선 방향)이고 다른 지점도 apogee(원지점)이므로 두 sinφ가 모두 1입니다. 따라서 v₁=v₀r₀/r₁입니다. r₁이 커질수록 speed(속력)는 작아진다는 결과가 식에도 나타납니다.',eq='r₀v₀ = r₁v₁<br>v₁ = v₀r₀/r₁')
add(106,'두 보존식으로 원지점 거리를 구합니다.','Problem Solving 31:48–32:21',
    'v₁을 에너지 식에 대입하면 ½v₀²[1−(r₀/r₁)²]=(μ/r₀)(1−r₀/r₁)입니다. 서로 다른 두 apses(근지점·원지점)를 구하므로 r₁≠r₀인 해에서 1−r₀/r₁을 약분하면 1+r₀/r₁=2μ/(r₀v₀²)입니다.',
    '따라서 r₁=r₀/[2μ/(r₀v₀²)−1]입니다. μ=9.81(6.37×10⁶)²=3.98059389×10¹⁴ m³/s²를 중간 반올림 없이 사용하면 r₁≈6.67025×10⁷ m, maximum altitude(최대고도) r₁−R≈6.03325×10⁷ m=60333 km입니다.',eq='r₁ = r₀/[2μ/(r₀v₀²)−1]<br>zmax = r₁−R ≈ 60333 km',
    correction='원본은 μ≈398×10¹², r₁≈66.8×10⁶ m, maximum altitude≈60.4×10⁶ m를 표시합니다. 본문은 원본 답 약 60400 km와 같은 입력을 끝까지 유지한 검산 약 60333 km를 구별합니다. 처음 위치도 에너지식의 자명한 해이므로 약분에서 제외했음을 밝힙니다.')
add(107,'문항 b: 허용되는 가장 낮은 지점의 속력','Problem Solving 32:21–32:53',
    'Closest allowed altitude(허용 최저고도)는 200 km이므로 rmin=R+200 km=6.57×10⁶ m입니다. Initial speed(초기 속력)의 크기가 같으면 energy(에너지)는 발사 방향과 무관하게 같고, 에너지 식으로 이 근지점의 vmax를 구할 수 있습니다.',
    'vmax²=v₀²+2μ(1/rmin−1/r₀)입니다. 구한 speed(속력)를 다음 angular momentum(각운동량) 식에 넣어 initial direction(초기 방향)을 결정합니다.',eq='vmax² = v₀²+2μ(1/rmin−1/r₀)')
add(108,'발사각이 달라지면 sinφ₀를 생략할 수 없습니다.','Problem Solving 32:53–33:24',
    'φ₀는 outward radius(바깥쪽 반지름)와 initial velocity(초기 속도)의 끼인각입니다. 기준인 수평 발사는 φ₀=90°이지만 error(오차)가 있으면 달라집니다. 근지점의 속도는 radius(반지름)에 수직이므로 그쪽만 sinφ=1입니다.',
    '같은 r₀와 v₀에서 수평을 벗어나면 tangential component(접선 성분)가 줄어 angular momentum(각운동량)도 줄어듭니다. 이것이 더 낮은 perigee(근지점)를 허용하게 되는 이유입니다.',eq='r₀v₀ sinφ₀ = rmin vmax<br>sinφ₀ = rmin vmax/(r₀v₀)')
add(109,'허용 오차는 수평 방향에서 약 ±11.44°입니다.','Problem Solving 33:24–33:50',
    '위의 입력으로 sinφ₀≈0.9801189입니다. φ₀는 약 78.556° 또는 101.444°로, horizontal direction(수평 방향)인 90°에서 약 ±11.444° 벗어납니다. Radial angle(반지름 기준 각도) φ₀와 horizontal launch error(수평 발사 오차)를 구별합니다.',
    '편집자 보강: δ=φ₀−90°라 놓으면 sinφ₀=cosδ입니다. 따라서 허용 범위는 |δ|≤arccos(0.9801189)≈11.44°입니다. 부호가 반대인 두 초기 radial directions(반지름 운동 방향들)는 같은 에너지·각운동량 크기를 갖지만 궤도 위 출발 방향이 다릅니다.',eq='|δ| ≤ arccos(0.9801189)<br>≈ 11.44°',
    correction='원본의 sinφ₀=0.9801에서 직접 계산한 수평 오차는 약 11.45°이고, 원본 표시는 ±11.5°입니다. 입력을 끝까지 유지한 본문 검산값은 ±11.44°이며 원본 숫자와 구별합니다. 자막 “sine of v0”는 sinφ₀로 읽습니다.')
add(110,'궤도 보정 설명은 예제의 이상화와 구별합니다.','Problem Solving 33:50–34:08',
    '원본은 space probe(우주 탐사선)의 mid-course correction(중간 궤도 보정)을 언급합니다. 이번 계산은 초기 조건 이후 중력만 작용하는 이상적인 coast phase(관성 비행 구간)를 다루며, correction thrust(보정 추력)가 작용하는 구간에서는 해당 보존식을 그대로 유지할 수 없습니다.',
    '편집자 보강: 실제 위성의 궤도 보정 필요 여부는 임무·초기 오차·저항 등에 따라 다릅니다. 원본의 “우주정거장에서 발사한 위성은 대체로 미세 보정이 필요 없다”는 문장을 모든 위성의 설계 규칙으로 일반화하지 않습니다.')
add(111,'참고문헌','원본 참고문헌 슬라이드',
    'Beer, Johnston, Cornwell, Self, Sanghi, <em>Vector Mechanics for Engineers: Dynamics</em>, 12th Edition, Chapter 13. 원본에 제시된 참고문헌을 보존했습니다.',role='Reference')
assert len(records) == 111

exam_items = [
    ('Q1. Define work(일을 정의하라).',
     'The work of a force over a displacement is the line integral of the dot product of the force and the differential displacement: U = integral of F dot dr. Work is a signed scalar quantity.',
     'Dot product(내적), differential displacement(미소 변위), signed scalar(부호 있는 스칼라)가 핵심 표현입니다. Force(힘)의 크기에 이동거리만 곱하는 정의는 일반적인 variable force(변하는 힘)를 포함하지 못합니다.'),
    ('Q2. State the work–energy principle(일·에너지 원리를 서술하라).',
     'For a particle of constant mass in an inertial frame, the total work done by all forces equals the change in its kinetic energy. Thus, T1 + sum of U(1 to 2) = T2, where T = one half m v squared.',
     'All forces(모든 힘), change in kinetic energy(운동에너지의 변화), constant mass(일정 질량)를 포함합니다. Total work(전체 일)를 운동에너지 자체와 같다고 쓰지 않습니다.'),
    ('Q3. Explain zero work by a normal force(수직항력의 일이 0인 이유를 설명하라).',
     'For a particle moving along a fixed smooth surface, the normal force is perpendicular to the displacement at every point. Therefore, its dot product with the displacement is zero, although the normal force itself need not be zero.',
     'Fixed smooth surface(고정된 매끈한 표면)라는 조건과 perpendicular(수직)이라는 이유를 같이 씁니다. Zero work(0인 일)와 zero force(0인 힘)는 다릅니다.'),
    ('Q4. Define a conservative force(보존력을 정의하라).',
     'A force is conservative if its work between two points is independent of the path. Its work can be written as V1 minus V2, and its work over any closed path is zero.',
     'Independent of the path(경로에 무관한), any closed path(모든 닫힌 경로), V₁−V₂의 순서를 지킵니다. Potential energy decrease(위치에너지 감소)가 positive work(양의 일)에 대응합니다.'),
    ('Q5. State the condition for mechanical energy conservation(역학적 에너지 보존 조건을 서술하라).',
     'Mechanical energy is conserved when the forces doing work are conservative and the remaining forces do no net work. Then T1 + V1 = T2 + V2. With nonconservative work, the change in T + V equals that work.',
     'Conservative(보존적)인 힘만 존재해야 한다고 좁히기보다 zero-work reaction(일을 하지 않는 반력)도 허용됨을 명시합니다. 뒤의 generalized balance(일반화된 수지)는 시험용 보강입니다.'),
    ('Q6. Distinguish power and work(일률과 일을 구별하라).',
     'Work measures energy transferred by a force through displacement. Power is the rate at which work is done, P = F dot v. Work is measured in joules, whereas power is measured in watts.',
     'Rate at which(…하는 비율)가 power(일률)의 정의입니다. 영어 답안의 P는 power(일률)이며 진자 예제의 tension(장력) P와 다른 용도입니다.'),
    ('Q7. Explain the spring deformation used in the energy equation(에너지식의 스프링 변형량을 설명하라).',
     'The deformation must be measured from the undeformed length of the spring. For an initial compression x0 and an additional compression d, the increase in elastic potential energy is one half k times [(x0 + d) squared minus x0 squared].',
     'Undeformed length(무변형 길이), initial compression(초기 압축), additional compression(추가 압축)을 구분합니다. 예제 2의 d는 이 답안에서 추가 압축량을 뜻하며 그룹 문제의 경사면 길이와 무관합니다.'),
    ('Q8. Determine the speed in the connected-block problem(연결 블록 문제의 속력을 구하라).',
     'The ideal inextensible cable gives equal speed magnitudes and equal travel distances for the two blocks. The tension work cancels in the combined system. Hence, (mB g - mu_k mA g)s = one half (mA + mB)v squared, giving v = 4.43 m/s. Block A moves to the right.',
     'Equal speed magnitudes(같은 속력 크기)라고 쓰면 서로 다른 vector directions(벡터 방향)를 혼동하지 않습니다. Cable(케이블)과 pulley(도르래)의 ideal assumptions(이상 가정)이 상쇄의 근거입니다.'),
    ('Q9. Explain why energy alone cannot determine the pendulum tension(에너지만으로 진자 장력을 정하지 못하는 이유를 설명하라).',
     'The tension is perpendicular to the motion and does no work, so it does not appear in the work–energy equation. First find the speed from energy, then apply the normal equation P - mg = m v squared / l. At the bottom, P = 3mg for release from rest at the horizontal position.',
     'Release from rest(정지 상태에서 놓기)와 horizontal position(수평 위치) 조건 없이 P=3mg를 일반화하지 않습니다.'),
    ('Q10. Determine the minimum crest radius(봉우리의 최소 반지름을 구하라).',
     'At the crest, the inward direction is downward, so mg - N = m v squared / rho. Contact requires N to be nonnegative. The limiting case N = 0 gives rho_min = v squared / g = 15 m. A radius greater than 15 m gives a positive normal force in this ideal model.',
     'Inward(안쪽), nonnegative(0 이상), limiting case(한계 상황)를 기억합니다. Minimum radius(최소 반지름) 15 m는 실제 설계 안전인증이 아니라 이 모형의 접촉 한계입니다.'),
    ('Q11. Explain the negative gravitational potential energy(음의 중력 위치에너지를 설명하라).',
     'For inverse-square gravity, choosing zero potential energy at infinity gives V = -GMm/r. The negative sign is a consequence of this reference choice. Moving the mass outward increases its potential energy, and gravity does negative work.',
     'At infinity(무한대에서), reference choice(기준 선택), outward(바깥쪽)를 반복 확인합니다. Negative potential energy(음의 위치에너지) 자체는 오류가 아닙니다.'),
    ('Q12. Set up the launch-angle limit(발사각 한계를 정식화하라).',
     'Use energy conservation to find the speed at the limiting perigee radius R + 200 km. Then use angular momentum conservation, r0 v0 sin(phi0) = r_min v_max. Since phi0 is measured from the radial direction, the error from horizontal is phi0 minus 90 degrees.',
     'Perigee radius(근지점 중심 거리)는 altitude(고도)가 아닙니다. Energy(에너지)는 속력, angular momentum(각운동량)은 방향 조건을 연결합니다. 본문 검산은 약 ±11.44°, 원본 표시는 ±11.5°입니다.'),
    ('Q13. Explain why kinetic friction cannot be represented by a position-only potential(운동마찰을 위치만의 위치에너지로 표현할 수 없는 이유를 설명하라).',
     'For sliding on a fixed rough surface, kinetic friction opposes the motion on both the outward and return paths. Its work over the round trip is negative rather than zero, so it cannot be represented by a potential that depends only on position.',
     'Fixed rough surface(고정된 거친 표면), round trip(왕복), depends only on position(위치에만 의존함)이 전제와 결론입니다. Friction(마찰)의 공간 방향은 바뀌어도 일의 음의 부호는 유지됩니다.'),
    ('Q14. Explain why the collar displacement is not the spring extension(칼라 이동거리와 스프링 신장량이 다른 이유를 설명하라).',
     'The collar moves vertically, but the spring is inclined. Its final length must be found from geometry: sqrt(0.200 squared + 0.150 squared) = 0.250 m. Subtracting the natural length gives a final extension of 0.150 m, compared with an initial extension of 0.100 m.',
     'Final extension(최종 신장량)은 0.150 m지만 additional extension(추가 신장량)은 0.050 m입니다. 수치가 같아 보이는 collar travel(칼라 이동거리) 0.150 m와 역할을 구분합니다.'),
]

terms = [
    ('work','일','힘과 변위의 내적을 경로를 따라 적분한 부호 있는 스칼라'),
    ('kinetic energy','운동에너지','입자의 운동 상태에 배정되는 T=½mv²'),
    ('potential energy','위치에너지','보존력이 한 일을 두 상태의 차이로 표현하는 함수 V'),
    ('mechanical energy','역학적 에너지','운동에너지와 위치에너지의 합 T+V'),
    ('dot product','내적','두 벡터 크기와 끼인각의 코사인을 곱하는 연산'),
    ('line integral','선적분','실제 이동 경로를 따라 미소 기여량을 적분하는 것'),
    ('scalar / vector','스칼라 / 벡터','방향 없는 양 / 크기와 방향을 갖는 양'),
    ('positive / negative / zero work','양의 / 음의 / 0인 일','힘과 변위의 내적 부호로 구분'),
    ('tangential component','접선 성분','경로의 순간 진행 방향으로 투영한 성분'),
    ('normal component','법선 성분','경로에 수직인 성분'),
    ('normal force / normal reaction','수직항력 / 법선 반력','접촉면에 수직으로 작용하는 구속 반력'),
    ('perpendicular / parallel','수직인 / 평행한','끼인각 90° / 평행 방향 관계'),
    ('acute / obtuse angle','예각 / 둔각','90°보다 작은 / 90°보다 큰 끼인각'),
    ('displacement / path length','변위 / 경로 길이','방향을 가진 위치 변화 / 실제 이동거리'),
    ('finite / infinitesimal','유한한 / 무한소의','유한 구간 / 미분에서의 미소량'),
    ('constant / variable force','일정한 / 변하는 힘','적분 밖에 둘 수 있는 힘 / 위치 등에 따라 바뀌는 힘'),
    ('weight / mass','중량 / 질량','중력에 의한 힘 W=mg / 운동 관성의 크기 m'),
    ('elevation / datum','높이 / 기준 높이','선택한 기준에 대한 높이 / 높이의 영점'),
    ('spring constant','스프링 상수','선형 스프링의 힘–변형량 비 k, 단위 N/m'),
    ('deflection / deformation','변형량 / 변형','자연 상태에서 변한 길이 또는 형상'),
    ('undeformed / undeflected / natural length','무변형의 / 변형되지 않은 / 자연길이','스프링이 늘거나 눌리지 않은 기준 상태와 길이'),
    ('extension / compression','신장 / 압축','스프링이 길어짐 / 짧아짐'),
    ('initially compressed / preloaded','처음부터 압축된 / 사전 하중을 받은','추가 운동 전에 이미 탄성에너지가 저장된 상태'),
    ('restoring force','복원력','변형된 물체를 자연 상태로 되돌리려는 힘'),
    ('rebound','되튐','스프링 등으로 운동 방향이 반전된 뒤의 운동'),
    ('maximum compression','최대 압축','운동 구간에서 스프링 압축량이 가장 큰 순간'),
    ('conservative / nonconservative','보존적인 / 비보존적인','위치에너지 함수로 일을 표현할 수 있음 / 그 형태로 일반 표현할 수 없음'),
    ('path-independent','경로에 무관한','두 끝점이 같으면 어떤 경로에서도 같은 값을 갖는'),
    ('closed path / round trip','닫힌 경로 / 왕복','출발점과 도착점이 일치하는 경로 / 갔다 돌아오는 이동'),
    ('gradient / partial derivative','기울기 벡터 / 편미분','함수 증가 방향을 나타내는 벡터 / 다른 변수를 고정한 미분'),
    ('conservation / conserved','보존 / 보존되는','해당 조건에서 물리량이 변하지 않는 성질'),
    ('dissipation / thermal energy','소산 / 열에너지','역학적 에너지가 다른 형태로 전환되는 과정 / 열적 에너지'),
    ('power / average power','일률 / 평균 일률','일을 하는 순간 비율 / 구간의 일÷시간'),
    ('efficiency / useful output','효율 / 유용한 출력','유용한 출력과 입력의 비 / 목적에 사용되는 출력'),
    ('joule / watt / horsepower','줄 / 와트 / 마력','일·에너지 / 일률 / 일률을 나타내는 단위'),
    ('released from rest / starts from rest','정지 상태에서 놓인 / 정지 출발하는','초기 속력이 0임을 뜻하는 조건'),
    ('inextensible / weightless / frictionless','늘어나지 않는 / 무게 없는 / 마찰 없는','케이블·도르래·면의 이상화 조건'),
    ('kinetic friction / coefficient','운동마찰 / 계수','미끄럼을 거스르는 마찰 / 여기서는 f=μₖN의 무차원 비'),
    ('combined system / internal force','결합계 / 내력','여러 물체를 함께 선택한 계 / 그 계 내부 물체 사이의 힘'),
    ('tension / cable constraint','장력 / 케이블 구속조건','줄의 당기는 힘 / 길이 일정으로 얻는 운동 관계'),
    ('free-body diagram','자유물체도','선택한 물체에 작용하는 외력을 표시한 그림'),
    ('bob / pendulum / collar','진자 추 / 진자 / 칼라','진자의 집중 질량 부분 / 매달려 흔들리는 계 / 봉을 따라 미끄러지는 부품'),
    ('radius of curvature / crest','곡률반지름 / 봉우리','국소적인 휘어짐의 반지름 / 위로 볼록한 경로 정상부'),
    ('inward / outward','안쪽 / 바깥쪽','곡률중심 또는 힘의 중심을 향함 / 그 반대'),
    ('nonnegative / limiting case','0 이상인 / 한계 상황','음수가 아닌 값 / 부등식 경계가 등식이 되는 경우'),
    ('contact maintained / loss of contact','접촉 유지 / 접촉 상실','지지 반력이 가능한 운동 / 표면으로부터 이탈하는 상태'),
    ('central force / angular momentum','중심력 / 각운동량','작용선이 고정 중심을 지나는 힘 / r×mv'),
    ('altitude / radial distance','고도 / 중심 거리','표면에서 잰 높이 / 천체 중심에서 잰 거리'),
    ('perigee / apogee','근지점 / 원지점','지구 중심에 가장 가까운 / 가장 먼 궤도 위치'),
    ('launch-angle error / allowable','발사각 오차 / 허용되는','지정 발사 방향과의 차이 / 조건을 만족하는 범위'),
    ('determine / evaluate / neglect','구하라 / 계산하라 / 무시하라','시험 지시 동사: 미지수 결정 / 수치 평가 / 모델에서 제외'),
    ('assume / substitute / combine','가정하라 / 대입하라 / 결합하라','전제 설정 / 식에 값 삽입 / 여러 관계를 함께 사용'),
]

audit = [
    ('Overview 00:42–00:59','break / breaking','brake / braking(제동하다 / 제동)','skid mark(미끄럼 자국)와 감속 문맥'),
    ('Contents 1 02:09·04:30·15:19','inputs / mess / trippy zoidal','impulse(충격량) / mass(질량) / trapezoid(사다리꼴)','원본 8·12·22장'),
    ('Contents 1 12:50·19:13 / Contents 2 11:14·14:07','work is always negative','변형 증가·중심 거리 증가 구간에만 음의 일','적분 방향을 반대로 하면 양의 일이 됨'),
    ('원본 21','x₂&lt;x₁이면 양의 스프링 일','일반 조건은 x₂²&lt;x₁²','양의 신장량 그림을 압축까지 일반화하지 않음'),
    ('원본 37','∫mv dv = ½mv₁²','½mv₂²−½mv₁²','정적분과 같은 장의 T₂−T₁'),
    ('원본 39','크기·부호는 있고 방향은 없다는 문구','진자 추의 조건으로 사용하지 않음','work(일) 설명이 반복된 문맥 불일치'),
    ('원본 43 · Contents 1 35:33·36:11','ΣEₙ / freeway diagram / row times velocity squared','ΣFₙ / free-body diagram(자유물체도) / v²/ρ','원본 힘의 평형이 아닌 법선 운동방정식'),
    ('Contents 2 00:34–01:26','zero per second / what / deficiency / Ada','joule per second(초당 줄) / watt(와트) / efficiency(효율) / η','원본 45–46의 단위·정의'),
    ('원본 48–49 · Contents 2 04:48–05:24','normal force: No','일 0인 이상 구속 반력으로 처리','별도 위치에너지 항을 정의하지 않는 문맥; 보존력의 일반 판정으로 확장하지 않음'),
    ('원본 58','∂Y/∂z 및 단위벡터 누락','∂V/∂z, <b>F</b>=−∇V','앞줄의 전미분과 각 힘 성분 비교'),
    ('원본 62','V₀=0','최저점의 V₂=0','상태 1과 2를 연결하는 그림·에너지식'),
    ('원본 63 · Contents 2 23:26','초기 sinφ 및 conservative force만 언급','sinφ₀, conservative central force(보존 중심력)','슬라이드 제목과 고정 중심에 대한 영 모멘트 조건'),
    ('원본 70','300×9.81=2960, −F꜀(2)−2940(2)','2943 N, 중량의 일은 +2943(2)','하향 변위·중량 방향 및 원본 71의 양의 항'),
    ('원본 71·74·76','전체 일 4900 J','반올림 없는 4905 J와 구별','원본 질량·g·μₖ 대입; 최종 v≈4.43 m/s는 일치'),
    ('원본 75','total work 질문 아래 T₂ 식 반복','T₂=250v², 전체 일은 앞 장 참조','work(일)와 kinetic energy(운동에너지)의 역할 구별'),
    ('원본 77 · Problem Solving 07:27–07:54','maximum deflection 40 mm','추가 압축 40 mm, 총 압축 160 mm','원본 80–81의 그림·힘 계산'),
    ('원본 80–81','마찰 대입 부호 누락, Pmax=2400 N','Uf=−376.704μₖ J, Pmax=3200 N','힘의 방향 및 0.120+0.040 m'),
    ('Problem Solving 11:50–12:30','마찰만으로 풀이하다 스프링 항 추가','최종식에 두 일을 모두 반영','영상의 후속 정정과 원본 81'),
    ('원본 84 · Problem Solving 16:52–17:15','spring returns all of its energy','추가 저장분 112 J 반환; 사전 저장 144 J 유지','초기·최종 압축량과 케이블 제한'),
    ('원본 88·90','N=5W(1000)(9.81), 에너지 풀이 제목 반복','N=5W=5(1000)(9.81); 90장은 법선 운동방정식','차원 및 실제 표시식'),
    ('Problem Solving 18:33·23:23–23:37','반지름을 늘리면 속력 감소 / 15 m 미만에서 5W 초과','같은 높이에서는 속력 동일; 봉우리는 N₃≥0 조건','원본 87–90의 에너지식과 법선식'),
    ('Problem Solving 17:07·25:14–28:27','observe / color','absorb(흡수하다) / collar(칼라)','원본 84·95–99의 물체와 설명'),
    ('원본 97–98','2500 mm, Vg=(9.81)(−0.15)','250 mm, Vg=(10)(9.81)(−0.15)','200–150–250 삼각형, 질량 10 kg'),
    ('원본 106·109','60400 km, ±11.5°','원본 답 유지 + 검산 60333 km, ±11.44° 병기','g=9.81, R=6370 km, v₀=10250 m/s로 재계산'),
    ('Problem Solving 30:27·33:24–33:41','horse / sine of v0 / 15 of 11.5','Earth(지구) / sinφ₀ / 원본 ±11.5°','원본 102–109의 기호·수치'),
    ('Summary 00:57–01:07','cannot compute forces','일을 하지 않는 미지 반력은 직접 결정 불가','에너지 식에 나타나는 미지 힘까지 모두 불가능하다는 뜻으로 확대하지 않음'),
]

roadmap = '''<section class="editorial-section section-divider" id="course-roadmap" aria-labelledby="roadmap-title">
<p class="section-kicker">Summary video · Course roadmap</p>
<h2 class="section-title" id="roadmap-title">Summary 영상 후반: 다음은 충격량과 운동량입니다.</h2>
<p class="section-lead">Summary 00:17–01:07의 앞부분은 work–energy principle(일·에너지 원리), conservative force(보존력), mechanical energy(역학적 에너지) 보존과 방법의 한계를 복습하므로 핵심 개념 요약에 반영했습니다. 00:57 구간 끝의 “next week”부터는 다음 강의 안내로 구분합니다.</p>
</section>
<section class="editorial-section" id="roadmap-detail" aria-labelledby="roadmap-detail-title">
<p class="section-kicker">What comes next</p>
<h2 class="section-title" id="roadmap-detail-title">변위에 대한 적분에서 시간에 대한 적분으로.</h2>
<div class="card"><h3>Impulse and momentum(충격량과 운동량)</h3><p>다음 단원에서는 force(힘)를 time(시간)에 대해 적분하는 impulse(충격량), momentum(운동량)의 보존, collision(충돌) 전후 입자의 운동을 다룹니다. 현재 강의 인덱스에서는 Week 06 · 2026-10-07 · Lecture 7입니다. 이 예고를 이번 강의의 개념 복습과 혼합하지 않습니다.</p></div>
<div class="evidence"><span>Summary 00:57–01:26</span><span>강의 인덱스 대조</span></div>
</section>'''

template = (SITE / 'templates/lecture-page.template.html').read_text(encoding='utf-8')
source_pattern = r'<section class="source-section"[\s\S]*?</section>'
source_template = re.search(source_pattern, template).group()
sections = []
for n, (title, evidence, blocks, role) in enumerate(records, 1):
    section = source_template
    values = {'NN': f'{n:02d}', 'SLIDE_ROLE': role, 'SLIDE_HEADING': title,
              'LECTURE_SLUG': 'lecture06', 'DESCRIPTIVE_ALT_TEXT': f'Lecture 6 원본 슬라이드 {n:02d}: {escape(title)}',
              'CURRENT_PAGE': str(n), 'PAGE_COUNT': '111', 'TRANSCRIPT_TIME_OR_SLIDE_ROLE': evidence,
              'SLIDE_EXPLANATION_BLOCKS': blocks}
    for key, value in values.items():
        section = section.replace('{{'+key+'}}', value)
    sections.append(section)
template = re.sub(source_pattern, lambda _: '\n\n'.join(sections), template, count=1)
exam_html = ''.join('<div class="exam-card"><h3>'+q+'</h3><div class="answer"><span class="answer__label">Model answer</span>'+escape(a)+'</div><p style="margin-top: 12px">'+ko+'</p></div>' for q,a,ko in exam_items)
template = re.sub(r'<div class="exam-card">\s*<h3>\{\{EXAM_QUESTION\}\}</h3>[\s\S]*?</div>\s*</div>', lambda _: exam_html+'\n          </div>', template, count=1)
videos = [('Overview','TyDEbI-RBGE'),('Contents 1','0gohr-4TtS0'),('Contents 2','K3mFnZandvc'),('Problem Solving','-flNXvW8oTU'),('Summary','EQmTc_5-4hQ')]
toc = [('overview','전체 개요'),('concept-map','개념 지도'),('concept-summary','핵심 개념 요약')] + [(f'slide-{i:02d}',f'{i:02d} · {row[0]}') for i,row in enumerate(records,1)] + [('course-roadmap','Summary · 다음 단원 안내'),('exam-english','시험 영어'),('glossary','용어집'),('asr-log','원본·스크립트 교정'),('sources','출처')]
values = {
    'LECTURE_NUMBER':'Lecture 6', 'LECTURE_TITLE':'Work and Energy Principle',
    'ONE_SENTENCE_DESCRIPTION':'5주차 일과 에너지 원리: 원본 111장과 영어 영상 5개를 대조한 한국어 수업 대체 학습 노트',
    'WEEK':'Week 05', 'DATE_OR_날짜_미기재':'2026-09-30', 'PAGE_COUNT':'111',
    'LECTURE_PROMISE':'Work(일)에서 kinetic energy(운동에너지)와 potential energy(위치에너지)를 연결하고, 스프링·마찰·곡선 트랙·위성의 운동을 수식 유도와 예제로 설명합니다.',
    'VIDEO_SET':'Overview · Contents 1·2 · Problem Solving · Summary',
    'ALL_CONTENTS_AND_PROBLEM_SOLVING_BUTTONS':'\n'.join(f'<a class="button button--primary" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상 열기</a>' for label,vid in videos[1:4]),
    'ORIGINAL_PDF_URL':'https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/lecture06_note.pdf',
    'LECTURE_NOTE_FILENAME':'lecture06_note.pdf',
    'CORE_RELATIONSHIP_HEADLINE':'힘이 한 일로, 이동 전후의 속력을 연결합니다.',
    'CORE_RELATIONSHIP_EXPLANATION':'Work(일)는 force(힘)가 displacement(변위)를 따라 전달한 에너지를 나타냅니다. 그 일이 kinetic energy(운동에너지)를 바꾸며, conservative force(보존력)는 potential energy(위치에너지)의 차로 다시 표현할 수 있습니다. 속력을 구한 뒤 필요한 반력은 Newton’s second law(뉴턴 제2법칙)로 연결합니다.',
    'CONCEPT_MAP_HEADLINE':'일의 정의에서 보존식과 문제풀이까지.',
    'CONCEPT_MAP_BLOCKS':'<div class="grid-3">'+card('Work(일)','힘과 변위의 내적을 적분합니다. 부호와 실제 이동 경로를 확인합니다.')+card('Energy(에너지)','T₁+ΣU=T₂를 쓰고 보존력의 일을 V₁−V₂로 바꿉니다.')+card('Application(적용)','마찰·스프링·구속관계를 반영합니다. 반력이 필요하면 ΣFₙ=mv²/ρ를 추가합니다.')+'</div>',
    'STANDALONE_CONCEPT_SUMMARY':summary,
    'DISTINCT_SUMMARY_VIDEO_SECTION_IF_NEEDED':roadmap,
    'EXAM_SECTION_TITLE':'일과 에너지를 설명하는 영어 답안',
    'BILINGUAL_GLOSSARY_TABLE':table(['영어(한국어)','의미와 사용'],[(f'{en}({ko})',escape(meaning)) for en,ko,meaning in terms]),
    'AUDIT_SECTION_TITLE':'원본 슬라이드·자동생성 스크립트 교정 기록',
    'ASR_CORRECTION_TABLE':p('원본 PDF와 영어 자동생성 자막은 수정하지 않았습니다. 표는 본문에 채택한 해석을 설명합니다. 자막의 오표기가 실제 발화인지 인식 오류인지는 별도의 음성 판독 없이 단정하지 않습니다. 원본의 중요한 수식·부호·조건 문제는 해당 슬라이드 아래에도 표시했습니다.')+table(['위치','원문 또는 문제','본문 처리','근거'],audit),
    'SOURCE_LIST_AND_PROVENANCE_NOTE':'<ul class="plain-list"><li>원본 PDF: Lecture 6, MC2103, Fall 2026, 111장.</li>'+''.join(f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상</a> · 영어 자동생성 원문, 2026-09-28 확보.</li>' for label,vid in videos)+'<li>주차·날짜: 보존된 강의 인덱스, Week 05 · 2026-09-30.</li></ul>'+p('원본 111장을 그림과 함께 확인하고 영어 원문 자막 5편을 대조했습니다. 시간 표시는 관련 설명 구간이며 정확한 슬라이드 전환 시각을 뜻하지 않습니다. 원본 3장의 보조 링크는 보존하되 해당 영상은 설명 근거에 포함하지 않았습니다. Summary의 현재 단원 복습은 개념 요약에 반영하고 다음 단원 예고는 분리했습니다.')+p('생략된 대수 단계, 적용 조건, 일반화된 비보존 일의 식, 추가 검산, 그룹 문제의 완성 계산은 시험용 보강 또는 편집자 보강입니다. 특히 그룹 문제의 6.71 m는 원본에 없는 모델 기반 보강 답이며 연결부 가정을 함께 명시했습니다. 위성 계산은 원본의 R=6370 km, g=9.81 m/s²를 사용했습니다.'),
    'TABLE_OF_CONTENTS_LINKS':''.join(f'<li><a href="#{id}">{label}</a></li>' for id,label in toc),
}
for key,value in values.items():
    template = template.replace('{{'+key+'}}',value)
template = template.replace('이 부분만 읽어도 렉처의 핵심 정의, 개념 관계, 가정과 풀이 흐름을 이해할 수 있도록 작성합니다.','일의 부호와 적분, 운동에너지, 위치에너지와 보존 조건, 다섯 예제의 풀이 흐름을 연결한 독립형 요약입니다. 원본과 본강의·Summary의 실제 개념 복습을 종합했으며, 아래에서 모든 슬라이드의 상세 해설을 이어갑니다.')
template = re.sub(r'\s*<!--[\s\S]*?-->', '', template)
template = '\n'.join(line.rstrip() for line in template.splitlines())+'\n'
assert not re.search(r'\{\{[^}]+\}\}',template)
(SITE/'lecture06.html').write_text(template,encoding='utf-8')
print(f'BUILT lecture06.html: {len(records)} source sections, {len(exam_items)} exam cards, {len(terms)} terms')
