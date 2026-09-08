"""Fill the Lecture 1-derived template with reviewed Lecture 3 content."""
from pathlib import Path
import re
from html import escape

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
records = []

def p(text):
    return '<p>' + text + '</p>'

def card(title, *body, kind='card'):
    return f'<div class="{kind}"><h3>{title}</h3>' + ''.join(p(x) for x in body) + '</div>'

def formula(text):
    return '<span class="formula">' + text + '</span>'

def add(title, evidence, *body, eq='', extra='', role='Concept'):
    blocks = card('핵심 해설' if role == 'Concept' else '슬라이드 안내', *body,
                  kind='card' if role == 'Concept' else 'quiet-card')
    if eq:
        blocks += card('식과 기호', formula(eq))
    records.append((title, evidence, blocks + extra, role))

add('Lecture 3 표지', 'MC2103 · Fall 2026', 'Kinematics of particles II: Curvilinear Motion(입자의 운동학 II: 곡선운동)의 표지입니다.', role='Title')
add('Lecture 3-1 구분', '원본 구분 슬라이드', '첫 도입 구간의 구분 슬라이드입니다.', role='Divider')
add('도입 참고 영상 링크', '원본 영상 링크', '<a href="https://youtu.be/3fFWPCQpggQ" target="_blank" rel="noreferrer">원본 슬라이드에 기재된 참고 영상 열기</a>. 이 링크 슬라이드는 그대로 보존하며, 아래 해설은 강의 인덱스의 본강의 5개 영상과 원본 PDF를 근거로 합니다.', role='Video link')
add('Lecture 3-2 · 벡터와 직교좌표', 'Contents 1', 'Position(위치), velocity(속도), acceleration(가속도)을 vector(벡터)로 정의하고 rectangular coordinates(직교좌표)와 relative motion(상대운동)을 다루는 구간입니다.', role='Divider')
add('곡선을 따라 움직이는 입자', 'Contents 1 00:17–00:37',
    'Curvilinear motion(곡선운동)은 particle(입자)이 straight line(직선)이 아닌 curve(곡선)를 따라 움직이는 운동입니다. 그림의 snowboarder(스노보더)와 train(기차)은 이동하면서 진행 방향도 달라집니다. 실제 물체 전체의 회전보다 한 점의 이동 경로를 추적하는 particle model(입자 모델)을 사용합니다.',
    'Rectilinear motion(직선운동)에서는 고정된 한 축의 부호로 방향을 표현할 수 있었지만, curvilinear motion(곡선운동)에서는 방향 자체가 달라집니다. 따라서 speed(속력)가 일정해도 velocity(속도)가 변할 수 있으며 acceleration(가속도)이 생깁니다. 이번 단원은 이 변화를 여러 coordinate systems(좌표계)로 표현하는 방법을 다룹니다.')
add('위치벡터와 변위는 서로 다른 화살표입니다', 'Contents 1 00:41–01:54',
    'Position vector(위치벡터) <b>r</b>는 fixed reference frame(고정 기준좌표계)의 origin(원점) O에서 현재 particle(입자) P로 향합니다. 시간이 Δt만큼 지나 P′로 이동하면 새 position vector(위치벡터)는 <b>r</b>′입니다. 두 position vectors(위치벡터)의 차가 displacement vector(변위벡터) Δ<b>r</b>입니다.',
    '그림에서 Δ<b>r</b>는 P에서 P′로 바로 연결한 chord(현)이고, Δs는 실제 curve(곡선)를 따라 이동한 arc length(호의 길이)입니다. 유한한 구간에서는 |Δ<b>r</b>|와 Δs가 일반적으로 다릅니다. Position vector(위치벡터)는 원점 선택에 의존하지만, 같은 고정 좌표축으로 표현한 두 점 사이 displacement(변위)는 원점을 평행이동해도 같습니다.',
    eq='Δ<b>r</b> = <b>r</b>(t + Δt) − <b>r</b>(t)')
add('순간속도는 접선 방향, 속력은 그 크기입니다', 'Contents 1 02:00–02:26',
    'Average velocity(평균속도)는 Δ<b>r</b>/Δt입니다. Δt를 0으로 보내면 두 점을 잇는 chord(현)가 그 점의 tangent(접선)에 접근하여 instantaneous velocity(순간속도) <b>v</b> = d<b>r</b>/dt를 얻습니다. 움직이는 particle(입자)의 velocity(속도)는 경로의 tangent direction(접선 방향)을 향합니다.',
    'Instantaneous speed(순간속력) v는 velocity vector(속도벡터)의 magnitude(크기)이며 scalar(스칼라)입니다. s를 이동 방향으로 증가하는 distance along the path(경로를 따른 이동거리)로 잡으면 v = ds/dt입니다. 유한 구간의 average speed(평균속력) Δs/Δt와 average velocity magnitude(평균속도의 크기) |Δ<b>r</b>|/Δt를 동일시하면 안 됩니다.',
    eq='<b>v</b> = d<b>r</b>/dt &nbsp;·&nbsp; v = |<b>v</b>| = ds/dt')
add('가속도는 속도벡터 전체의 변화율입니다', 'Contents 1 02:35–03:20',
    'Velocity vectors(속도벡터) <b>v</b>와 <b>v</b>′를 같은 시작점으로 옮겨 그린 뒤 빼면 Δ<b>v</b>를 얻습니다. Instantaneous acceleration(순간가속도)은 Δ<b>v</b>/Δt의 극한입니다. Speed(속력)의 변화뿐 아니라 direction(방향)의 변화도 acceleration(가속도)에 포함됩니다.',
    'Acceleration(가속도)은 일반적으로 velocity(속도)와 parallel(평행)하지도 perpendicular(수직)하지도 않습니다. Speed(속력)가 변하면서 회전하면 두 효과가 함께 나타납니다. Constant-speed circular motion(등속 원운동)처럼 speed(속력)가 일정한 경우에만 acceleration(가속도)이 velocity(속도)에 perpendicular(수직)인 특별한 상황이 나타납니다.',
    eq='<b>a</b> = d<b>v</b>/dt = d²<b>r</b>/dt²',
    extra=card('원문 대조', '슬라이드는 “not tangent”, 자동생성 스크립트 03:13–03:20은 “not perpendicular”로 표현합니다. 둘 중 하나를 보편적 방향 규칙으로 외우지 말고, acceleration(가속도)은 크기 변화와 방향 변화의 합이라는 정의로 이해합니다.', kind='callout'))
add('직교좌표에서는 고정된 단위벡터를 사용합니다', 'Contents 1 03:31–04:39',
    'Rectangular coordinates(직교좌표), 또는 Cartesian coordinates(데카르트 좌표)에서 <b>i</b>, <b>j</b>, <b>k</b>는 x, y, z축의 unit vectors(단위벡터)입니다. 여기서는 축의 방향이 fixed(고정)되어 있으므로 이 unit vectors(단위벡터)의 시간 미분은 0입니다.',
    '따라서 position vector(위치벡터)를 미분할 때 x(t), y(t), z(t)만 미분하면 됩니다. 점 하나는 first time derivative(시간에 대한 1차 미분), 점 두 개는 second time derivative(시간에 대한 2차 미분)입니다. <b>v</b>의 각 component(성분)는 부호를 가질 수 있고, speed(속력)는 √(vₓ²+vᵧ²+v_z²)로 구합니다.',
    eq='<b>r</b> = x<b>i</b> + y<b>j</b> + z<b>k</b><br><b>v</b> = ẋ<b>i</b> + ẏ<b>j</b> + ż<b>k</b><br><b>a</b> = ẍ<b>i</b> + ÿ<b>j</b> + z̈<b>k</b>')
add('포물선운동: 방향별 가속도부터 정합니다', 'Contents 1 04:46–05:27',
    'Projectile motion(포물선운동)을 x-y 평면에서 표현합니다. Upward(위쪽)를 +y로 정하면 gravity(중력)에 의한 acceleration(가속도)은 −g<b>j</b>입니다. Horizontal(수평) acceleration(가속도)은 0이고, 초기 z방향 velocity(속도)가 0이면 계속 z = 0입니다.',
    '이 모델은 air resistance(공기저항)를 neglect(무시)하고 g를 constant(일정)하게 취급하는 범위에서 성립합니다. Initial position(초기위치)을 origin(원점)으로 잡되 initial velocity(초기속도)의 x·y 성분은 주어진 발사 조건을 사용합니다. 초기속도가 전부 0이라는 뜻이 아닙니다.',
    eq='aₓ = 0, aᵧ = −g, a_z = 0<br>x₀ = y₀ = z₀ = 0, &nbsp; v_z₀ = 0')
add('적분 두 번으로 포물선운동의 위치를 구합니다', 'Contents 1 05:34–05:37',
    'Acceleration(가속도)을 한 번 integrate(적분)하면 velocity(속도), 다시 integrate(적분)하면 position(위치)입니다. 각 단계에서 initial condition(초기조건)을 넣어 적분상수를 결정합니다. Horizontal velocity(수평속도)는 일정하고 vertical velocity(수직속도)는 시간에 따라 선형으로 감소합니다.',
    '원본 y식의 vᵧ₀y 표기는 vᵧ₀t로 교정해야 합니다. Velocity(속도)에 time(시간)을 곱해야 length(길이)가 되며, 올바른 식을 미분하면 vᵧ = vᵧ₀ − gt로 돌아옵니다. 최고점에서 vᵧ = 0이어도 vₓ가 남아 있으므로 projectile(투사체)이 일반적으로 완전히 멈추지는 않습니다.',
    eq='vₓ = vₓ₀, &nbsp; vᵧ = vᵧ₀ − gt<br>x = vₓ₀t, &nbsp; y = vᵧ₀t − ½gt², &nbsp; z = 0')
add('두 직선운동은 같은 시간을 공유합니다', 'Contents 1 05:45–05:58',
    'Horizontal motion(수평운동)은 uniform motion(등속운동), vertical motion(수직운동)은 uniformly accelerated motion(등가속도운동)입니다. 각 방향의 식은 independently(독립적으로) 계산할 수 있지만, 같은 particle(입자)의 운동이므로 두 식에는 동일한 time(시간) t를 넣습니다.',
    '예를 들어 특정 horizontal position(수평위치)에 도달하는 시간을 x식으로 구한 후 그 시간을 y식에 넣으면 그때의 height(높이)를 알 수 있습니다. “독립”은 서로 다른 시간을 사용한다는 뜻이 아니라, 각 component equation(성분 방정식)을 따로 적분할 수 있다는 뜻입니다.')
add('움직이는 배에서 본 헬리콥터', 'Contents 1 06:06–06:20',
    'Relative motion(상대운동)은 다른 observer(관측자)를 기준으로 본 운동입니다. Helicopter(헬리콥터)가 aircraft carrier(항공모함)에 착륙하려면 지면 기준의 velocity(속도)보다 배에 대한 relative velocity(상대속도)가 중요합니다.',
    '두 물체가 지면에 대해 같은 velocity vector(속도벡터)로 움직이면 relative velocity(상대속도)는 0입니다. 같은 speed(속력)만으로는 충분하지 않으며 direction(방향)까지 같아야 합니다.')
add('고정좌표계와 병진하는 좌표계', 'Contents 1 06:25–07:18',
    'Oxyz를 fixed frame(고정좌표계), A를 origin(원점)으로 갖는 Ax′y′z′를 moving frame(이동좌표계)으로 둡니다. <b>r</b>ₐ와 <b>r</b>ᵦ는 모두 O에서 측정한 absolute position vectors(절대위치벡터)이고, <b>r</b>ᵦ/ₐ는 A에서 B를 향하는 relative position vector(상대위치벡터)입니다.',
    '이 절의 핵심 조건은 frame in translation(병진하는 좌표계)입니다. Moving frame(이동좌표계)의 축 방향은 고정좌표계에 대해 회전하지 않습니다. Translation(병진)은 반드시 straight-line motion(직선운동)만을 뜻하지 않으며, 원점이 곡선을 따라가더라도 축이 회전하지 않으면 이 조건을 만족할 수 있습니다.')
add('상대운동은 B에서 A를 뺍니다', 'Contents 1 07:21–07:55',
    'O에서 A를 거쳐 B로 가는 vector addition(벡터 합)을 쓰면 <b>r</b>ᵦ = <b>r</b>ₐ + <b>r</b>ᵦ/ₐ입니다. “B relative to A(B의 A에 대한)”는 관측 대상 B에서 기준 A를 빼는 순서로 기억합니다. 순서를 바꾸면 모든 relative vectors(상대벡터)의 부호가 반대가 됩니다.',
    'Position relation(위치 관계)을 시간에 대해 미분하여 velocity relation(속도 관계), 다시 미분하여 acceleration relation(가속도 관계)을 얻습니다. 아래 식에서 relative velocity(상대속도)와 relative acceleration(상대가속도)을 moving frame(이동좌표계)의 측정값으로 그대로 해석하는 데에는 nonrotating axes(회전하지 않는 축) 조건이 필요합니다.',
    eq='<b>r</b>ᵦ/ₐ = <b>r</b>ᵦ − <b>r</b>ₐ<br><b>v</b>ᵦ/ₐ = <b>v</b>ᵦ − <b>v</b>ₐ<br><b>a</b>ᵦ/ₐ = <b>a</b>ᵦ − <b>a</b>ₐ')
add('절대운동을 관측자 운동과 상대운동으로 합성합니다', 'Contents 1 08:02–08:12',
    'Absolute motion(절대운동)은 기준 A의 motion(운동)과 A에서 본 B의 relative motion(상대운동)을 vector sum(벡터 합)으로 합성한 결과입니다. 서로 다른 방향의 두 speed(속력)를 단순히 더하지 말고 같은 coordinate basis(좌표 기저)로 표현한 velocity vectors(속도벡터)를 더합니다.',
    '편집자 보강: 배가 east(동쪽)로 10 m/s, 배에서 본 물체가 north(북쪽)로 6 m/s라면 지면 기준 <b>v</b> = 10<b>i</b> + 6<b>j</b> m/s입니다. Speed(속력)는 16 m/s가 아니라 √136 ≈ 11.66 m/s입니다. 다음 예제에서는 이 합성을 거꾸로 하여 relative motion(상대운동)을 구합니다.')
add('Lecture 3-3 · 경로좌표와 극좌표', 'Contents 2', 'Path coordinates(경로좌표)와 polar coordinates(극좌표)의 unit vectors(단위벡터)가 회전할 때 velocity(속도)와 acceleration(가속도)을 미분하는 방법을 다룹니다.', role='Divider')
add('경로를 알면 접선·법선으로 나눕니다', 'Contents 2 00:17–00:45',
    'Track(궤도)나 road(도로)처럼 path(경로)가 주어지면 tangential-normal coordinates(접선·법선 좌표), 즉 path coordinates(경로좌표)가 편리합니다. “얼마나 빨라지는가?”와 “얼마나 방향을 바꾸는가?”를 직접 분리할 수 있기 때문입니다.',
    'Rectangular coordinates(직교좌표)의 x·y축은 공간에 고정되어 있지만, path coordinates(경로좌표)의 unit vectors(단위벡터)는 particle(입자)이 있는 점의 path(경로)에 맞춰 바뀝니다. 길이를 1로 유지한다고 해서 그 vector(벡터)의 미분이 0인 것은 아닙니다.')
add('접선·법선 성분의 정의', 'Contents 2 00:48–01:42',
    'Unit tangent(단위접선벡터) <b>e</b>ₜ는 현재 motion(운동)의 tangent direction(접선 방향)을 향하고, principal normal(주법선) <b>e</b>ₙ은 이에 perpendicular(수직)이며 곡선 안쪽 center of curvature(곡률중심)를 향합니다. ρ는 instantaneous radius of curvature(순간곡률반경)입니다.',
    'Velocity(속도)는 v<b>e</b>ₜ 하나로 표현되지만 acceleration(가속도)에는 두 component(성분)가 있습니다. Tangential acceleration(접선가속도) aₜ는 speed(속력)를 바꾸고 normal acceleration(법선가속도) aₙ은 direction(방향)을 바꿉니다. ρ는 경로가 현재 얼마나 완만한지 나타내며 임의 origin(원점)에서 잰 거리 r와 다릅니다.',
    eq='<b>v</b> = v<b>e</b>ₜ<br><b>a</b> = (dv/dt)<b>e</b>ₜ + (v²/ρ)<b>e</b>ₙ')
add('방향이 바뀌는 단위벡터를 비교합니다', 'Contents 2 01:53–02:28',
    '그림 왼쪽은 particle(입자)이 P에서 P′로 이동하는 실제 path(경로), 오른쪽은 두 unit tangent vectors(단위접선벡터)를 같은 시작점 O′로 옮겨 비교한 그림입니다. 오른쪽 원의 radius(반지름) 1은 unit vector(단위벡터)의 길이이며 실제 path(경로)의 radius of curvature(곡률반경) ρ가 아닙니다.',
    '두 unit vectors(단위벡터)의 magnitude(크기)는 모두 1이지만 방향이 Δθ만큼 변하므로 Δ<b>e</b>ₜ가 0이 아닙니다. 이 direction change(방향 변화)를 시간에 대한 변화율로 환산하면 normal acceleration(법선가속도)을 얻게 됩니다.')
add('단위접선벡터를 미분하면 주법선이 됩니다', 'Contents 2 02:28–03:10',
    '같은 길이 1인 두 화살표가 만드는 isosceles triangle(이등변삼각형)에서 차벡터의 길이는 2 sin(Δθ/2)입니다. 이를 Δθ로 나누고 Δθ → 0의 limit(극한)을 취하면 sin u/u → 1이므로 크기가 1로 접근합니다.',
    '유한한 Δθ에서 차벡터는 두 방향의 중간에 대응하는 방향을 향하며, Δθ → 0일 때 현재 point(점)의 principal normal(주법선) 방향으로 접근합니다. 따라서 unit tangent(단위접선벡터)의 turning angle(회전각)에 대한 derivative(미분)는 <b>e</b>ₙ입니다.',
    eq='|Δ<b>e</b>ₜ| = 2 sin(Δθ/2)<br>d<b>e</b>ₜ/dθ = <b>e</b>ₙ')
add('곱의 미분과 연쇄법칙으로 v²/ρ를 유도합니다', 'Contents 2 03:17–05:34',
    'Velocity(속도) <b>v</b> = v<b>e</b>ₜ를 differentiate(미분)할 때 speed(속력) v와 unit tangent(단위접선벡터) <b>e</b>ₜ가 모두 시간에 의존합니다. Product rule(곱의 미분법)을 적용하여 v̇<b>e</b>ₜ + v d<b>e</b>ₜ/dt로 나눕니다. 두 번째 항을 생략하면 곡선운동의 방향 변화를 전부 놓칩니다.',
    'Chain rule(연쇄법칙)로 d<b>e</b>ₜ/dt = (d<b>e</b>ₜ/dθ)(dθ/ds)(ds/dt)입니다. 각각 <b>e</b>ₙ, 1/ρ, v를 대입하면 (v/ρ)<b>e</b>ₙ입니다. 여기에 앞의 v가 다시 곱해져 v²/ρ가 됩니다. 여기서 θ는 tangent(접선)의 회전각이며 뒤의 polar angle(극각)과 일반적으로 같지 않습니다.',
    eq='ds = ρ dθ, &nbsp; ds/dt = v<br>d<b>e</b>ₜ/dt = (v/ρ)<b>e</b>ₙ<br>aₜ = dv/dt, &nbsp; aₙ = v²/ρ')
add('접선가속도의 부호와 법선가속도의 방향', 'Contents 2 05:38–06:03',
    'Tangential acceleration(접선가속도) aₜ는 speeding up(빨라짐)이면 positive(양수), slowing down(느려짐)이면 negative(음수)입니다. Normal acceleration(법선가속도) aₙ = v²/ρ는 주법선 방향을 곡률중심 쪽으로 정한 관례에서 nonnegative(0 이상)입니다.',
    'Constant speed(일정한 속력)이면 aₜ = 0이지만 curved path(곡선 경로)에서 v ≠ 0이고 ρ가 유한하면 aₙ은 남습니다. Straight path(직선 경로)에서는 curvature(곡률)가 0이어서 normal contribution(법선 성분)이 사라집니다. Total acceleration magnitude(전체 가속도의 크기)는 두 perpendicular components(수직 성분)의 제곱합 제곱근입니다.',
    eq='|<b>a</b>| = √(aₜ² + aₙ²)')
add('공간곡선에서도 접선·법선 분해가 성립합니다', 'Contents 2 06:06–06:14',
    'Space curve(공간곡선)는 path(경로) 전체가 하나의 fixed plane(고정 평면)에 놓이지 않는 3차원 곡선입니다. 그래도 매 순간 velocity(속도)의 tangent direction(접선 방향)과 그 방향이 변하는 principal normal direction(주법선 방향)을 정할 수 있습니다.',
    '두 unit vectors(단위벡터)가 만드는 plane(평면)은 particle(입자)의 위치에 따라 바뀔 수 있지만, instantaneous acceleration(순간가속도)은 같은 aₜ = dv/dt, aₙ = v²/ρ 식으로 분해됩니다. “공간곡선이라서 가속도 성분이 반드시 세 개”라고 판단하지 않습니다.')
add('접촉평면은 접선과 주법선을 포함합니다', 'Contents 2 06:22–06:36',
    'Osculating plane(접촉평면)은 현재 point(점)의 unit tangent(단위접선벡터) <b>e</b>ₜ와 principal normal(주법선) <b>e</b>ₙ을 포함하는 plane(평면)입니다. 그림의 분홍색 평면 안에 두 vector(벡터)가 놓입니다.',
    '자동생성 스크립트에는 “oscillating plane”과 “perpendicular to both”가 나타나지만, 슬라이드의 정의는 containing(포함하는)입니다. Osculating(접촉하는)을 oscillating(진동하는)으로 외우면 다른 개념이 됩니다. 두 vector(벡터)에 perpendicular(수직)인 것은 다음 슬라이드의 binormal(종법선)입니다.')
add('종법선 방향 가속도는 0입니다', 'Contents 2 06:44–07:08',
    'Binormal(종법선) <b>e</b>ᵦ = <b>e</b>ₜ × <b>e</b>ₙ은 right-hand rule(오른손 법칙)로 정하는 세 번째 unit vector(단위벡터)입니다. 이 vector(벡터)는 osculating plane(접촉평면)에 perpendicular(수직)입니다.',
    'Acceleration(가속도)은 v̇<b>e</b>ₜ + (v²/ρ)<b>e</b>ₙ이므로 binormal component(종법선 성분)는 0입니다. 이는 공간곡선이 평면곡선이라는 뜻이 아니라, 매 순간 acceleration(가속도)이 그 순간의 osculating plane(접촉평면)에 놓인다는 뜻입니다. 정지점이나 곡률이 0인 점에서는 경로 기저의 정의에 별도 주의가 필요합니다.',
    eq='<b>e</b>ᵦ = <b>e</b>ₜ × <b>e</b>ₙ, &nbsp; <b>a</b> · <b>e</b>ᵦ = 0')
add('회전과 신장을 함께 다루는 극좌표', 'Contents 2 07:17–08:04',
    'Polar coordinates(극좌표)는 fixed origin(고정 원점)에서의 distance(거리) r와 angle(각도) θ로 위치를 표시합니다. Rotation(회전)과 extension(신장)이 함께 주어지는 ladder(사다리) 끝점이나 sliding collar(미끄러지는 칼라)에 유용합니다.',
    'Radial direction(반지름 방향)은 origin(원점)에서 바깥쪽을 향하고 transverse direction(횡방향)은 angle(각도)이 증가하는 방향입니다. 이 두 방향은 path(경로)의 tangent(접선)·normal(법선)과 일반적으로 다릅니다. 특히 r가 변하면 velocity(속도)는 radial(반지름 방향) 성분도 갖습니다.')
add('극좌표 속도: 거리 변화와 회전을 더합니다', 'Contents 2 08:06–09:08',
    'Position vector(위치벡터)는 <b>r</b> = r<b>e</b>ᵣ입니다. Radial unit vector(반지름 방향 단위벡터) <b>e</b>ᵣ는 θ가 바뀌면 방향이 바뀌므로 derivative(미분)가 0이 아닙니다. Distance(거리) r가 일정해도 회전하면 velocity(속도)가 생기는 이유입니다.',
    'Radial velocity component(반지름 방향 속도 성분)는 ṙ로, outward(바깥쪽)이면 positive(양수), inward(안쪽)이면 negative(음수)입니다. Transverse velocity component(횡방향 속도 성분)는 rθ̇입니다. Angular velocity(각속도) θ̇의 단위는 rad/s이고 rθ̇의 단위는 m/s입니다.',
    eq='<b>v</b> = ṙ<b>e</b>ᵣ + rθ̇<b>e</b>θ<br>v = √(ṙ² + r²θ̇²)')
add('극좌표 가속도에는 네 항이 필요합니다', 'Contents 2 09:13–09:23',
    'Radial acceleration component(반지름 방향 가속도 성분)는 r̈ − rθ̇²입니다. r̈는 radial distance(반지름 거리)의 변화율이 다시 변하는 효과이고 −rθ̇²는 rotating basis(회전하는 기저) 때문에 생기는 inward(안쪽) 항입니다. 따라서 aᵣ를 r̈만으로 계산하면 일반적으로 틀립니다.',
    'Transverse acceleration component(횡방향 가속도 성분)는 rθ̈ + 2ṙθ̇입니다. 첫 항은 angular velocity(각속도)의 변화, 두 번째 항은 radial motion(반지름 방향 운동)과 rotation(회전)이 동시에 있을 때 생기는 결합입니다. 두 component(성분)는 모두 positive(양수) 또는 negative(음수)가 될 수 있습니다.',
    eq='<b>a</b> = (r̈ − rθ̇²)<b>e</b>ᵣ + (rθ̈ + 2ṙθ̇)<b>e</b>θ')
add('극좌표 속도의 곱의 미분', 'Contents 2 09:27–10:53',
    'd(r<b>e</b>ᵣ)/dt에 product rule(곱의 미분법)을 적용하면 ṙ<b>e</b>ᵣ + r d<b>e</b>ᵣ/dt입니다. 원점으로부터 distance(거리)가 바뀌는 효과와 방향이 회전하는 효과를 따로 계산한 것입니다.',
    'θ가 작은 양만큼 증가하면 <b>e</b>ᵣ의 끝점은 unit circle(단위원)을 따라 움직입니다. 그 변화 방향은 <b>e</b>θ이고, 시간에 대한 변화율은 θ̇<b>e</b>θ입니다. 따라서 두 번째 항이 rθ̇<b>e</b>θ가 됩니다. Unit vector(단위벡터)의 길이가 일정하다는 사실은 그 방향이 일정하다는 뜻이 아닙니다.',
    eq='d<b>e</b>ᵣ/dt = θ̇<b>e</b>θ<br>d(r<b>e</b>ᵣ)/dt = ṙ<b>e</b>ᵣ + rθ̇<b>e</b>θ')
add('두 단위벡터의 미분 부호를 구분합니다', 'Contents 2 10:56–13:16',
    'θ가 increasing(증가)할 때 radial unit vector(반지름 방향 단위벡터)는 transverse direction(횡방향)으로 돌아가지만, transverse unit vector(횡방향 단위벡터)는 inward radial direction(안쪽 반지름 방향)으로 돌아갑니다. 따라서 두 미분식에는 서로 다른 부호가 붙습니다.',
    '편집자 보강: 고정 직교기저로 <b>e</b>ᵣ = cosθ<b>i</b> + sinθ<b>j</b>, <b>e</b>θ = −sinθ<b>i</b> + cosθ<b>j</b>로 써서 직접 미분하면 부호를 확인할 수 있습니다. θ에 대한 derivative(미분)를 시간에 대한 derivative(미분)로 바꿀 때는 chain rule(연쇄법칙)에 따라 θ̇를 곱합니다.',
    eq='d<b>e</b>ᵣ/dθ = <b>e</b>θ, &nbsp; d<b>e</b>θ/dθ = −<b>e</b>ᵣ<br>d<b>e</b>ᵣ/dt = θ̇<b>e</b>θ, &nbsp; d<b>e</b>θ/dt = −θ̇<b>e</b>ᵣ')
add('극좌표 가속도 유도: 2ṙθ̇는 두 곳에서 나옵니다', 'Contents 2 13:19–13:30',
    '첫 velocity term(속도 항) ṙ<b>e</b>ᵣ를 미분하면 r̈<b>e</b>ᵣ + ṙθ̇<b>e</b>θ입니다. 두 번째 velocity term(속도 항) rθ̇<b>e</b>θ를 미분하면 (ṙθ̇ + rθ̈)<b>e</b>θ − rθ̇²<b>e</b>ᵣ입니다. 각 term(항)에서 scalar coefficient(스칼라 계수)와 unit vector(단위벡터)를 모두 미분해야 합니다.',
    '같은 basis vector(기저벡터)끼리 모으면 <b>e</b>θ 앞의 ṙθ̇가 두 번 더해져 2ṙθ̇가 됩니다. θ̇가 constant(일정)하여 θ̈ = 0이어도 ṙ ≠ 0이면 transverse acceleration(횡방향 가속도)이 남을 수 있습니다.',
    eq='d(ṙ<b>e</b>ᵣ)/dt = r̈<b>e</b>ᵣ + ṙθ̇<b>e</b>θ<br>d(rθ̇<b>e</b>θ)/dt = −rθ̇²<b>e</b>ᵣ + (ṙθ̇ + rθ̈)<b>e</b>θ')
add('Lecture 3-4 · 문제풀이', 'Problem Solving', 'Relative motion(상대운동), tangential-normal coordinates(접선·법선 좌표), polar coordinates(극좌표)를 예제에 적용합니다.', role='Divider')
add('예제 1 · 교차로에서 두 자동차의 상대운동', 'Problem Solving 00:17–01:09',
    'Automobile A(자동차 A)는 east(동쪽)로 constant speed(일정한 속력) 36 km/h로 움직입니다. A가 intersection(교차로)을 통과하는 순간을 t = 0으로 정합니다. 동시에 B는 교차로 north(북쪽) 35 m 지점에서 starts from rest(정지 상태에서 출발)하여 south(남쪽)로 constant acceleration(일정한 가속도) 1.2 m/s²로 움직입니다.',
    '구할 것은 t = 5 s에서 B relative to A(B의 A에 대한) position(위치), velocity(속도), acceleration(가속도)입니다. “Relative to A(A에 대한)”가 붙으면 A의 관점으로 변환해야 합니다. B 자체의 남쪽 velocity(속도)만 답하면 조건을 충족하지 않습니다.')
add('예제 1 · 각각 계산한 뒤 같은 시각에 뺍니다', 'Problem Solving 01:12–01:42',
    '먼저 intersection(교차로)을 origin(원점), east(동쪽)를 +x, north(북쪽)를 +y로 정합니다. A와 B의 absolute motion(절대운동)을 이 fixed frame(고정좌표계)에서 각각 계산한 후 같은 t = 5 s에 평가합니다.',
    '마지막에 position vectors(위치벡터), velocity vectors(속도벡터), acceleration vectors(가속도벡터)를 각각 B − A 순서로 뺍니다. 그림으로 vector triangle(벡터 삼각형)을 그릴 수도 있지만, signed components(부호 있는 성분)를 먼저 적으면 방향 오류를 줄일 수 있습니다.')
add('예제 1 · 단위와 초기조건', 'Problem Solving 01:47–02:04',
    '36 km/h에 1000 m/km와 1 h/3600 s를 곱하면 10 m/s입니다. 이후 time(시간)을 s, distance(거리)를 m로 사용하므로 먼저 SI units(SI 단위)로 통일합니다. A의 x₀ = 0, B의 y₀ = 35 m입니다.',
    'B의 southward acceleration(남쪽 가속도)은 +y의 반대이므로 aᵧᵦ = −1.2 m/s²입니다. Starts from rest(정지 상태에서 출발)는 vᵦ₀ = 0을 의미하며 initial position(초기위치)이 0이라는 의미가 아닙니다.',
    eq='vₐ = 36 × 1000/3600 = 10 m/s<br><b>a</b>ₐ = <b>0</b>, &nbsp; <b>a</b>ᵦ = −1.2<b>j</b> m/s²')
add('예제 1 · 자동차 A는 등속운동입니다', 'Problem Solving 02:12–02:19',
    'A는 straight road(직선 도로)를 constant speed(일정한 속력)로 이동하므로 velocity vector(속도벡터)도 constant(일정)합니다. 따라서 acceleration(가속도)은 0이고 xₐ = 10t입니다. 이는 곡선에서 speed(속력)만 일정한 경우와 다릅니다.',
    't = 5 s에 A는 교차로 east(동쪽) 50 m에 있고, 계속 eastward velocity(동쪽 속도) 10 m/s를 가집니다. 벡터 답안에서는 <b>i</b>를 함께 써서 magnitude(크기)와 direction(방향)을 동시에 전달합니다.',
    eq='<b>r</b>ₐ = 50<b>i</b> m<br><b>v</b>ₐ = 10<b>i</b> m/s<br><b>a</b>ₐ = <b>0</b> m/s²')
add('예제 1 · 자동차 B는 남쪽으로 빨라집니다', 'Problem Solving 02:24–02:31',
    'B의 vertical coordinate(수직좌표)는 yᵦ(t) = 35 + 0t + ½(−1.2)t² = 35 − 0.6t²입니다. Velocity component(속도 성분)는 vᵧᵦ = −1.2t이고 acceleration component(가속도 성분)는 −1.2입니다. t > 0에서 두 부호가 모두 negative(음수)이므로 B는 south(남쪽)로 speeding up(빨라짐) 상태입니다.',
    '원본 첫 position equation(위치 방정식)의 yᵦ 뒤에는 등호 대신 빼기 기호처럼 보이는 표기가 있습니다. 올바른 관계는 yᵦ = yᵦ₀ + vᵦ₀t + ½aᵦt²이며, 바로 뒤의 35 − 0.6t² 계산과도 일치합니다.',
    eq='yᵦ = 35 − 0.6t², &nbsp; vᵧᵦ = −1.2t, &nbsp; aᵧᵦ = −1.2')
add('예제 1 · B는 북쪽에 있으면서 남쪽으로 움직입니다', 'Problem Solving 02:37–02:42',
    't = 5 s이면 yᵦ = 35 − 0.6 × 25 = +20 m, vᵧᵦ = −6 m/s입니다. 즉 position(위치)은 north(북쪽), velocity(속도)는 south(남쪽)입니다. Position(위치)의 부호와 velocity(속도)의 부호가 다르다고 모순은 아닙니다.',
    '원본 하단의 <b>r</b>ᵦ = 20 m 화살표는 downward(아래쪽)로 표시되어 있으나, yᵦ = +20 m와 도형은 upward(위쪽)를 지시합니다. 본문에서는 +20<b>j</b>로 교정합니다. 스크립트의 “3.5 seconds” 역시 문제와 결과의 t = 5 s에 맞춰 해석합니다.',
    eq='<b>r</b>ᵦ = 20<b>j</b> m<br><b>v</b>ᵦ = −6<b>j</b> m/s<br><b>a</b>ᵦ = −1.2<b>j</b> m/s²')
add('예제 1 · 벡터를 빼기 전의 상태', 'Problem Solving 02:51–02:56',
    'A의 position vector(위치벡터)는 east(동쪽), B의 position vector(위치벡터)는 north(북쪽)입니다. 반면 B의 velocity(속도)와 acceleration(가속도)은 south(남쪽)입니다. 원본의 B 위치 화살표 오기는 앞 슬라이드와 동일하게 +y로 교정하여 읽습니다.',
    'Relative position(상대위치)을 구할 때는 A의 끝점에서 B의 끝점으로 향하는 화살표를 그립니다. Relative velocity(상대속도)도 같은 subtraction(뺄셈)을 하되 position diagram(위치 그림)과 velocity diagram(속도 그림)을 혼합하지 않습니다.',
    eq='<b>r</b>ᵦ − <b>r</b>ₐ = 20<b>j</b> − 50<b>i</b><br><b>v</b>ᵦ − <b>v</b>ₐ = −6<b>j</b> − 10<b>i</b>')
add('예제 1 · 크기와 방향을 기하학적으로 구합니다', 'Problem Solving 03:03–03:12',
    'Relative position(상대위치)의 magnitude(크기)는 √(50² + 20²) = 53.85 m이고 direction(방향)은 west(서쪽)에서 north(북쪽)로 21.8°입니다. Relative velocity(상대속도)는 √(10² + 6²) = 11.66 m/s이며 west(서쪽)에서 south(남쪽)로 31.0°입니다.',
    'Arctangent(역탄젠트)는 component ratio(성분비)로 기준축과의 작은 각을 주지만, quadrant(사분면)는 각 component(성분)의 부호로 결정합니다. 21.8° 또는 31.0°만 적으면 기준 방향이 불분명합니다. Relative acceleration(상대가속도)은 1.2 m/s² south(남쪽)입니다.',
    eq='α = tan⁻¹(20/50) = 21.8°<br>β = tan⁻¹(6/10) = 31.0°')
add('예제 1 · 벡터 답안과 관측 의미', 'Problem Solving 03:19–03:37',
    'Relative position(상대위치), relative velocity(상대속도), relative acceleration(상대가속도)를 B − A로 각각 계산한 최종 결과입니다. 이 답안은 모든 direction(방향)을 signed unit-vector components(부호 있는 단위벡터 성분)로 명시하므로 각도 해석이 필요 없습니다.',
    'A 탑승자에게 B는 현재 northwest(북서쪽)에 있으면서 southwest(남서쪽)로 움직이는 것으로 보입니다. 이는 A가 east(동쪽)로 움직이는 효과가 B의 apparent westward motion(겉보기 서쪽 운동)에 더해지기 때문입니다.',
    eq='<b>r</b>ᵦ/ₐ = −50<b>i</b> + 20<b>j</b> m<br><b>v</b>ᵦ/ₐ = −10<b>i</b> − 6<b>j</b> m/s<br><b>a</b>ᵦ/ₐ = −1.2<b>j</b> m/s²')
add('예제 1 · 수치에는 평가 시각이 붙습니다', 'Problem Solving 03:43–03:56',
    '53.9 m와 11.66 m/s는 t = 5 s에서만 성립합니다. Relative position(상대위치)과 relative velocity(상대속도)는 time(시간)에 따라 변하므로 문제에 지정된 instant(순간)를 답안에 표시합니다.',
    '시간함수로 쓰면 아래와 같습니다. 첫 식을 differentiate(미분)하면 두 번째 식이 되고, 다시 differentiate(미분)하면 relative acceleration(상대가속도)이 됩니다. 이번 예제에서 relative acceleration(상대가속도)은 constant(일정)하지만 relative velocity(상대속도)는 constant(일정)하지 않습니다.',
    eq='<b>r</b>ᵦ/ₐ(t) = −10t<b>i</b> + (35 − 0.6t²)<b>j</b><br><b>v</b>ᵦ/ₐ(t) = −10<b>i</b> − 1.2t<b>j</b>')
add('예제 2 · 곡선도로에서 제동 직후의 가속도', 'Problem Solving 04:02–04:48',
    'Radius(반지름) 750 m인 curved road(곡선도로)에서 자동차가 90 km/h로 달리다가 brakes(브레이크)를 작동합니다. Speed(속력)는 constant rate(일정한 변화율)로 감소하여 8 s 후 72 km/h가 됩니다. 구할 것은 immediately after braking(제동 직후)의 acceleration(가속도)입니다.',
    '8 s의 정보는 tangential acceleration(접선가속도)을 계산하는 데 쓰고, normal acceleration(법선가속도)에는 제동 직후의 speed(속력) 90 km/h를 써야 합니다. “After 8 s(8초 후)”와 “immediately after(직후)”가 서로 다른 역할을 하는 것이 이 문제의 핵심입니다.')
add('예제 2 · 경로좌표를 선택하는 이유', 'Problem Solving 04:52–05:22',
    'Path(경로)와 radius of curvature(곡률반경) ρ가 주어지고 speed change(속력 변화)가 알려져 있으므로 tangential-normal coordinates(접선·법선 좌표)를 선택합니다. 진행 방향을 +<b>e</b>ₜ, curve center(곡선 중심) 쪽을 +<b>e</b>ₙ으로 정합니다.',
    '먼저 speed(속력) 변화를 시간으로 나눠 aₜ를 구하고, 그 instant(순간)의 speed(속력)로 aₙ = v²/ρ를 계산합니다. 마지막으로 두 component(성분)를 perpendicular(수직)하게 합성하여 magnitude(크기)와 direction(방향)을 구합니다.')
add('예제 2 · 속력을 SI 단위로 바꿉니다', 'Problem Solving 05:30–05:51',
    'Initial speed(초기속력) 90 km/h는 25 m/s, final speed(나중 속력) 72 km/h는 20 m/s입니다. 제동은 speed(속력)를 5 m/s 감소시킵니다. 750 m와 8 s를 그대로 사용할 수 있도록 단위를 맞춥니다.',
    'Acceleration diagram(가속도 그림)의 tangential component(접선 성분)는 motion(운동)의 반대 방향을 향하고 normal component(법선 성분)는 안쪽을 향합니다. 두 화살표가 모두 필요하므로 “제동 중이니 뒤쪽 가속도만 있다”는 해석은 잘못입니다.',
    eq='v₀ = 25 m/s, &nbsp; v₈ = 20 m/s, &nbsp; ρ = 750 m')
add('예제 2 · 일정한 감속률로 접선성분을 구합니다', 'Problem Solving 05:57–06:04',
    '문제의 slows down at a constant rate(일정한 비율로 감속한다)는 tangential acceleration(접선가속도)이 constant(일정)함을 뜻합니다. 따라서 average rate(평균 변화율) Δv/Δt를 어느 순간의 aₜ에도 사용할 수 있습니다.',
    'aₜ = (20 − 25)/8 = −0.625 m/s²입니다. Negative(음수) 부호는 진행 방향으로 잡은 +<b>e</b>ₜ의 반대를 뜻합니다. 다만 normal acceleration(법선가속도)은 v²/ρ이므로 speed(속력)가 줄면서 달라집니다. 전체 acceleration vector(가속도벡터)가 constant(일정)한 것은 아닙니다.',
    eq='aₜ = dv/dt = (20 − 25)/8 = −0.625 m/s²')
add('예제 2 · 직후의 속력으로 법선성분을 계산합니다', 'Problem Solving 06:12–06:22',
    'Immediately after(직후)에는 speed(속력)가 아직 25 m/s입니다. 따라서 aₙ = 25²/750 = 0.8333 m/s²입니다. 20 m/s는 8 s 후의 값이므로 이 단계에 넣으면 질문과 다른 instant(순간)의 답이 됩니다.',
    '전체 magnitude(크기)는 √(0.625² + 0.8333²) = 1.0417 m/s²입니다. Acceleration(가속도)은 backward tangent(진행 반대 접선)에서 inward normal(안쪽 법선) 쪽으로 53.1° 기울어집니다. 각도식에는 aₜ의 magnitude(크기) |aₜ|를 써서 기준 방향을 분명히 합니다.',
    eq='<b>a</b> = −0.625<b>e</b>ₜ + 0.8333<b>e</b>ₙ m/s²<br>|<b>a</b>| ≈ 1.042 m/s², &nbsp; α = tan⁻¹(0.8333/0.625) = 53.1°')
add('예제 2 · 감속과 방향 전환은 동시에 일어납니다', 'Problem Solving 06:34–06:59',
    'Tangential component(접선 성분)는 speed(속력)를 줄이고, normal component(법선 성분)는 자동차가 curve(곡선)를 계속 따라가도록 velocity direction(속도 방향)을 바꿉니다. 이 둘이 합쳐져 비스듬한 acceleration vector(가속도벡터)를 만듭니다.',
    'Cartesian coordinates(데카르트 좌표)로도 풀 수 있지만, 순간 tangent angle(접선 각도) 등을 추가로 표현해야 합니다. 문제에 주어진 path radius(경로 반지름)와 speed change(속력 변화)를 바로 활용하는 path coordinates(경로좌표)가 계산을 단순하게 합니다.')
add('예제 3 · 회전 막대를 따라 미끄러지는 칼라', 'Problem Solving 07:07–08:02',
    'Arm(막대)의 angle(각도)은 θ = 0.15t² rad이고 collar(칼라) B의 distance(거리)는 r = 0.9 − 0.12t² m입니다. Arm(막대)이 30° 회전했을 때 total velocity(전체속도), total acceleration(전체가속도), arm-relative acceleration(막대에 대한 상대가속도)을 구합니다.',
    'Collar(칼라)는 inward sliding(안쪽 미끄럼)과 rotation(회전)을 동시에 하므로 polar coordinates(극좌표)를 사용합니다. 마지막 질문은 회전하는 arm(막대)에 앉아서 본 sliding motion(미끄럼운동)의 가속도입니다. Fixed frame(고정좌표계)에서 구한 radial acceleration component(반지름 방향 가속도 성분)와 구분해야 합니다.')
add('예제 3 · 각도로 시간을 구한 다음 미분값을 평가합니다', 'Problem Solving 08:10–08:49',
    '먼저 30°를 π/6 rad로 convert(변환)하여 θ(t)에 대입하고 time(시간)을 구합니다. θ식은 radians(라디안) 기준이므로 30을 그대로 넣으면 안 됩니다. 그 후 r, ṙ, r̈, θ̇, θ̈를 모두 같은 time(시간)에서 계산합니다.',
    'Radial component(반지름 방향 성분)와 transverse component(횡방향 성분)를 계산한 뒤 vector(벡터)를 합성합니다. Relative acceleration(상대가속도)은 arm(막대)과 함께 회전하는 관측자가 본 r방향 sliding(미끄럼)만 따로 구합니다.')
add('예제 3 · 필요한 여섯 값을 한 시각에 모읍니다', 'Problem Solving 08:55–09:05',
    'θ = π/6 = 0.15t²에서 t = √[(π/6)/0.15] ≈ 1.8683 s입니다. 원본은 30°를 0.524 rad로 반올림하여 1.869 s로 제시합니다. 계산 중에는 π/6을 유지하고 마지막에 반올림하면 오차가 덜 쌓입니다.',
    'ṙ = −0.24t, r̈ = −0.24, θ̇ = 0.30t, θ̈ = 0.30입니다. ṙ가 negative(음수)이므로 inward(안쪽)로 움직이고, θ̇와 θ̈는 positive(양수)이므로 positive rotation(양의 회전) 방향으로 빨라집니다.',
    eq='t ≈ 1.8683 s, &nbsp; r ≈ 0.48112 m<br>ṙ ≈ −0.44840 m/s, &nbsp; r̈ = −0.240 m/s²<br>θ̇ ≈ 0.56050 rad/s, &nbsp; θ̈ = 0.300 rad/s²')
add('예제 3 · 전체속도는 막대 방향과 일치하지 않습니다', 'Problem Solving 09:13–09:53',
    'Radial velocity component(반지름 방향 속도 성분)는 vᵣ = ṙ ≈ −0.4484 m/s, transverse velocity component(횡방향 속도 성분)는 vθ = rθ̇ ≈ 0.2697 m/s입니다. 따라서 velocity(속도)는 inward(안쪽)와 positive transverse direction(양의 횡방향)을 함께 가집니다.',
    'Speed(속력)는 두 component(성분)의 제곱합 제곱근인 약 0.5232 m/s입니다. 원본의 0.524 m/s는 중간값 −0.449, 0.270을 사용한 반올림 결과입니다. Direction(방향)은 −<b>e</b>ᵣ에서 +<b>e</b>θ 쪽으로 약 31.0°이며, ṙ만을 total speed(전체속력)로 쓰면 rotation(회전)을 누락합니다.',
    eq='<b>v</b> ≈ −0.4484<b>e</b>ᵣ + 0.2697<b>e</b>θ m/s<br>|<b>v</b>| ≈ 0.5232 m/s')
add('예제 3 · 가속도 부호와 단위를 교정합니다', 'Problem Solving 10:01–10:46',
    'aᵣ = r̈ − rθ̇² ≈ −0.240 − 0.48112(0.56050)² = −0.39115 m/s²입니다. aθ = rθ̈ + 2ṙθ̇ ≈ 0.14434 − 0.50265 = −0.35832 m/s²입니다. Positive angular acceleration(양의 각가속도)이 있어도 inward sliding(안쪽 미끄럼)에서 발생하는 결합 항이 더 커서 aθ는 negative(음수)입니다.',
    '원본은 aᵣ 대입 첫 항을 +0.240으로 잘못 표시했지만 r̈는 −0.240입니다. 최종 acceleration magnitude(가속도의 크기)의 단위도 m/s가 아니라 m/s²여야 합니다. 본문 결과는 중간 반올림을 줄인 약 0.5305 m/s²이며 원본의 약 0.531 m/s²와 일치합니다. 방향은 −<b>e</b>ᵣ에서 −<b>e</b>θ 쪽으로 약 42.5°입니다.',
    eq='<b>a</b> ≈ −0.39115<b>e</b>ᵣ − 0.35832<b>e</b>θ m/s²<br>|<b>a</b>| ≈ 0.5305 m/s²')
add('예제 3 · 막대에 대한 상대가속도는 r̈입니다', 'Problem Solving 10:51–11:44',
    'Arm(막대)과 함께 회전하는 관측자는 collar(칼라)가 막대를 따라 inward(안쪽)로 미끄러지는 것만 봅니다. 이 relative rectilinear motion(상대 직선운동)을 나타내는 coordinate(좌표)는 r이므로 arm-relative acceleration(막대에 대한 상대가속도)은 r̈ = −0.240 m/s²입니다.',
    '이는 fixed-frame acceleration(고정좌표계 가속도)의 radial component(반지름 방향 성분) aᵣ ≈ −0.39115 m/s²와 다릅니다. 후자에는 −rθ̇²가 포함됩니다. 앞 절의 frame in translation(병진하는 좌표계) 공식을 rotating arm(회전하는 막대)의 관측값에 그대로 대입하지 않습니다.',
    eq='<b>a</b>relative to arm = −0.240<b>e</b>ᵣ m/s²<br>aᵣ = r̈ − rθ̇² ≠ r̈')
add('예제 3 · r과 곡률반경 ρ는 다릅니다', 'Problem Solving 11:48–12:44',
    'Polar radius(극좌표 반지름) r는 origin(원점) O에서 collar(칼라)까지의 distance(거리)입니다. Radius of curvature(곡률반경) ρ는 실제 trajectory(궤적)가 현재 얼마나 휘어 있는지를 나타냅니다. Sliding(미끄럼)이 있으므로 trajectory(궤적)는 O를 중심으로 하는 circle(원)이 아니며 r = ρ라고 둘 수 없습니다.',
    '시험용 보강: velocity direction(속도 방향)으로 acceleration(가속도)을 project(투영)하여 aₜ = (<b>v</b>·<b>a</b>)/|<b>v</b>|를 구합니다. 이어 aₙ = √(|<b>a</b>|² − aₜ²), ρ = v²/aₙ을 사용하면 같은 운동을 path coordinates(경로좌표)로 해석할 수 있습니다. aₙ을 |aᵣ|로 대체해서는 안 됩니다.',
    eq='aₜ = (<b>v</b> · <b>a</b>)/|<b>v</b>|<br>aₙ = √(|<b>a</b>|² − aₜ²), &nbsp; ρ = v²/aₙ')
add('그룹 예제 · 원심분리기의 두 바퀴 회전', 'Problem Solving 12:47–13:58',
    'Centrifuge(원심분리기)의 arm radius(막대 반지름)는 8 m이고 angular acceleration(각가속도)은 θ̈ = 0.05θ rad/s²입니다. 문제는 starts from rest(정지 상태에서 출발)하여 gondola(곤돌라)가 two full rotations(두 바퀴 완전 회전)을 지난 상태의 acceleration magnitude(가속도의 크기)를 묻습니다.',
    'Two full rotations(두 바퀴 완전 회전)은 θ = 4π rad입니다. θ̈가 time(시간)이 아니라 angular position(각위치)의 함수이므로 constant angular acceleration(일정한 각가속도) 공식을 바로 사용할 수 없습니다. 강의가 제시한 적분 풀이를 따르되, 초기조건의 수학적 한계는 적분 단계에서 따로 짚습니다.')
add('그룹 예제 · 두 바퀴 조건으로 통일합니다', 'Problem Solving 14:03–14:20',
    'Polar coordinates(극좌표)에서 r = 8 m, ṙ = r̈ = 0을 먼저 설정합니다. Angular velocity(각속도) θ̇를 각위치 함수의 integral(적분)로 구한 후 aᵣ = −rθ̇², aθ = rθ̈를 계산합니다.',
    '이 슬라이드의 “three revolutions(세 바퀴)”는 문제문 57장, 적분 상한 61장, 영상 13:58의 “two full rotations(두 바퀴)”와 충돌합니다. 반복되는 문제 조건과 실제 계산이 일치하는 two revolutions(두 바퀴), 즉 4π rad를 채택합니다.')
add('그룹 예제 · 옆모습만 보고 방향을 판단하지 않습니다', 'Problem Solving 14:29–14:48',
    'Side view(측면도)에서는 radial direction(반지름 방향) <b>e</b>ᵣ가 막대를 따라 outward(바깥쪽)로 보입니다. Transverse direction(횡방향) <b>e</b>θ는 회전 방향으로, 이 순간에는 그림 평면 안쪽을 향합니다. 다음 top view(평면도)로 두 방향을 확인합니다.',
    '이 circular motion(원운동)의 principal normal(주법선) <b>e</b>ₙ은 inward(안쪽)이므로 −<b>e</b>ᵣ입니다. Transverse direction(횡방향) <b>e</b>θ와 normal direction(법선 방향) <b>e</b>ₙ은 같지 않습니다. 스크립트의 “en” 언급은 도형과 일치하는 <b>e</b>θ로 구분해서 읽습니다.')
add('그룹 예제 · 각가속도의 독립변수를 바꿉니다', 'Problem Solving 14:52–16:23',
    'Angular acceleration(각가속도)은 θ̈ = dθ̇/dt입니다. Angular velocity(각속도) θ̇를 θ의 함수로 보면 chain rule(연쇄법칙)에 따라 dθ̇/dt = (dθ̇/dθ)(dθ/dt) = θ̇ dθ̇/dθ입니다. 따라서 θ̈ dθ = θ̇ dθ̇를 얻습니다.',
    '이 식은 rectilinear motion(직선운동)의 a dx = v dv와 대응합니다. 주어진 θ̈ = 0.05θ를 넣으면 좌변에는 angular position(각위치), 우변에는 angular velocity(각속도)만 남아 각각 integrate(적분)할 수 있습니다.',
    eq='θ̈ = θ̇ dθ̇/dθ<br>0.05θ dθ = θ̇ dθ̇')
add('그룹 예제 · 적분 결과와 초기조건의 한계', 'Problem Solving 16:25–16:31',
    '강의의 풀이에서는 θ = 0, θ̇ = 0을 적분 하한으로 두고 θ = 4π까지 적분합니다. ∫0.05θ dθ = 0.025θ², ∫θ̇ dθ̇ = ½θ̇²이므로 θ̇² = 0.05(4π)²를 얻습니다. 이는 θ와 θ̇ 사이의 관계입니다.',
    '편집자 보강 — 초기조건 주의: θ̈ = 0.05θ를 처음부터 정확히 적용하면서 유한한 시작 시각에 θ = θ̇ = 0이면, 해는 계속 θ = 0으로 머뭅니다. 별도 시동이나 비영 초기조건이 없으면 실제로 두 바퀴에 도달하지 않습니다. 아래 수치는 강의가 의도한 회전 상태를 조건부로 가정한 적분 결과이며, 이 조건만으로 출발이 설명되었다고 볼 수는 없습니다.',
    eq='∫₀⁴π 0.05θ dθ = ∫₀^ω ω dω<br>ω² = 0.05(4π)², &nbsp; ω = θ̇')
add('그룹 예제 · 각속도와 각가속도를 구분합니다', 'Problem Solving 16:36–16:56',
    '앞 슬라이드의 조건부 회전 상태에서 positive rotation(양의 회전)을 택하면 angular velocity(각속도)는 θ̇ = √0.05 × 4π ≈ 2.8099 rad/s입니다. Angular acceleration(각가속도)은 원래 주어진 식에 θ = 4π를 넣어 θ̈ = 0.05 × 4π ≈ 0.6283 rad/s²입니다.',
    '원본의 angular acceleration(각가속도) 계산 줄에는 점이 하나인 θ̇가 인쇄되어 있지만 단위와 원래 식에 맞는 기호는 θ̈입니다. Radians per second(초당 라디안)와 radians per second squared(초 제곱당 라디안)를 구분합니다.',
    eq='θ̇ ≈ 2.8099 rad/s<br>θ̈ ≈ 0.6283 rad/s²')
add('그룹 예제 · 선가속도 성분과 크기', 'Problem Solving 17:01–17:13',
    'r가 constant(일정)하므로 radial acceleration(반지름 방향 가속도)은 −8(2.8099)² ≈ −63.1655 m/s², transverse acceleration(횡방향 가속도)은 8(0.6283) ≈ 5.0265 m/s²입니다. 전자는 inward(안쪽), 후자는 positive transverse direction(양의 횡방향)입니다.',
    '두 성분을 합성하면 magnitude(크기)는 약 63.365 m/s²입니다. 이 값은 angular acceleration(각가속도)이 아니라 gondola(곤돌라)의 linear acceleration(선가속도)입니다. 강의의 수치는 앞에서 설명한 회전 상태 가정 아래 얻는 결과입니다.',
    eq='<b>a</b> ≈ −63.1655<b>e</b>ᵣ + 5.0265<b>e</b>θ m/s²<br>|<b>a</b>| ≈ 63.365 m/s²')
add('그룹 예제 · 막대가 신장하면 추가 항이 생깁니다', 'Problem Solving 17:22–18:11',
    'Arm(막대)이 6 m에서 10 m까지 extend(신장)할 수 있으면 r는 더 이상 constant(일정)하지 않습니다. Radial acceleration(반지름 방향 가속도)에 r̈가 추가되고 transverse acceleration(횡방향 가속도)에 2ṙθ̇가 추가될 수 있습니다. r 자체가 바뀌어 기존의 −rθ̇²와 rθ̈도 달라집니다.',
    '따라서 extension profile(신장 시간함수)을 조절하면 gondola acceleration(곤돌라 가속도)의 변화 양상, 즉 G-onset rate(G 증가율)에 영향을 줄 수 있습니다. 다만 “6 m에서 10 m”만으로는 ṙ와 r̈를 알 수 없으므로 새로운 numerical answer(수치 답)를 정할 수 없습니다. 구체적인 r(t)가 필요합니다.',
    eq='<b>a</b> = (r̈ − rθ̇²)<b>e</b>ᵣ + (rθ̈ + 2ṙθ̇)<b>e</b>θ')
add('참고문헌', '원본 참고문헌 슬라이드', 'Beer, Johnston, Cornwell, Self, Sanghi, <em>Vector Mechanics for Engineers: Dynamics</em>, 12th Edition, Chapter 11. 원본에 기재된 참고문헌입니다.', role='References')

assert len(records) == 65, len(records)

summary = ''.join([
    card('1. 곡선운동에서는 속력과 방향을 함께 봅니다.',
         'Curvilinear motion(곡선운동)의 핵심은 velocity(속도)가 vector(벡터)라는 점입니다. Fixed origin(고정 원점)에서 particle(입자)로 향하는 position vector(위치벡터) <b>r</b>를 미분하면 <b>v</b>, 다시 미분하면 <b>a</b>입니다. Speed(속력) v = |<b>v</b>|는 scalar(스칼라)이며, path(경로)를 따라 간 distance(거리) s의 변화율 ds/dt입니다. Velocity(속도)는 path(경로)의 tangent(접선)을 향하지만 acceleration(가속도)은 speed change(속력 변화)와 direction change(방향 변화)를 모두 담습니다.',
         '따라서 constant speed(일정한 속력)로 curve(곡선)를 돌아도 acceleration(가속도)이 생깁니다. Finite displacement(유한한 변위)의 크기 |Δ<b>r</b>|는 path length(경로 길이) Δs와 일반적으로 다릅니다. 이 차이를 유지해야 average velocity(평균속도)와 average speed(평균속력)를 혼동하지 않습니다.',
         formula('<b>v</b> = d<b>r</b>/dt, &nbsp; v = ds/dt, &nbsp; <b>a</b> = d<b>v</b>/dt'), kind='callout'),
    card('2. 직교좌표: 고정된 축마다 직선운동처럼 계산합니다.',
         'Rectangular coordinates(직교좌표)는 x(t), y(t), z(t)가 주어지거나 acceleration components(가속도 성분)를 각각 적분하기 쉬울 때 적합합니다. Unit vectors(단위벡터) <b>i</b>, <b>j</b>, <b>k</b>는 fixed(고정)되어 있으므로 coordinate(좌표)만 미분합니다. 각 component(성분)의 부호는 축 방향을 나타내며, 전체 magnitude(크기)는 제곱합 제곱근으로 구합니다.',
         'Projectile motion(포물선운동)에서 air resistance(공기저항)를 neglect(무시)하고 upward(위쪽)를 +y로 두면 aₓ = 0, aᵧ = −g입니다. Horizontal motion(수평운동)은 uniform(등속)이고 vertical motion(수직운동)은 uniformly accelerated(등가속도)입니다. Origin(원점)을 발사점으로 잡으면 x = vₓ₀t, y = vᵧ₀t − ½gt²입니다. 두 방향은 독립적으로 계산하되 반드시 같은 time(시간)을 사용합니다.',
         formula('<b>r</b> = x<b>i</b> + y<b>j</b> + z<b>k</b><br><b>v</b> = ẋ<b>i</b> + ẏ<b>j</b> + ż<b>k</b><br><b>a</b> = ẍ<b>i</b> + ÿ<b>j</b> + z̈<b>k</b>')),
    card('3. 상대운동: 관측 대상에서 관측자를 뺍니다.',
         'B relative to A(B의 A에 대한)는 B − A입니다. Relative position(상대위치), relative velocity(상대속도), relative acceleration(상대가속도)를 각각 같은 fixed axes(고정축)로 표현한 뒤 뺍니다. A에서 본 B의 position(위치)이 북쪽이라고 해서 velocity(속도)도 북쪽이어야 하는 것은 아닙니다.',
         '교차로 예제의 t = 5 s에서는 <b>r</b>ᵦ/ₐ = −50<b>i</b> + 20<b>j</b> m, <b>v</b>ᵦ/ₐ = −10<b>i</b> − 6<b>j</b> m/s, <b>a</b>ᵦ/ₐ = −1.2<b>j</b> m/s²입니다. 즉 B는 A의 northwest(북서쪽)에 있으면서 southwest(남서쪽)로 움직입니다. Moving-frame derivatives(이동좌표계에서의 미분)를 이 단순 뺄셈으로 해석하는 조건은 frame in translation(병진하는 좌표계), 즉 축이 회전하지 않는다는 것입니다.',
         formula('<b>r</b>ᵦ = <b>r</b>ₐ + <b>r</b>ᵦ/ₐ<br><b>v</b>ᵦ/ₐ = <b>v</b>ᵦ − <b>v</b>ₐ, &nbsp; <b>a</b>ᵦ/ₐ = <b>a</b>ᵦ − <b>a</b>ₐ')),
    card('4. 경로좌표: 빨라짐과 꺾임을 분리합니다.',
         'Path coordinates(경로좌표)는 path(경로)와 radius of curvature(곡률반경) ρ를 알 때 유용합니다. <b>e</b>ₜ는 velocity direction(속도 방향), <b>e</b>ₙ은 center of curvature(곡률중심) 쪽입니다. Tangential acceleration(접선가속도) aₜ = dv/dt는 speeding up(빨라짐)이면 positive(양수), slowing down(느려짐)이면 negative(음수)입니다. Normal acceleration(법선가속도) aₙ = v²/ρ는 direction change(방향 변화)를 나타내며 중심을 향합니다.',
         '공식의 이유는 <b>v</b> = v<b>e</b>ₜ의 product rule(곱의 미분법)입니다. Speed(속력)의 변화가 v̇<b>e</b>ₜ를 만들고, unit tangent(단위접선벡터)의 방향 변화 d<b>e</b>ₜ/dt = (v/ρ)<b>e</b>ₙ이 v²/ρ 항을 만듭니다. Space curve(공간곡선)에서도 두 성분은 성립합니다. 두 방향이 만드는 osculating plane(접촉평면)의 perpendicular direction(수직 방향)인 binormal(종법선)에는 acceleration component(가속도 성분)가 없습니다.',
         '곡선도로 제동 예제에서는 8 s 동안 25 → 20 m/s로 감소하여 aₜ = −0.625 m/s²입니다. Immediately after braking(제동 직후)을 물으므로 aₙ에는 25 m/s를 넣어 0.8333 m/s²를 얻습니다. 전체 acceleration magnitude(가속도의 크기)는 약 1.042 m/s²입니다.',
         formula('<b>a</b> = v̇<b>e</b>ₜ + (v²/ρ)<b>e</b>ₙ<br>|<b>a</b>| = √(aₜ² + aₙ²)')),
    card('5. 극좌표: 원점에서의 거리와 각도를 추적합니다.',
         'Polar coordinates(극좌표)는 fixed origin(고정 원점)에서 잰 r(t)와 θ(t)가 주어질 때 유용합니다. <b>e</b>ᵣ는 outward(바깥쪽), <b>e</b>θ는 angle(각도)이 increasing(증가)하는 방향입니다. Unit vectors(단위벡터)가 회전하므로 d<b>e</b>ᵣ/dt = θ̇<b>e</b>θ와 d<b>e</b>θ/dt = −θ̇<b>e</b>ᵣ를 반드시 포함합니다.',
         'Velocity(속도)는 radial motion(반지름 방향 운동) ṙ와 rotation(회전) rθ̇의 합입니다. Acceleration(가속도)에는 radial coordinate acceleration(반지름 좌표의 가속도) r̈, inward rotation term(안쪽 회전 항) −rθ̇², angular acceleration term(각가속도 항) rθ̈, coupled term(결합 항) 2ṙθ̇가 있습니다. 마지막 항은 두 velocity terms(속도 항)를 각각 미분할 때 ṙθ̇가 한 번씩 나와 생깁니다.',
         formula('<b>v</b> = ṙ<b>e</b>ᵣ + rθ̇<b>e</b>θ<br><b>a</b> = (r̈ − rθ̇²)<b>e</b>ᵣ + (rθ̈ + 2ṙθ̇)<b>e</b>θ'),
         'Rotation(회전)과 inward sliding(안쪽 미끄럼)이 겹친 collar(칼라) 예제에서 θ = 30°는 π/6 rad입니다. 그 순간 v ≈ 0.5232 m/s, |<b>a</b>| ≈ 0.5305 m/s²이지만 arm-relative acceleration(막대에 대한 상대가속도)은 r̈ = −0.240 m/s²입니다. Radial acceleration component(반지름 방향 가속도 성분) aᵣ와 r̈는 다른 물리량입니다.'),
    card('6. 같은 운동이어도 r과 ρ, 횡방향과 접선방향은 다릅니다.',
         'Polar radius(극좌표 반지름) r는 선택한 origin(원점)에서 잰 거리이고, radius of curvature(곡률반경) ρ는 trajectory(궤적) 자체의 휨을 나타냅니다. 따라서 aᵣ = −v²/r, aₙ = |aᵣ|를 일반식처럼 사용하면 안 됩니다. Fixed-radius circular motion(고정 반지름 원운동)에서 origin(원점)이 circle center(원 중심)일 때만 두 표현이 특별히 단순하게 연결됩니다.',
         'r = R이 constant(일정)하면 ṙ = r̈ = 0이므로 <b>v</b> = Rθ̇<b>e</b>θ, <b>a</b> = −Rθ̇²<b>e</b>ᵣ + Rθ̈<b>e</b>θ입니다. Positive rotation(양의 회전)에서는 <b>e</b>ₜ = <b>e</b>θ, <b>e</b>ₙ = −<b>e</b>ᵣ, ρ = R입니다. Radial component(반지름 방향 성분)는 음수이고 normal component(법선 성분)는 양수여도 같은 inward acceleration(안쪽 가속도)을 표현합니다.'),
    card('7. 각가속도가 각도의 함수이면 적분 변수를 바꿉니다.',
         'θ̈가 θ의 함수이면 chain rule(연쇄법칙)로 θ̈ = θ̇ dθ̇/dθ를 사용합니다. 따라서 θ̈ dθ = θ̇ dθ̇를 integrate(적분)하면 angular position(각위치)과 angular velocity(각속도)를 직접 연결할 수 있습니다. Two revolutions(두 바퀴)는 4π rad이며 원심분리기 예제의 강의 계산은 θ̇ ≈ 2.8099 rad/s, θ̈ ≈ 0.6283 rad/s², |<b>a</b>| ≈ 63.365 m/s²입니다.',
         '편집자 보강: 이 예제의 θ̈ = 0.05θ와 정확한 θ = θ̇ = 0 초기조건만으로는 실제 출발하지 않습니다. 위 수치는 강의가 가정한 회전 상태에서의 형식적 적분 결과로 이해해야 합니다. 문제 조건의 물리적 타당성과 주어진 풀이의 계산을 구분합니다.'),
    card('문제를 읽고 좌표계를 고르는 순서',
         '먼저 determine(구하라)의 대상이 vector(벡터)인지 magnitude(크기)인지, absolute(절대)인지 relative(상대)인지 확인합니다. 이어 starts from rest(정지 출발), constant speed(일정한 속력), constant rate(일정한 변화율), immediately after(직후)처럼 상태와 평가 시각을 나타내는 표현을 식으로 바꿉니다.',
         'Fixed-axis components(고정축 성분)가 주어지면 rectangular coordinates(직교좌표), path curvature(경로 곡률)와 speed change(속력 변화)가 주어지면 path coordinates(경로좌표), r(t)와 θ(t)가 주어지면 polar coordinates(극좌표)를 선택합니다. Unit conversion(단위 변환) → 미분 또는 적분 → 지정 시각 대입 → 성분 합성 → 방향과 단위 설명의 순서로 풉니다.', kind='exam-card'),
    '<div class="evidence"><span>슬라이드 05–64 종합</span><span>Contents 1·2 및 Problem Solving</span><span>Summary 00:18–00:50</span></div>',
])

terms = [
('curvilinear motion','곡선운동','직선이 아닌 경로를 따라 움직이는 운동'),
('position vector','위치벡터','원점에서 현재 위치를 향하는 벡터'),
('displacement','변위','두 위치벡터의 차; 경로 길이와 구분'),
('velocity','속도','위치벡터의 시간 변화율; 방향 포함'),
('speed','속력','속도벡터의 크기; 0 이상인 스칼라'),
('acceleration','가속도','속도벡터의 시간 변화율'),
('instantaneous','순간의','한 시각의 극한 변화율을 나타냄'),
('magnitude','크기','벡터의 길이; 방향 정보와 별개'),
('rectangular / Cartesian coordinates','직교좌표 / 데카르트 좌표','고정된 직교축의 성분으로 위치를 표현'),
('projectile motion','포물선운동','공기저항을 무시하고 일정한 중력가속도로 다루는 투사체 운동'),
('uniform motion','등속운동','속도벡터가 일정한 운동'),
('uniformly accelerated','등가속도의','해당 운동의 가속도가 일정한 상태'),
('frame in translation','병진하는 좌표계','원점이 이동하되 축 방향이 회전하지 않는 좌표계'),
('relative to / with respect to','…에 대한','관측 기준을 지정하는 표현'),
('tangential','접선 방향의','현재 경로의 접선에 따른 방향'),
('normal / principal normal','법선 / 주법선','접선에 수직이며 곡률중심으로 향하는 방향'),
('radius of curvature','곡률반경','해당 점에서 경로의 휨을 나타내는 ρ'),
('osculating plane','접촉평면','접선과 주법선을 포함하는 순간 평면'),
('binormal','종법선','접촉평면에 수직인 eᵦ = eₜ × eₙ 방향'),
('radial','반지름 방향의','극좌표 원점에서 바깥쪽으로 향하는 방향'),
('transverse','횡방향의','반지름 방향에 수직이며 극각이 증가하는 방향'),
('angular velocity','각속도','각도의 시간 변화율 θ̇; rad/s'),
('angular acceleration','각가속도','각속도의 시간 변화율 θ̈; rad/s²'),
('product rule / chain rule','곱의 미분법 / 연쇄법칙','변하는 계수와 기저벡터를 미분하는 규칙'),
('determine / evaluate','구하라 / 계산하여 평가하라','조건을 사용해 값을 구하거나 지정 상태에 대입'),
('starts from rest','정지 상태에서 출발한다','초기속도가 0; 초기위치가 0이라는 뜻은 아님'),
('constant speed','일정한 속력','속도 크기가 일정; 방향까지 일정하다는 뜻은 아님'),
('slows down at a constant rate','일정한 비율로 감속한다','접선가속도가 일정한 음수'),
('immediately after','직후','사건 바로 뒤의 순간; 이후의 지정 시각과 구분'),
('two full rotations / revolutions','두 바퀴 완전 회전','각변위 4π rad'),
('inward / outward','안쪽 / 바깥쪽','원점 쪽 / 원점 반대쪽'),
('perpendicular / tangent','수직인 / 접하는','기준 방향과 이루는 기하학적 관계'),
('collar / arm / centrifuge','칼라 / 막대 / 원심분리기','극좌표 예제의 장치 이름'),
]

exam_items = [
('Can a particle have constant speed(일정한 속력) and nonzero acceleration(0이 아닌 가속도)?',
 'Yes. On a curved path, the velocity changes direction even when its magnitude is constant. The tangential acceleration is zero, but the normal acceleration is v²/ρ toward the center of curvature.',
 'Constant speed(일정한 속력)는 aₜ = 0만 뜻합니다. Finite curvature(유한한 곡률)를 가진 경로에서 움직이면 normal acceleration(법선가속도)은 남습니다.'),
('Define velocity(속도) and speed(속력).',
 'Velocity is the time derivative of the position vector and is tangent to the path. Speed is the magnitude of velocity and equals the rate of change of distance traveled along the path.',
 'Position vector(위치벡터)의 derivative(미분)는 velocity(속도), 그 magnitude(크기)는 speed(속력)입니다. Finite displacement(유한한 변위)와 distance traveled(이동거리)를 혼동하지 않습니다.'),
('Explain motion relative to a translating frame(병진하는 좌표계에 대한 운동).',
 'For a nonrotating frame attached to A, r_B = r_A + r_B/A. Differentiation gives v_B/A = v_B − v_A and a_B/A = a_B − a_A. All vectors must be expressed in compatible axes.',
 'Nonrotating(회전하지 않는) 조건, B − A subtraction order(뺄셈 순서), 동일한 axes(축)를 답안에 포함합니다.'),
('Determine the relative motion(상대운동) in Sample Problem 1 at t = 5 s.',
 'Taking east as +x and north as +y, r_B/A = (−50i + 20j) m, v_B/A = (−10i − 6j) m/s, and a_B/A = −1.2j m/s². Thus B is northwest of A and appears to move southwest.',
 'Northwest(북서쪽)는 relative position(상대위치), southwest(남서쪽)는 relative velocity(상대속도)의 방향입니다.'),
('Derive the tangential and normal components(접선·법선 성분) of acceleration(가속도).',
 'Starting from v = v e_t, the product rule gives a = (dv/dt)e_t + v(de_t/dt). Since de_t/dt = (v/ρ)e_n, a = (dv/dt)e_t + (v²/ρ)e_n.',
 'Product rule(곱의 미분법)와 changing unit tangent(변하는 단위접선벡터)을 써야 방향 변화 항을 설명할 수 있습니다.'),
('Find the acceleration immediately after braking(제동 직후) in Sample Problem 2.',
 'The constant tangential acceleration is (20 − 25)/8 = −0.625 m/s². Immediately after braking, v = 25 m/s, so a_n = 25²/750 = 0.8333 m/s². Therefore a = −0.625e_t + 0.8333e_n m/s² and its magnitude is approximately 1.042 m/s².',
 'Immediately after(직후)에는 initial speed(초기속력)를 사용합니다. 8 s 후의 speed(속력)는 aₜ 계산에만 들어갑니다.'),
('Write velocity(속도) and acceleration(가속도) in polar coordinates(극좌표).',
 'With e_r directed outward and e_θ in the direction of increasing θ, v = ṙe_r + rθ̇e_θ and a = (r̈ − rθ̇²)e_r + (rθ̈ + 2ṙθ̇)e_θ. These expressions include the time derivatives of the unit vectors.',
 'Outward(바깥쪽)와 increasing θ(증가하는 θ)를 먼저 정의하고 radial(반지름 방향)·transverse(횡방향) 성분을 모두 씁니다.'),
('Is radial acceleration(반지름 방향 가속도) equal to r̈?',
 'Not in general. The radial component of absolute acceleration is a_r = r̈ − rθ̇². For the sliding collar, the acceleration relative to the rotating arm is r̈e_r, which differs from the radial component of absolute acceleration.',
 'Absolute acceleration(절대가속도)의 component(성분)와 rotating arm(회전 막대)에 대한 relative acceleration(상대가속도)을 구분합니다.'),
('Are polar radius(극좌표 반지름) r and radius of curvature(곡률반경) ρ identical?',
 'No. The polar radius is measured from a selected origin, whereas the radius of curvature describes the local shape of the trajectory. They coincide for circular motion when the origin is at the circle center.',
 '선택한 origin(원점)에 대한 distance(거리)와 path geometry(경로 기하학)의 차이를 설명합니다.'),
('How do you use angular acceleration as a function of angle(각도의 함수인 각가속도)?',
 'Use θ̈ = θ̇(dθ̇/dθ), so θ̈ dθ = θ̇ dθ̇. Integrate between the specified angular positions and angular velocities, while checking that the initial conditions allow the assumed motion.',
 'Chain rule(연쇄법칙)로 독립변수를 바꾸고 initial conditions(초기조건)가 motion(운동)을 허용하는지도 확인합니다.'),
]

audit = [
('Contents 1 00:29–00:35', 'curvy linear / currently linear motion', 'curvilinear motion(곡선운동)', '슬라이드 05 제목과 정의'),
('Contents 1 03:13–03:20', 'not perpendicular', '일반 가속도는 접선·법선 두 성분을 가질 수 있음', '슬라이드 08 및 19–23; 원문은 보존하고 정의로 해설'),
('Contents 2 06:22–07:08', 'oscillating plane / binomial / perpendicular to both', 'osculating plane(접촉평면), binormal(종법선); 평면은 접선·주법선을 포함', '슬라이드 25–26의 정의와 도형'),
('Problem Solving 02:37', '3.5 seconds', 't = 5 s', '문제 34장, 계산 39장, 영상 03:56 모두 5 s'),
('Problem Solving 04:34', 'after a second', 'after 8 s(8초 후)', '슬라이드 44 문제문과 47장의 분모 8'),
('Problem Solving 07:18–11:44', 'caller / color / all double that', 'collar(칼라), r̈', '슬라이드 50–55의 장치와 수식; 원문 파일은 수정하지 않음'),
('슬라이드 11', 'y = vᵧ₀y − ½gt²', 'y = vᵧ₀t − ½gt²', '시간 미분과 단위가 vᵧ = vᵧ₀ − gt를 만족'),
('슬라이드 38', 'yᵦ 뒤의 빼기 기호', 'yᵦ = yᵦ₀ + vᵦ₀t + ½aᵦt²', '같은 줄의 최종식 35 − 0.6t²와 39장'),
('슬라이드 39–40', 'rᵦ = 20 m에 아래쪽 화살표', '<b>r</b>ᵦ = +20<b>j</b> m, north(북쪽)', 'yᵦ = +20 m와 위치 그림, 42장 벡터식'),
('슬라이드 54', 'aᵣ 대입 +0.240, 최종 단위 m/s', '−0.240, 최종 단위 m/s²', 'r̈ = −0.240인 52장과 가속도 정의'),
('슬라이드 58', 'three revolutions(세 바퀴)', 'two revolutions(두 바퀴), 4π rad', '57장 문제, 61장 적분 상한, 영상 13:58'),
('슬라이드 62', '각가속도 계산 줄의 θ̇', 'θ̈ = 0.6283 rad/s²', '57장의 원래 식과 단위'),
('슬라이드 57·61 초기조건', 'θ̈ = 0.05θ, θ = θ̇ = 0에서 출발', '정확한 영 초기조건이면 정지해가 유지됨', '편집자 보강: 강의의 회전 상태 계산과 실제 출발 가능성을 분리'),
]

def table(headers, rows):
    return '<table class="term-table"><thead><tr>' + ''.join('<th>'+x+'</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows) + '</tbody></table>'

template = (SITE / 'templates/lecture-page.template.html').read_text(encoding='utf-8')
source_pattern = r'<section class="source-section"[\s\S]*?</section>'
source_template = re.search(source_pattern, template).group()
sources = []
for n, (title, evidence, blocks, role) in enumerate(records, 1):
    vals = {'NN':f'{n:02d}', 'SLIDE_ROLE':role, 'SLIDE_HEADING':title,
            'LECTURE_SLUG':'lecture03', 'DESCRIPTIVE_ALT_TEXT':f'Lecture 3 원본 슬라이드 {n:02d}: {escape(title)}',
            'CURRENT_PAGE':str(n), 'PAGE_COUNT':'65', 'TRANSCRIPT_TIME_OR_SLIDE_ROLE':evidence,
            'SLIDE_EXPLANATION_BLOCKS':blocks}
    section = source_template
    for key, value in vals.items():
        section = section.replace('{{'+key+'}}', value)
    sources.append(section)
template = re.sub(source_pattern, lambda _: '\n\n'.join(sources), template, count=1)
exam_html = ''.join('<div class="exam-card"><h3>'+q+'</h3><div class="answer"><span class="answer__label">Model answer</span>'+a+'</div><p style="margin-top: 12px">'+ko+'</p></div>' for q,a,ko in exam_items)
template = re.sub(r'<div class="exam-card">\s*<h3>\{\{EXAM_QUESTION\}\}</h3>[\s\S]*?</div>\s*</div>', lambda _: exam_html + '\n          </div>', template, count=1)
videos = [('Overview','H0vLGY16cg0'),('Contents 1','_jP-6KZXrWs'),('Contents 2','I0SNe-8ShAo'),('Problem Solving','Mu_C3stQ_cM'),('Summary','jtZDnB-WVgQ')]
toc = [('overview','전체 개요'),('concept-map','개념 지도'),('concept-summary','핵심 개념 요약')] + [(f'slide-{i:02d}', f'{i:02d} · {row[0]}') for i,row in enumerate(records,1)] + [('exam-english','시험 영어'),('glossary','용어집'),('asr-log','원본·스크립트 교정'),('sources','출처')]
values = {
    'LECTURE_NUMBER':'Lecture 3', 'LECTURE_TITLE':'Kinematics of Particles II: Curvilinear Motion',
    'ONE_SENTENCE_DESCRIPTION':'2주차 곡선운동: 65장 원본 슬라이드와 영어 영상 5개를 종합한 한국어 학습 노트',
    'WEEK':'Week 02', 'DATE_OR_날짜_미기재':'2026-09-09', 'PAGE_COUNT':'65',
    'LECTURE_PROMISE':'Curvilinear motion(곡선운동)을 vector(벡터)로 이해하고, rectangular coordinates(직교좌표)·path coordinates(경로좌표)·polar coordinates(극좌표)를 문제 조건에 맞춰 선택합니다.',
    'VIDEO_SET':'Overview · Contents 1·2 · Problem Solving · Summary',
    'ALL_CONTENTS_AND_PROBLEM_SOLVING_BUTTONS':'\n'.join(f'<a class="button button--primary" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상 열기</a>' for label,vid in videos[1:4]),
    'ORIGINAL_PDF_URL':'https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/lecture03_note.pdf',
    'LECTURE_NOTE_FILENAME':'lecture03_note.pdf',
    'CORE_RELATIONSHIP_HEADLINE':'속력이 바뀌거나 방향이 바뀌면 가속도가 생깁니다.',
    'CORE_RELATIONSHIP_EXPLANATION':'Curvilinear motion(곡선운동)에서는 velocity(속도)를 magnitude(크기)와 direction(방향)을 갖는 vector(벡터)로 다룹니다. 같은 motion(운동)도 coordinate system(좌표계)에 따라 성분식이 달라지므로, 주어진 path(경로)·position(위치)·angle(각도)에 가장 잘 맞는 기준을 선택합니다.',
    'CONCEPT_MAP_HEADLINE':'하나의 벡터 관계를 세 좌표계로 표현합니다.',
    'CONCEPT_MAP_BLOCKS':'<div class="grid-3">' + ''.join([
        card('Rectangular coordinates(직교좌표)','고정된 x·y·z축에서 coordinate(좌표)를 미분합니다. Projectile motion(포물선운동), 두 물체의 relative motion(상대운동)에 적합합니다.'),
        card('Path coordinates(경로좌표)','진행 tangent(접선)과 안쪽 normal(법선)을 사용합니다. Speed change(속력 변화)와 path curvature(경로 곡률)가 주어질 때 적합합니다.'),
        card('Polar coordinates(극좌표)','Origin(원점)에서의 distance(거리) r와 angle(각도) θ를 사용합니다. Rotation(회전)과 sliding(미끄럼)이 겹치는 운동에 적합합니다.')]) + '</div>',
    'STANDALONE_CONCEPT_SUMMARY':summary,
    'DISTINCT_SUMMARY_VIDEO_SECTION_IF_NEEDED':'',
    'EXAM_SECTION_TITLE':'조건을 해석하고 풀이를 설명하는 영어',
    'BILINGUAL_GLOSSARY_TABLE':table(['영어(한국어)','의미와 사용'], [(f'{en}({ko})',ex) for en,ko,ex in terms]),
    'AUDIT_SECTION_TITLE':'원본 슬라이드·자동생성 스크립트 교정 기록',
    'ASR_CORRECTION_TABLE':p('원본 슬라이드와 영어 자동생성 스크립트는 그대로 보존했습니다. 아래는 본문에서 사용한 교정과 그 근거입니다. 음성을 다시 판독하지 않은 항목은 강사의 실제 발화 오류인지 자막 인식 오류인지 단정하지 않습니다.') + table(['위치','원문 또는 문제','본문 처리','근거'],audit),
    'SOURCE_LIST_AND_PROVENANCE_NOTE':'<ul class="plain-list"><li>원본 PDF: Lecture 3, MC2103, Fall 2026, 65장.</li>' + ''.join(f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상</a> · 영어 자동생성 스크립트, 2026-09-08 확보.</li>' for label,vid in videos) + '<li>주차·날짜: Teams에서 보존한 강의 인덱스의 Week 02 · 2026-09-09.</li></ul>' + p('Summary 00:18–00:50의 실제 개념 복습은 핵심 개념 요약에 반영했습니다. 00:52–01:03은 다음 단원의 kinetics(운동역학)와 Newton’s laws(뉴턴 법칙) 예고이며 현재 개념 요약과 구분합니다.') + p('계산값은 특별히 표시하지 않으면 중간 반올림을 줄여 계산했습니다. 원본의 반올림 값과 마지막 자리 차이가 있을 수 있습니다. 강의에 없는 추가 유도나 조건 검토는 시험용 보강 또는 편집자 보강으로 표시했습니다.'),
    'TABLE_OF_CONTENTS_LINKS':''.join(f'<li><a href="#{id}">{text}</a></li>' for id,text in toc),
}
for key,value in values.items():
    template = template.replace('{{'+key+'}}',value)
template = template.replace('이 부분만 읽어도 렉처의 핵심 정의, 개념 관계, 가정과 풀이 흐름을 이해할 수 있도록 작성합니다.', '이 부분은 원본 슬라이드와 Contents·Problem Solving·Summary의 개념 설명을 종합합니다. 곡선운동의 정의에서 좌표계 선택, 주요 공식과 예제 해석까지 연결하여 읽을 수 있습니다.')
template = re.sub(r'\s*<!--[\s\S]*?-->','',template)
template = '\n'.join(line.rstrip() for line in template.splitlines()) + '\n'
assert not re.search(r'\{\{[^}]+\}\}',template), re.findall(r'\{\{[^}]+\}\}',template)
(SITE / 'lecture03.html').write_text(template, encoding='utf-8')
print(f'BUILT lecture03.html: {len(records)} source sections, {len(exam_items)} exam cards')
