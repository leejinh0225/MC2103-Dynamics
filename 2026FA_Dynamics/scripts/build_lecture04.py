"""Build Lecture 4 by filling the fixed Lecture 1-derived template."""
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

def add(title, evidence, *body, eq='', extra='', role='Concept'):
    blocks = card('핵심 해설' if role == 'Concept' else '슬라이드 안내', *body, kind='card' if role == 'Concept' else 'quiet-card')
    if eq:
        blocks += card('식과 기호', formula(eq))
    records.append((title, evidence, blocks + extra, role))

add('Lecture 4 표지','MC2103 · Fall 2026','Kinetics of Particles(입자의 운동역학)를 다루는 Lecture 4의 표지입니다.',role='Title')
add('Lecture 4-1 · 도입','Overview 00:17–01:18','입자 모델과 운동의 원인을 소개하는 구간입니다. Overview(도입 영상)는 자동차의 rotation(회전)을 무시한 particle model(입자 모델)과 force(힘)의 예를 설명합니다.',role='Divider')
add('원본의 도입 참고 영상 링크','원본 링크 슬라이드','<a href="https://youtu.be/ELptDhf6H_U" target="_blank" rel="noreferrer">원본 슬라이드의 참고 영상 열기</a>. 이 링크는 강의 인덱스의 Overview(도입 영상)와 다릅니다. 아래 해설의 영상 근거는 인덱스에 지정된 5개 영상입니다.',role='Video link')
add('Lecture 4-2 · 뉴턴 법칙과 자유물체도','Contents 1','Newton’s second law(뉴턴 제2법칙), linear momentum(선운동량), unit system(단위계), free-body diagram(자유물체도)을 다루는 구간입니다.',role='Divider')
add('경주차의 경로를 설계하려면 힘을 알아야 합니다','Contents 1 00:17–00:41',
    'Kinematics(운동학)는 racecar(경주차)가 어디에 있고 얼마나 빠르게 움직이는지 기술합니다. Kinetics(운동역학)는 그 acceleration(가속도)을 만들려면 어떤 force(힘)가 필요한지 묻습니다. 따라서 track(주행로)의 geometry(기하학)뿐 아니라 타이어의 contact force(접촉력), weight(중량), air drag(공기저항)를 함께 고려합니다.',
    '강의의 핵심 전환은 “주어진 운동을 계산하기”에서 “힘과 운동을 연결하기”로 넘어가는 것입니다. Particle model(입자 모델)에서는 자동차의 크기와 rotation(회전)을 생략하고 translation(병진운동)에 집중합니다. Overview(도입 영상)의 torque(토크) 언급은 넓은 운동 원인의 예이며, 이번 입자 문제에 회전 운동방정식을 별도로 추가하라는 뜻은 아닙니다.')
add('원심분리기의 큰 속력은 큰 힘을 요구합니다','Contents 1 00:49–01:00',
    'Centrifuge(원심분리기)는 빠르게 회전하면서 내용물의 velocity direction(속도 방향)을 계속 바꿉니다. 직전 렉처의 normal acceleration(법선가속도) v²/ρ를 이번 렉처의 force(힘)와 연결하면 arm(막대)이 견뎌야 할 하중을 이해할 수 있습니다.',
    '시험용 보강: 일정한 radius(반지름)에서 mass(질량)와 speed(속력)가 각각 m, v이면 필요한 inward resultant(안쪽 알짜힘)의 크기는 mv²/ρ입니다. Speed(속력)가 두 배가 되면 같은 radius(반지름)에서 필요한 force(힘)는 네 배입니다. 이는 새 종류의 힘을 추가하는 식이 아니라 실제 힘들의 합이 만족해야 하는 조건입니다.',eq='ΣFₙ = mv²/ρ')
add('뉴턴 제2법칙에는 적용 조건이 있습니다','Contents 1 01:06–02:03',
    'Newton’s second law(뉴턴 제2법칙)는 resultant force(합력)와 acceleration(가속도)을 연결합니다. Σ는 물체에 작용하는 모든 external forces(외력)를 vector sum(벡터합)으로 더한다는 뜻입니다. Mass(질량)가 양수이면 acceleration(가속도)은 resultant force(합력)와 같은 direction(방향)을 향합니다. 개별 force(힘)나 velocity(속도)와 반드시 같은 방향인 것은 아닙니다.',
    '여기서는 constant mass(일정한 질량)와 inertial reference frame(관성 기준좌표계)을 가정합니다. 관성계는 다른 관성계에 대해 accelerating(가속)하거나 rotating(회전)하지 않는 기준입니다. Constant-velocity translation(등속 병진)도 허용됩니다. 영상은 지구 고정축을 많은 공학 문제에서 근사 관성계로 취급하지만 지구가 정확한 관성계는 아니라고 설명합니다.',eq='Σ<b>F</b> = m<b>a</b>')
add('선운동량은 질량과 속도벡터의 곱입니다','Contents 1 02:07–02:55',
    'Linear momentum(선운동량)은 mass(질량)와 velocity(속도)의 곱입니다. 이 강의는 기호 <b>L</b>을 사용하며, 다른 교재의 <b>p</b>와 같은 물리량입니다. <b>L</b>이 이 슬라이드에서 angular momentum(각운동량)을 뜻한다고 혼동하지 마십시오. Direction(방향)은 velocity(속도)와 같고 SI unit(SI 단위)은 kg·m/s입니다.',
    'Acceleration(가속도)을 d<b>v</b>/dt로 바꾸고 constant mass(일정한 질량)를 미분 기호 안으로 넣으면 Σ<b>F</b> = d(m<b>v</b>)/dt를 얻습니다. 즉 force(힘)는 momentum(운동량)의 time rate of change(시간 변화율)입니다. 이번 유도는 constant-mass particle(일정 질량의 입자)을 대상으로 하므로 질량이 드나드는 계에 그대로 대입하지 않습니다.',eq='<b>L</b> = m<b>v</b><br>Σ<b>F</b> = d<b>L</b>/dt')
add('합력이 0이면 선운동량 벡터가 보존됩니다','Contents 1 02:57–03:03',
    'Resultant force(합력)가 zero(0)이면 d<b>L</b>/dt = 0이므로 linear momentum(선운동량)은 constant(일정)합니다. 여기서 일정하다는 것은 magnitude(크기)뿐 아니라 direction(방향)도 변하지 않는다는 뜻입니다. Constant mass(일정한 질량)인 입자는 constant velocity(일정한 속도)를 유지합니다.',
    '시험용 보강: Σ<b>F</b> = 0은 각 force(힘)가 모두 없다는 뜻이 아닙니다. 여러 force(힘)가 상쇄될 수 있습니다. 또한 speed(속력)만 일정한 circular motion(원운동)은 direction(방향)이 변하므로 이 momentum conservation(운동량 보존)의 예가 아닙니다.',eq='Σ<b>F</b> = 0 ⇒ <b>L</b> = constant(일정)')
add('힘·질량·길이·시간의 단위는 서로 연결됩니다','Contents 1 03:10–04:06',
    'Force(힘), mass(질량), length(길이), time(시간)의 네 primary dimensions(주요 차원)는 Newton’s second law(뉴턴 제2법칙)로 묶입니다. 세 가지의 unit(단위)을 정하면 나머지 하나는 그 법칙과 compatible(양립 가능)해야 합니다. 서로 다른 단위계의 숫자를 그대로 섞으면 식의 모양이 맞아도 답이 틀립니다.',
    '이 과목은 주로 SI units(SI 단위계)를 사용합니다. 문제를 읽을 때 mass(질량)가 kg인지, weight(중량)가 N인지 먼저 확인하고 km/h는 m/s로 바꾸어 대입합니다. Dimension(차원)은 물리량의 종류이고 unit(단위)은 그 크기를 재는 기준입니다.',eq='[F] = [M][L][T]⁻²')
add('뉴턴은 kg·m/s²로 정의됩니다','Contents 1 04:17–04:46',
    'SI units(SI 단위계)의 기본 단위는 length(길이)에 m, mass(질량)에 kg, time(시간)에 s입니다. Force(힘)의 단위 N은 mass(질량) 1 kg에 acceleration(가속도) 1 m/s²를 주는 force(힘)로 정의됩니다. 따라서 N은 독립된 임의 기준이 아니라 derived unit(유도단위)입니다.',
    'Weight(중량)는 gravity(중력)가 만드는 force(힘)이므로 W = mg입니다. 지표면 근처에서 g = 9.81 m/s²를 사용하면 mass(질량) 1 kg의 weight(중량)는 약 9.81 N입니다. Mass(질량)와 weight(중량)의 숫자와 단위가 서로 다르다는 점을 유지해야 합니다.',eq='1 N = 1 kg·m/s²<br>W = mg')
add('미국 관용단위에서는 힘과 질량의 파운드를 구별합니다','Contents 1 04:53–05:13',
    'U.S. customary units(미국 관용단위계)에서는 force(힘)에 pound-force(파운드힘, lbf), length(길이)에 foot(피트, ft), time(시간)에 s를 쓰는 일관된 구성을 사용할 수 있습니다. 이때 mass(질량)의 coherent unit(일관된 단위)은 slug(슬러그)입니다. 원본의 length(m) 표기는 바로 아래 ft 기반 식과 맞지 않아 본문에서는 ft로 교정합니다.',
    '슬라이드의 lb 표기는 force(힘)와 mass(질량)에 혼용되어 있습니다. 본문에서는 lbf와 lbm을 구별합니다. 1 slug = 1 lbf·s²/ft이며 약 32.2 lbm입니다. SI 문제라면 kg·m·s·N으로 통일하는 것이 안전합니다.',eq='1 slug = 1 lbf·s²/ft<br>1 lbf = (1 slug)(1 ft/s²)')
add('운동방정식은 힘과 가속도의 등식입니다','Contents 1 05:18–05:33',
    'Equation of motion(운동방정식)은 Newton’s second law(뉴턴 제2법칙)를 실제 물체의 조건에 맞춰 쓴 식입니다. 왼쪽은 external forces(외력)의 합, 오른쪽은 mass(질량)와 absolute acceleration(절대가속도)의 곱입니다. Unknown(미지수)이 force(힘)인지 acceleration(가속도)인지에 따라 같은 식으로 서로 다른 문제를 풉니다.',
    '시험용 보강: 물체가 initially at rest(처음 정지)라는 이유로 Σ<b>F</b> = 0을 쓰면 안 됩니다. Rest(정지)는 velocity(속도)의 조건일 뿐, 그 순간 acceleration(가속도)을 정하지 않습니다. Equilibrium(평형) 여부는 acceleration(가속도)과 force balance(힘의 평형)를 통해 판단합니다.',eq='Σ<b>F</b> = m<b>a</b>')
add('직교좌표에서는 각 축마다 운동방정식을 씁니다','Contents 1 05:39–06:26',
    'Rectangular coordinates(직교좌표)의 fixed unit vectors(고정 단위벡터) <b>i</b>, <b>j</b>, <b>k</b>에 따라 force(힘)와 acceleration(가속도)을 분해합니다. Vector equation(벡터 방정식) 하나는 세 개의 scalar component equations(스칼라 성분 방정식)과 동등합니다. 모든 항은 같은 positive direction(양의 방향)에 따라 부호를 붙여야 합니다.',
    '한 축의 acceleration(가속도)이 0이면 그 축에서만 force balance(힘의 평형)가 성립합니다. 예를 들어 수평으로 움직이는 블록의 vertical acceleration(수직가속도)은 0이어도 horizontal acceleration(수평가속도)은 0이 아닐 수 있습니다. 원본 아래 줄의 ΣFₓ = mÿ는 축 아래첨자 오타이며 ΣFᵧ = mÿ가 맞습니다.',eq='ΣFₓ = mẍ<br>ΣFᵧ = mÿ<br>ΣF𝓏 = mz̈')
add('자유물체도는 주변 물체를 힘으로 바꾼 그림입니다','Contents 1 06:28–08:57',
    'Free-body diagram(자유물체도, FBD)은 body of interest(관심 물체)를 isolate(분리)하고 그 물체에 작용하는 external forces(외력)를 그린 그림입니다. “Free(자유로운)”는 force-free(힘이 없음)가 아니라 주변 물체에서 개념적으로 떼어냈다는 뜻입니다. Coordinate axes(좌표축)를 정하고 applied force(작용력), weight(중량), normal force(수직항력), friction force(마찰력)를 표시합니다.',
    '그림의 wedge(쐐기)를 지워도 접촉의 효과는 사라지지 않습니다. 지운 support(지지물)를 normal force(수직항력)와 friction force(마찰력)로 replace(대체)해야 합니다. 225 N cable tension(케이블 장력)은 줄 방향, weight(중량)는 수직 아래, normal force(수직항력)는 접촉면에 수직입니다. Inclined axes(기울어진 축)를 선택하면 경사면 방향의 성분 계산이 단순해집니다.')
add('운동도에는 실제 힘 대신 ma를 표시합니다','Contents 1 09:05–09:43',
    'Kinetic diagram(운동도, KD)은 같은 물체에 mass times acceleration(질량×가속도)을 표시합니다. FBD(자유물체도)가 원인인 external forces(외력)를 보인다면 KD(운동도)는 그 결과와 연결되는 inertial terms(관성항)를 보입니다. 그림 두 개 사이의 등호는 Σ<b>F</b> = m<b>a</b>를 시각화한 것입니다.',
    'Unknown acceleration(미지의 가속도)은 선택한 positive direction(양의 방향)으로 먼저 그릴 수 있습니다. 계산 결과가 negative(음수)이면 실제 방향이 반대입니다. 시험용 보강: 이 강의의 FBD(자유물체도)에 m<b>a</b>를 또 하나의 applied force(작용력)로 추가하면 같은 효과를 중복 계산하게 됩니다.')
add('도르래가 부착된 쐐기는 계의 경계부터 정합니다','Contents 1 09:46–10:22',
    '문제의 관심 대상은 block A(블록 A)이며, A에 부착된 massless pulleys(질량 없는 도르래)도 선택한 system(계)에 포함합니다. Block B(블록 B), cable(케이블), ground(지면)는 이 system boundary(계의 경계) 밖에 있습니다. 원본의 massless(질량 없는)·frictionless(마찰 없는) 조건은 도르래에 관한 것으로 접촉면 전체가 frictionless(마찰 없는)라는 뜻은 아닙니다.',
    'System boundary(계의 경계)를 정하면 무엇이 external force(외력)인지 정해집니다. B와 바닥을 분리한 자리에는 각 contact force(접촉력)를, 줄이 도르래나 A를 당기는 자리에는 tension(장력)을 표시합니다. 그림에 pulley(도르래)가 여러 개 있다고 모든 force(힘)를 한 화살표로 합치기 전에 각각의 줄 방향을 확인합니다.')
add('A를 분리해도 접촉과 장력의 효과는 남습니다','Contents 1 10:24–11:17',
    '순서는 isolate(분리) → axes(좌표축) → applied forces(작용력) → support reactions(지지반력) → angles(각도) → KD(운동도)입니다. A 위의 B를 제거한 뒤에는 B가 A를 누르는 normal reaction(수직반력)과 접촉면의 friction force(마찰력)를 추가합니다. 바닥에서도 같은 절차로 지면의 반력을 표시합니다.',
    '영상은 도르래를 지운다는 표현을 쓰지만, 원본이 정한 A+부착 도르래의 system boundary(계의 경계)를 유지해야 합니다. 도르래의 질량을 무시하는 것과 그 도르래에 작용하는 cable forces(케이블 힘)를 없애는 것은 다릅니다. 최종 FBD(자유물체도)는 이 힘들을 보존합니다.')
add('A의 자유물체도와 운동도를 읽는 방법','Contents 1 11:21–11:31',
    '빨간 화살표는 cable tension(케이블 장력), weight(중량), B와의 contact forces(접촉력), 지면과의 contact forces(접촉력)입니다. 같은 ideal cable(이상 케이블)의 tension magnitude(장력 크기)는 T로 같더라도 각 줄의 direction(방향)은 다릅니다. A에 작용하는 힘과 A가 B에 가하는 reaction(반작용)을 한 FBD(자유물체도)에 함께 그리지 않습니다.',
    '파란 KD(운동도)는 A가 지면의 straight incline(직선 경사면)을 따라 움직인다는 constraint(구속조건)를 반영합니다. 지면과 접촉을 유지하면 지면 수직 방향 acceleration(가속도)은 0입니다. 그림의 friction directions(마찰 방향)는 가정된 화살표이며, 실제 sliding direction(미끄럼 방향) 또는 impending motion(임박 운동)에 맞는지 확인해야 합니다.')
add('Lecture 4-3 · 곡선운동의 힘 성분','Contents 2','회전 막대의 FBD(자유물체도)를 시작으로 path coordinates(경로좌표)와 polar coordinates(극좌표)의 운동방정식을 연결합니다.',role='Divider')
add('회전 막대 위 칼라의 운동 조건을 읽습니다','Contents 2 00:17–00:52',
    'Collar B(칼라 B)는 rod(막대)를 따라 slide(미끄러짐)할 수 있으며, rod(막대)는 O를 중심으로 rotate(회전)합니다. 이번 예는 vertical plane(수직평면) 운동이고 friction(마찰)이 존재합니다. θ is increasing(θ가 증가한다)는 angular velocity(각속도)가 양수라는 뜻이지 radial velocity(반지름 방향 속도) ṙ의 부호까지 지정하는 것은 아닙니다.',
    'Polar coordinates(극좌표)를 선택하면 eᵣ는 막대 바깥 방향, eθ는 θ 증가 방향입니다. Weight(중량)는 여전히 수직 아래로 작용하므로 두 극좌표 성분을 가집니다. Horizontal plane(수평평면) 예제와 달리 weight(중량)를 운동평면 밖이라고 생략할 수 없습니다.')
add('칼라에 작용하는 세 힘을 분리합니다','Contents 2 00:56–01:07 및 01:12–02:23',
    'Collar(칼라)를 분리하면 weight(중량) mg, rod normal force(막대 수직항력) N, rod friction(막대 마찰력) Ff가 남습니다. Normal force(수직항력)는 rod(막대)에 perpendicular(수직)하고 friction force(마찰력)는 rod(막대)에 parallel(평행)합니다. Collar(칼라)의 운동 전체가 아니라 접촉면을 따른 relative sliding(상대 미끄럼)에 반대가 되는 방향을 선택합니다.',
    '원본 다음 장은 friction(마찰)을 inward(안쪽)로 그립니다. 이는 outward sliding(바깥쪽 미끄럼)을 가정한 그림으로 읽을 수 있지만, θ increasing(θ 증가)만으로 도출되는 방향은 아닙니다. ṙ를 모르는 상태에서는 가정임을 표시하고 계산 후 sliding condition(미끄럼 조건)과 대조합니다.')
add('극좌표 자유물체도와 운동방정식을 연결합니다','Contents 2 01:12–02:47',
    '원본의 양의 축은 eᵣ outward(바깥쪽), eθ counterclockwise(반시계 방향)입니다. Weight(중량)의 radial component(반지름 성분)는 −mg sinθ, transverse component(횡성분)는 −mg cosθ입니다. 그림처럼 N을 +eθ, friction(마찰)을 −eᵣ로 두면 아래 식을 얻습니다.',
    'KD(운동도)의 maᵣ와 maθ는 positive axes(양의 축)에 따라 가정한 관성항입니다. aᵣ = r̈ − rθ̇²이며 r̈와 다릅니다. 시험용 보강: 아래 식은 그림을 성분식으로 옮긴 것으로, 마찰 방향이 반대인 상태에서는 Ff 항의 부호를 바꾸어야 합니다.',eq='−Ff − mg sinθ = m(r̈ − rθ̇²)<br>N − mg cosθ = m(rθ̈ + 2ṙθ̇)')
add('선회할 때는 방향을 바꾸는 알짜힘이 필요합니다','Contents 2 02:52–03:19',
    'Aircraft(항공기)와 roller coaster(롤러코스터)가 turn(선회)하면 velocity direction(속도 방향)을 바꾸는 normal acceleration(법선가속도)이 생깁니다. 이때 경로의 center of curvature(곡률중심) 방향으로 net force(알짜힘)가 필요합니다. Constant speed(일정한 속력)라고 force balance(힘의 평형) 상태는 아닙니다.',
    '시험용 보강: path-normal force component(경로 법선 방향 힘 성분)와 contact normal force(접촉 수직항력)는 다른 개념입니다. 전자는 선택한 경로축에 대한 모든 힘의 성분 합이고, 후자는 실제 접촉면이 가하는 특정 force(힘)입니다. 같은 normal(법선)이라는 단어만 보고 동일시하지 않습니다.')
add('접선 성분은 속력, 법선 성분은 방향을 바꿉니다','Contents 2 03:20–03:51',
    'Path coordinates(경로좌표)에서 tangent(접선) eₜ는 진행 방향이고 normal(법선) eₙ은 center of curvature(곡률중심) 쪽입니다. Tangential acceleration(접선가속도) dv/dt는 speed(속력)의 변화율이며, normal acceleration(법선가속도) v²/ρ는 궤적이 휘어지는 효과입니다. 각각에 mass(질량)를 곱하면 Newton’s law(뉴턴 법칙)의 성분식을 얻습니다.',
    'Slowing down(감속)할 때 ΣFₜ는 negative(음수)일 수 있습니다. 반면 v²/ρ는 nonnegative(0 이상)이므로 ΣFₙ은 정한 inward normal(안쪽 법선)을 향합니다. Centripetal force(구심력)는 이러한 inward resultant(안쪽 합력)의 역할 이름이지, FBD(자유물체도)에 별도로 더하는 새 힘이 아닙니다.',eq='ΣFₜ = m dv/dt<br>ΣFₙ = mv²/ρ')
add('좌표계는 장치 이름보다 계산의 단순함으로 선택합니다','Contents 2 04:00–04:20',
    'Hydraulic actuator(유압 작동기), extending robotic arm(신장하는 로봇 팔), centrifuge(원심분리기)는 rotation(회전)과 radial motion(반지름 방향 운동)이 함께 나타나 polar coordinates(극좌표)가 편리할 수 있습니다. 원본 제목은 접선·법선 좌표라고 남아 있지만 본문과 다음 장은 radial-transverse coordinates(반지름·횡좌표)를 설명합니다.',
    '영상은 하나의 문제에 unique coordinate system(유일한 좌표계)이 정해져 있지 않다고 강조합니다. Path coordinates(경로좌표)도 사용할 수 있으나 주어진 정보가 r(t), θ(t)라면 polar coordinates(극좌표)가 직접적입니다. Coordinate choice(좌표 선택)가 바뀌어도 물리 법칙은 같습니다.')
add('극좌표에서는 회전하는 기저벡터의 효과까지 넣습니다','Contents 2 04:22–05:40',
    'Polar coordinates(극좌표)의 position vector(위치벡터)는 <b>r</b> = reᵣ입니다. 이를 미분하면 <b>v</b> = ṙeᵣ + rθ̇eθ이고, 다시 미분하면 아래 acceleration components(가속도 성분)를 얻습니다. Unit vectors(단위벡터)가 rotating(회전)하므로 좌표 r, θ의 미분만으로는 충분하지 않습니다.',
    'Radial term(반지름 항)의 −rθ̇²와 transverse term(횡항)의 2ṙθ̇를 빠뜨리지 않습니다. 시험용 보강: rotating basis(회전 기저)를 사용한다고 곧바로 rotating observer(회전 관측자)의 상대가속도를 쓰는 것은 아닙니다. 아래 식은 fixed origin(고정 원점)에 대한 absolute acceleration(절대가속도)을 회전 기저로 표현한 것입니다.',eq='ΣFᵣ = m(r̈ − rθ̇²)<br>ΣFθ = m(rθ̈ + 2ṙθ̇)')
add('Lecture 4-4 · 문제풀이','Problem Solving','힘 분해, 도르래 구속조건, 움직이는 쐐기, 경사진 도로, 회전 막대의 예제로 원리를 적용합니다.',role='Divider')

add('예제 1 · 비스듬히 미는 힘을 구합니다','Problem Solving 00:17–00:51',
    'Mass(질량) 80 kg의 block(블록)을 수평 아래쪽 30°로 push(밀기)하여 rightward acceleration(오른쪽 가속도) 2.5 m/s²를 만들려 합니다. Coefficient of kinetic friction(운동마찰계수)은 μₖ = 0.25입니다. Determine the magnitude(크기를 구하라)의 대상은 applied force(작용력) P입니다.',
    'P의 horizontal component(수평성분)는 가속에 기여하지만 downward component(아래쪽 성분)는 normal force(수직항력)를 키웁니다. 따라서 처음부터 N = mg라고 놓을 수 없습니다. 원문 rests(놓여 있다/정지해 있다)와 kinetic friction(운동마찰) 조건은 구분하여, 계산은 sliding(미끄러지는) 단계에 적용합니다.')
add('예제 1 · 미지수 P와 N을 두 식으로 풉니다','Problem Solving 01:00–01:29',
    'Rectangular coordinates(직교좌표)를 +x rightward(오른쪽), +y upward(위쪽)으로 정합니다. Unknowns(미지수)는 P와 normal reaction(수직반력) N입니다. Friction force(마찰력)는 Fₖ = μₖN으로 연결되므로 별개의 독립 미지수를 늘리지 않습니다.',
    'Horizontal equation(수평방정식)의 우변은 maₓ = 200 N이고 vertical equation(수직방정식)의 우변은 0입니다. 서로 다른 축에서 우변이 다른 것은 모순이 아닙니다. Block(블록)이 바닥과 contact(접촉)를 유지하면서 높이가 일정하다는 constraint(구속조건)를 쓰는 것입니다.')
add('예제 1 · 수평 힘에서 마찰을 뺍니다','Problem Solving 01:38–03:00',
    'FBD(자유물체도)에는 P, mg, N, Fₖ가 있습니다. Rightward sliding(오른쪽 미끄럼)을 가정하면 friction(마찰)은 leftward(왼쪽)이고, P의 수평성분은 P cos30°입니다. 따라서 ΣFₓ = P cos30° − μₖN입니다.',
    'm = 80 kg와 aₓ = 2.5 m/s²를 곱한 200의 unit(단위)은 N입니다. Weight(중량) 785 N을 mass(질량) 자리에 넣으면 안 됩니다. KD(운동도)에는 rightward(오른쪽) ma만 표시됩니다.',eq='P cos30° − 0.25N = 80 × 2.5 = 200 N')
add('예제 1 · 누르는 힘 때문에 수직항력이 커집니다','Problem Solving 03:07–04:03',
    'Vertical acceleration(수직가속도)이 0이므로 upward normal force(위쪽 수직항력)는 weight(중량)와 P의 downward component(아래쪽 성분)의 합을 상쇄해야 합니다. P sin30°가 아래로 향하므로 수직방정식에서 negative(음수)입니다.',
    '따라서 N = mg + P sin30°이며 N은 mg보다 큽니다. P를 크게 하면 friction(마찰)도 증가하므로, P의 수평성분 전부가 acceleration(가속도) 증가로 이어지지 않습니다. 아래는 중간 반올림을 하지 않은 mg = 784.8 N을 사용합니다.',eq='N − P sin30° − mg = 0<br>N = 784.8 + 0.5P')
add('예제 1 · 연립해 P ≈ 535 N을 얻습니다','Problem Solving 04:05–04:18',
    'Vertical equation(수직방정식)에서 얻은 N을 horizontal equation(수평방정식)에 substitute(대입)하면 P 하나의 식이 됩니다. P(cos30° − 0.25 sin30°) = 80(2.5 + 0.25×9.81)입니다. 이를 풀면 P ≈ 534.66 N이므로 원본 답안 535 N과 일치합니다.',
    '시험용 보강: N ≈ 1052.13 N, Fₖ ≈ 263.03 N입니다. 수평에서 P cos30° − Fₖ ≈ 200 N인지, 수직에서 N − P sin30° − mg ≈ 0인지 대입해 확인할 수 있습니다. 원본은 mg를 785 N으로 먼저 반올림했습니다.',eq='P = m(aₓ + μₖg)/(cos30° − μₖ sin30°)<br>P ≈ 535 N')
add('예제 1 · 정지마찰은 항상 μₛN이 아닙니다','Problem Solving 04:22–04:56',
    'Static friction(정지마찰)은 impending sliding(미끄러지기 직전)까지 필요한 크기로 조절되며 |Fₛ| ≤ μₛN입니다. 원본의 F = μₛN은 maximum static friction(최대정지마찰)을 나타내는 한계식으로 해석해야 합니다. Sliding(미끄럼)이 시작된 뒤에는 kinetic friction(운동마찰) Fₖ = μₖN을 사용합니다.',
    '이 문제에는 μₛ가 없으므로 정지 상태에서 출발 가능한 P의 별도 문턱값은 수치로 구할 수 없습니다. 계산한 535 N은 주어진 kinetic-friction model(운동마찰 모델)에서 지정 acceleration(가속도)을 만드는 값입니다. Downward push(아래로 누르는 힘)가 N과 friction(마찰)을 키운다는 결론은 이 식에서도 확인됩니다.',eq='|Fₛ| ≤ μₛN<br>Fₛ,max = μₛN,  Fₖ = μₖN')
add('예제 2 · 움직도르래와 두 블록','Problem Solving 05:01–05:35',
    'Block A(블록 A)는 100 kg이고 horizontal plane(수평면) 위에 있습니다. Block B(블록 B)는 300 kg이며 movable pulley C(움직도르래 C)에 연결되어 있습니다. Surface(면)와 pulleys(도르래)는 frictionless(마찰 없음), pulley mass(도르래 질량)는 negligible(무시 가능)하다고 가정합니다.',
    'Starts from rest(정지 출발)는 initial velocity(초기속도)가 0임을 뜻합니다. 구하는 것은 각 block acceleration(블록 가속도)과 cord tension(줄 장력)입니다. 같은 줄의 장력 T₁과 B를 직접 매다는 연결부 장력 T₂는 서로 다른 값입니다. 그림의 줄 경로를 먼저 읽어야 합니다.')
add('예제 2 · 운동학 조건과 힘의 조건을 함께 씁니다','Problem Solving 05:41–06:12',
    'Cable length(케이블 길이)가 일정하므로 A와 B는 dependent motion(종속운동)을 합니다. 먼저 acceleration relation(가속도 관계)을 구한 뒤 A, B, massless pulley(질량 없는 도르래)의 FBD(자유물체도)를 각각 그립니다.',
    'Kinematic constraint(운동학적 구속조건)는 움직임의 비율을, equation of motion(운동방정식)은 실제 acceleration(가속도)와 tension(장력)의 크기를 결정합니다. 길이 조건만으로 힘을 정할 수도 없고, ΣF = ma만 쓰고 가속도 관계를 생략할 수도 없습니다.')
add('예제 2 · 줄 길이를 두 번 미분합니다','Problem Solving 06:16–09:08',
    '+xₐ를 rightward(오른쪽), +yᵦ를 downward(아래쪽)로 잡습니다. A가 오른쪽으로 움직이면 수평 줄은 xₐ만큼 짧아지고, B가 아래로 움직이면 움직도르래를 받치는 두 수직 줄은 각각 yᵦ만큼 길어집니다. 따라서 −xₐ + 2yᵦ = C입니다.',
    'C는 fixed lengths(고정 길이)와 origin choice(원점 선택)를 포함한 constant(상수)입니다. 원본 yᵦ = xₐ/2는 C = 0이 되도록 좌표를 잡은 특별한 표현입니다. 어떤 원점을 택해도 두 번 differentiate(미분)하면 −aₐ + 2aᵦ = 0이므로 aᵦ = aₐ/2가 됩니다.',eq='−xₐ + 2yᵦ = C<br>aᵦ = aₐ/2')
add('예제 2 · A의 수평 가속도는 T₁이 만듭니다','Problem Solving 09:12–09:38',
    'A의 FBD(자유물체도)는 weight(중량), normal force(수직항력), rightward tension(오른쪽 장력) T₁입니다. Frictionless surface(마찰 없는 면)이므로 수평의 다른 저항력은 없습니다. Vertical acceleration(수직가속도)은 0이어서 N = mₐg이고, 수평방정식은 T₁ = mₐaₐ입니다.',
    'T₁은 A의 mass(질량) 100 kg에 aₐ를 곱한 값입니다. B의 weight(중량)를 이 식의 T₁에 바로 대입하면 B의 acceleration(가속도)과 pulley force ratio(도르래 힘 비율)를 모두 무시하게 됩니다.',eq='T₁ = 100aₐ')
add('예제 2 · B에서는 중량과 장력의 차가 가속도를 만듭니다','Problem Solving 09:46–10:28',
    'B의 positive direction(양의 방향)은 downward(아래쪽)입니다. Weight(중량) mᵦg는 positive(양수), upward tension(위쪽 장력) T₂는 negative(음수)로 씁니다. 따라서 mᵦg − T₂ = mᵦaᵦ입니다.',
    'B가 아래로 accelerate(가속)하면 T₂는 mᵦg보다 작습니다. Suspended(매달린) 물체라고 항상 tension equals weight(장력=중량)는 아닙니다. 원본은 300×9.81 = 2943 N을 약 2940 N으로 반올림하여 풉니다.',eq='T₂ = 300g − 300aᵦ')
add('예제 2 · 질량 없는 도르래는 T₂ = 2T₁을 줍니다','Problem Solving 10:34–11:15',
    'Pulley C(도르래 C)를 분리하면 두 rope segments(줄 구간)가 위쪽으로 각각 T₁을 가하고, B와의 연결부가 아래쪽으로 T₂를 가합니다. Pulley mass(도르래 질량)를 0으로 모델링하므로 ΣFᵧ = mCaC = 0입니다. 이 식에서 T₂ − 2T₁ = 0을 얻습니다.',
    'Massless(질량 없음)가 acceleration zero(가속도 0)를 뜻하지는 않습니다. 도르래는 B와 함께 가속하지만 유한한 acceleration(가속도)에 질량 0을 곱한 관성항이 0인 것입니다. 같은 ideal cable(이상 케이블)의 양쪽 T₁이 같은 것과 연결부 T₂가 같은 것은 구분해야 합니다.',eq='T₂ − 2T₁ = 0')
add('예제 2 · 네 관계식을 묶습니다','Problem Solving 11:18–11:23',
    'Unknowns(미지수)는 aₐ, aᵦ, T₁, T₂ 네 개입니다. A의 horizontal equation(수평방정식), B의 vertical equation(수직방정식), massless pulley(질량 없는 도르래)의 force relation(힘 관계), cable constraint(케이블 구속조건) 네 개를 사용합니다.',
    'aᵦ = aₐ/2를 B 식에 넣고 T₁ = 100aₐ, T₂ = 2T₁을 대입하면 aₐ 하나의 식으로 줄어듭니다. 이 단계가 kinetics(운동역학)와 kinematics(운동학)를 실제로 연결하는 부분입니다.',eq='T₁ = 100aₐ,  T₂ = 300g − 300aᵦ<br>T₂ = 2T₁,  aᵦ = aₐ/2')
add('예제 2 · 가속도와 두 장력을 구합니다','Problem Solving 11:29–11:31',
    '300g − 150aₐ = 200aₐ이므로 aₐ = 300g/350입니다. g = 9.81 m/s²이면 aₐ ≈ 8.409 m/s² rightward(오른쪽), aᵦ ≈ 4.204 m/s² downward(아래쪽), T₁ ≈ 840.9 N, T₂ ≈ 1681.7 N입니다. 원본의 중간 반올림을 따르면 8.40, 4.20, 840, 1680을 얻습니다.',
    '원본 파란 답안 상자의 마지막 줄 T₂ − 2T₁ = 1680 N은 잘못된 표기입니다. 올바른 답은 T₂ = 2T₁ = 1680 N이고, T₂ − 2T₁은 0이어야 합니다. 앞선 도르래 운동방정식과 직접 대조하여 교정했습니다.',eq='aₐ ≈ 8.40 m/s²,  aᵦ ≈ 4.20 m/s²<br>T₁ ≈ 840 N,  T₂ ≈ 1680 N')
add('예제 2 · 계를 묶으면 내부 장력은 사라집니다','Problem Solving 11:35–12:08',
    'B와 pulley C(도르래 C)를 하나의 system(계)으로 선택하면 연결부의 T₂는 internal force(내력)가 됩니다. 두 물체 사이의 action-reaction pair(작용·반작용 쌍)가 전체 계에서는 상쇄되므로 합쳐진 FBD(자유물체도)에 T₂를 그릴 필요가 없습니다.',
    '외부에서 위로 당기는 두 T₁과 아래로 작용하는 mᵦg는 남아 mᵦg − 2T₁ = mᵦaᵦ가 됩니다. 이는 별개로 푼 세 힘 식과 같은 결과입니다. Internal(내부)인지 external(외부)인지는 힘의 고유 속성이 아니라 선택한 system boundary(계의 경계)에 달려 있습니다.')
add('예제 3 · 블록이 미끄러지면 쐐기도 움직입니다','Problem Solving 12:12–13:03',
    'Mass(질량) 6 kg인 B가 mass(질량) 15 kg인 wedge A(쐐기 A)의 30° 경사면을 따라 slide(미끄러짐)합니다. 모든 friction(마찰)은 neglect(무시)하고 바닥은 horizontal(수평)입니다. B는 left-downward(왼쪽 아래)로 상대 이동하고 A는 rightward(오른쪽)로 움직입니다.',
    '구하는 것은 wedge acceleration(쐐기 가속도) aₐ와 block acceleration relative to the wedge(쐐기에 대한 블록의 상대가속도) aᵦ/ₐ입니다. B의 absolute acceleration(절대가속도)은 두 벡터의 합이므로 incline direction(경사면 방향)만으로 표시하면 틀립니다.')
add('예제 3 · 상대가속도 관계로 시작합니다','Problem Solving 13:08–13:48',
    'Wedge(쐐기)는 rotate(회전)하지 않고 translate(병진)하므로 <b>a</b>ᵦ = <b>a</b>ₐ + <b>a</b>ᵦ/ₐ를 사용합니다. Relative acceleration(상대가속도)은 경사면 아래로, wedge acceleration(쐐기 가속도)은 수평 오른쪽으로 잡습니다.',
    '각 물체의 FBD(자유물체도)를 그리고 Newton’s second law(뉴턴 제2법칙)에 이 absolute acceleration(절대가속도)을 넣습니다. Moving wedge(움직이는 쐐기)를 관성계처럼 취급하여 ΣF = maᵦ/ₐ라고 쓰지 않는 것이 핵심입니다.')
add('예제 3 · 두 가속도 화살표의 합이 B의 가속도입니다','Problem Solving 13:52–14:50',
    '그림에서 A의 aₐ는 horizontal rightward(수평 오른쪽)이고 aᵦ/ₐ는 down the incline(경사면 아래쪽)입니다. 각각 magnitude(크기)를 양수로 정의한 두 벡터를 더해야 B의 absolute acceleration(절대가속도)이 됩니다.',
    '시험용 보강: 지면의 +X를 오른쪽, +Y를 위쪽으로 두면 aᵦX = aₐ − aᵦ/ₐ cos30°, aᵦY = −aᵦ/ₐ sin30°입니다. 아래는 vector relation(벡터 관계)이며, 크기를 단순히 더하는 aᵦ = aₐ + aᵦ/ₐ와는 다릅니다.',eq='<b>a</b>ᵦ = <b>a</b>ₐ + <b>a</b>ᵦ/ₐ')
add('예제 3 · 쐐기 수평축과 블록 경사축을 나눕니다','Problem Solving 14:57–16:11',
    'A에는 floor normal force(바닥 수직항력), weight(중량), B가 누르는 contact normal force(접촉 수직항력) N₁이 작용합니다. N₁의 horizontal component(수평성분) N₁ sin30°가 A를 가속하므로 N₁ sin30° = mₐaₐ입니다.',
    'B에서는 +x를 up the incline(경사면 위쪽)로 정합니다. Weight(중량)의 성분은 −mᵦg sin30°이고, absolute acceleration component(절대가속도 성분)는 aₐ cos30° − aᵦ/ₐ입니다. 두 물체에서 x라는 이름의 축이 서로 다르므로 방향을 함께 확인하십시오.',eq='N₁ sin30° = mₐaₐ<br>−mᵦg sin30° = mᵦ(aₐ cos30° − aᵦ/ₐ)<br>aᵦ/ₐ = aₐ cos30° + g sin30°')
add('예제 3 · 경사면 수직의 절대가속도는 0이 아닙니다','Problem Solving 16:17–16:38',
    'B의 +y축을 away from the incline(경사면에서 바깥쪽)으로 정합니다. B가 면을 떠나지 않으므로 relative acceleration(상대가속도)의 y성분은 0입니다. 그러나 A가 수평으로 accelerate(가속)하므로 B의 absolute acceleration(절대가속도)에는 −aₐ sin30° 성분이 남습니다.',
    '따라서 N₁ − mᵦg cos30° = −mᵦaₐ sin30°입니다. Stationary incline(정지 경사면)의 N₁ = mᵦg cos30°를 그대로 사용하면 이 항을 놓칩니다. “상대적으로 면을 뚫고 움직이지 않는다”와 “절대 수직가속도가 0이다”는 다른 문장입니다.',eq='N₁ − mᵦg cos30° = −mᵦaₐ sin30°')
add('예제 3 · 쐐기는 오른쪽으로 약 1.545 m/s² 가속합니다','Problem Solving 16:45–16:56',
    '첫 식 0.5N₁ = mₐaₐ에서 N₁ = 2mₐaₐ를 얻어 B의 경사면 수직방정식에 대입합니다. 그러면 (2mₐ + mᵦ sin30°)aₐ = mᵦg cos30°가 되어 aₐ를 구할 수 있습니다.',
    'mₐ = 15 kg, mᵦ = 6 kg를 넣으면 aₐ ≈ 1.5447 m/s²입니다. Positive(양수) 결과이므로 가정한 rightward(오른쪽) 방향이 맞습니다. 시험용 보강: N₁ = 2mₐaₐ ≈ 46.34 N으로 positive(양수)이므로 선택한 접촉 방향과도 일치합니다.',eq='aₐ = mᵦg cos30°/(2mₐ + mᵦ sin30°)<br>aₐ ≈ 1.545 m/s²')
add('예제 3 · 상대가속도는 경사면 아래로 약 6.24 m/s²입니다','Problem Solving 17:00–17:03',
    '구한 aₐ를 aᵦ/ₐ = aₐ cos30° + g sin30°에 대입합니다. 첫 항 약 1.3377과 둘째 항 4.905를 더하면 aᵦ/ₐ ≈ 6.2427 m/s²입니다. 이 값의 방향은 down the incline(경사면 아래쪽)입니다.',
    'Stationary wedge(정지 쐐기)라면 relative acceleration(상대가속도)은 g sin30°뿐이지만, moving wedge(움직이는 쐐기)에서는 aₐ cos30°가 추가됩니다. 시험 답안에 relative to A(A에 대한 상대)와 direction(방향)을 함께 써야 6.24의 물리적 의미가 분명해집니다.',eq='aᵦ/ₐ ≈ 6.24 m/s², down the incline(경사면 아래쪽)')
add('예제 3 · 경사면 방향은 상대가속도의 방향입니다','Problem Solving 17:11–17:35',
    '원본은 B의 KD(운동도)에 경사면 아래 방향 ma 하나만 그리는 실수를 경고합니다. 그 방향은 relative acceleration(상대가속도)의 방향이고, Newton’s law(뉴턴 법칙)의 우변에는 absolute acceleration(절대가속도)이 필요합니다.',
    '시험용 보강: 지면 좌표에서 <b>a</b>ᵦ ≈ −3.862<b>i</b> − 3.121<b>j</b> m/s²입니다. 이 벡터는 경사면의 30° 아래 방향과 일치하지 않습니다. A와 B의 horizontal momentum(수평운동량)을 비교하면 15aₐ + 6aᵦX ≈ 0도 만족하여 내부 접촉력이 서로 상쇄됨을 확인할 수 있습니다.')
add('예제 3 · 고정 수평·수직축으로도 같은 답을 얻습니다','Problem Solving 17:41–17:59',
    'B의 unknown acceleration components(미지의 가속도 성분)를 aᵦX, aᵦY로 직접 두고 fixed rectangular axes(고정 직교축)에서 ΣF = ma를 써도 됩니다. 여기에 aᵦX = aₐ − aᵦ/ₐ cos30°, aᵦY = −aᵦ/ₐ sin30°를 추가하면 앞의 inclined-axis method(경사축 방법)와 동일합니다.',
    'Coordinate choice(좌표 선택)는 풀이의 표현을 바꾸지만 force law(힘 법칙)나 답을 바꾸지 않습니다. 중요한 것은 모든 force components(힘 성분)와 acceleration components(가속도 성분)가 같은 축에 투영되어야 한다는 점입니다.')
add('그룹 예제 1 · B를 당기는 줄 구간은 세 개입니다','Problem Solving 18:06–18:52',
    'A는 30 kg, B는 25 kg입니다. Cable(케이블)은 A에서 고정도르래를 지나 B에 부착된 movable pulley(움직도르래)를 돌아 올라간 뒤 위쪽 fixed pulley(고정도르래)를 거쳐 끝이 B에 연결됩니다. B와 함께 길이가 변하는 vertical segments(수직 줄 구간)는 세 개입니다.',
    'Massless pulleys(질량 없는 도르래)와 frictionless contacts(마찰 없는 접촉)를 가정합니다. 앞선 예제 2를 그대로 복사해 aₐ = 2aᵦ로 두면 안 됩니다. 마지막 줄 끝이 B에 부착되어 있으므로 geometry(기하학)와 force count(힘 개수)가 달라집니다.')
add('그룹 예제 1 · 구속조건과 힘의 식으로 완성한 풀이','Problem Solving 18:55–19:27 · 아래 계산은 시험용 보강',
    '영상은 strategy(풀이 전략)까지만 제시합니다. 시험용 보강: +xₐ rightward(오른쪽), +yᵦ downward(아래쪽)로 두면 constant cable length(일정한 줄 길이)로부터 −xₐ + 3yᵦ = C, aₐ = 3aᵦ입니다. A에는 T = 30aₐ, B+부착 도르래에는 25g − 3T = 25aᵦ를 씁니다.',
    'T = 90aᵦ를 B 식에 대입하면 25g = (25 + 270)aᵦ입니다. 따라서 aᵦ ≈ 0.8314 m/s² downward(아래쪽), aₐ ≈ 2.494 m/s² rightward(오른쪽), T ≈ 74.82 N입니다. 여기서 3T는 별개의 장력 세 종류가 아니라 같은 cable tension(케이블 장력)의 세 기여입니다.',eq='aₐ = 3aᵦ<br>aᵦ = 25g/(25 + 9×30)<br>T = 30aₐ ≈ 74.82 N')
add('예제 4 · 횡마찰 없이 도는 설계속도를 구합니다','Problem Solving 19:31–21:17',
    'Radius of curvature(곡률반경) ρ = 120 m인 highway curve(도로 곡선)가 bank angle(뱅크각) θ = 18°로 기울어져 있습니다. Rated speed(설계속도)는 no lateral friction force(횡방향 마찰력 없음) 조건에서 이 곡선을 따라 돌 수 있는 speed(속력)입니다.',
    '이는 모든 도로에서의 maximum safe speed(최대 안전속도)를 뜻하지 않습니다. 이번 이상 모델에서 lateral friction(횡마찰)을 0으로 놓는 특별한 속력입니다. Road-normal reaction(노면 수직반력)의 기울어진 방향이 horizontal inward force(수평 안쪽 힘)를 제공하게 됩니다.')
add('예제 4 · 노면 수직방향과 경로 법선방향은 다릅니다','Problem Solving 21:21–21:53',
    '차는 horizontal circular path(수평 원형 경로)를 따라 움직입니다. 따라서 normal acceleration(법선가속도)은 horizontal inward(수평 안쪽)이고 vertical acceleration(수직가속도)은 0입니다. 반면 contact normal reaction(접촉 수직반력) R은 tilted road surface(기울어진 노면)에 perpendicular(수직)합니다.',
    'FBD(자유물체도)에 weight(중량) W와 R을 그리고, vertical axis(수직축)와 path-normal axis(경로 법선축)로 분해합니다. Centripetal force(구심력)를 R 이외의 추가 화살표로 그리지 않습니다. R의 inward component(안쪽 성분)가 그 역할을 합니다.')
add('예제 4 · 수직 힘의 평형으로 R을 구합니다','Problem Solving 21:56–23:55',
    '차의 height(높이)가 constant(일정)하므로 ΣFᵧ = 0입니다. R의 vertical component(수직성분)는 R cosθ이고 weight(중량)는 아래 방향입니다. 따라서 R cosθ = W이며 R = W/cosθ입니다.',
    'R이 W보다 큰 이유는 R의 일부가 horizontal inward component(수평 안쪽 성분)를 담당하기 때문입니다. θ는 R과 vertical direction(수직방향) 사이의 각도로도 나타납니다. 삼각함수를 넣기 전에 그림에서 어떤 성분이 adjacent(인접)인지 확인합니다.',eq='R cosθ − W = 0<br>R = W/cosθ')
add('예제 4 · 수평 안쪽 합력은 mv²/ρ입니다','Problem Solving 24:05–24:50',
    'Path-normal direction(경로 법선방향)에는 R sinθ가 작용하고, acceleration(가속도)은 v²/ρ입니다. 따라서 R sinθ = mv²/ρ입니다. 이 방향에서는 circular motion(원운동)이므로 우변을 0으로 둘 수 없습니다.',
    '앞에서 구한 R = W/cosθ와 m = W/g를 대입하면 W tanθ = (W/g)v²/ρ입니다. W가 양쪽에서 소거되어 mass(질량)와 무관한 rated speed(설계속도)를 얻습니다. 같은 도로 기하학에서 필요한 비율 R sinθ/R cosθ가 정해지는 결과입니다.',eq='R sinθ = mv²/ρ<br>tanθ = v²/(gρ)')
add('예제 4 · 설계속도는 약 70.4 km/h입니다','Problem Solving 24:59–25:30',
    'v² = gρ tanθ에 g = 9.81 m/s², ρ = 120 m, θ = 18°를 넣으면 v ≈ 19.5575 m/s입니다. km/h로 바꾸려면 3.6을 곱하므로 약 70.4 km/h입니다. Speed(속력)는 nonnegative(0 이상)이므로 양의 제곱근을 선택합니다.',
    '자동생성 자막의 “18.50 second meter per second”는 원본 19.56 m/s 및 재계산 결과와 맞지 않습니다. 본문은 슬라이드의 값과 단위 검증을 따릅니다. 이 답에는 no lateral friction(횡마찰 없음)이라는 전제가 함께 붙습니다.',eq='v = √(gρ tanθ)<br>v ≈ 19.56 m/s ≈ 70.4 km/h')
add('예제 4 · 더 큰 뱅크각은 더 큰 설계속도에 대응합니다','Problem Solving 25:39–26:09',
    '같은 ρ에서 0 &lt; θ &lt; 90° 범위의 bank angle(뱅크각)이 커지면 tanθ가 증가하므로 rated speed(설계속도)도 증가합니다. R의 inward-to-vertical ratio(안쪽 대 수직 성분 비율)가 커져 더 큰 normal acceleration(법선가속도)을 제공할 수 있기 때문입니다.',
    '시험용 보강: 실제 차량의 안전한 속도는 friction(마찰), 노면 상태, 전복 가능성 등에도 영향을 받습니다. 여기서는 그것들을 새 조건으로 넣지 않고 원본의 ideal frictionless-lateral model(이상적인 횡마찰 없는 모델) 안에서 비교합니다.')
add('예제 4 · 필요한 방향의 방정식부터 풉니다','Problem Solving 26:13–26:41',
    '그림의 tangential direction(접선방향)은 화면 안쪽이며 rated speed(설계속도)를 구하는 식은 수직·경로 법선 두 방향으로 닫힙니다. 영상은 이번 질문이 접선 방향 force(힘)와 acceleration(가속도)을 요구하지 않아 그 방향을 따로 풀지 않았다고 설명합니다.',
    'Tangential analysis(접선 해석)를 생략했다는 사실과 접선 방향의 개별 force(힘)가 하나도 없다는 말은 다릅니다. 시험용 보강: constant speed(일정한 속력)를 추가로 가정하면 ΣFₜ = 0이지만 traction(구동력)과 drag(항력)가 각각 존재하면서 상쇄될 수 있습니다.')
add('예제 5 · 일정 각속도로 회전하는 막대 위의 자유 칼라','Problem Solving 26:44–27:47',
    'Frictionless arm(마찰 없는 막대)이 horizontal plane(수평평면)에서 constant angular velocity(일정한 각속도) ω = θ̇₀로 회전합니다. Collar B(칼라 B)는 initial radius(초기 반지름) r₀에서 release(놓아주기)됩니다. 구하는 것은 radial velocity(반지름 방향 속도) vᵣ와 막대가 가하는 horizontal force magnitude(수평 힘의 크기)를 r의 함수로 표현한 것입니다.',
    '원본의 다음 적분 하한은 vᵣ(r₀) = 0입니다. 이는 initially at rest relative to the arm(처음에 막대에 대해 정지)라는 조건이며 absolute velocity(절대속도)가 0이라는 뜻이 아닙니다. 처음에도 transverse velocity(횡속도) r₀ω가 있을 수 있습니다.')
add('예제 5 · r의 함수가 필요하므로 시간을 제거합니다','Problem Solving 27:52–28:39',
    '먼저 radial-transverse equations(반지름·횡방정식)을 씁니다. Radial equation(반지름방정식)을 integrate(적분)하면 vᵣ(r)를 얻고, 이를 transverse equation(횡방정식)에 대입하면 horizontal force(수평 힘)를 얻습니다.',
    '문제가 as a function of r(r의 함수로)라고 요구하므로 time solution(시간해)을 먼저 전부 구할 필요가 없습니다. Chain rule(연쇄법칙) r̈ = vᵣ dvᵣ/dr가 independent variable(독립변수)을 t에서 r로 바꾸어 줍니다.')
add('예제 5 · 반지름 힘이 0이어도 r̈는 0이 아닙니다','Problem Solving 28:42–29:52',
    'Frictionless arm(마찰 없는 막대)은 막대와 평행한 radial force(반지름 방향 힘)를 가하지 않습니다. 따라서 ΣFᵣ = 0이고 aᵣ = r̈ − rω² = 0입니다. 여기서 얻는 관계는 r̈ = rω²이지 r̈ = 0이 아닙니다.',
    'Horizontal force(수평 힘) F는 rod(막대)에 perpendicular(수직)하여 transverse direction(횡방향)으로 작용합니다. Constant angular velocity(일정한 각속도)이므로 θ̈ = 0이지만 2ṙω 항이 남습니다. Weight(중량)와 vertical support(수직 지지력)는 수평 운동평면 밖에서 상쇄됩니다.',eq='0 = m(r̈ − rω²)<br>Fθ = 2mṙω')
add('예제 5 · 연쇄법칙과 초기조건으로 반지름 속도를 구합니다','Problem Solving 29:55–32:51',
    'vᵣ = ṙ이므로 r̈ = dvᵣ/dt = (dvᵣ/dr)(dr/dt) = vᵣ dvᵣ/dr입니다. r̈ = rω²에 넣으면 vᵣ dvᵣ = ω²r dr입니다. Constant(일정한) ω를 적분 밖으로 꺼내고 (r₀, vᵣ=0)에서 (r, vᵣ)까지 integrate(적분)합니다.',
    '양쪽 결과는 ½vᵣ² = ½ω²(r² − r₀²)입니다. 따라서 outward motion(바깥쪽 운동)에서는 vᵣ = |ω|√(r² − r₀²)입니다. 원본은 positive rotation(양의 회전)을 가정하여 θ̇₀를 그대로 쓰지만 speed magnitude(속력 크기)를 일반적으로 표시할 때는 |ω|로 쓰는 것이 명확합니다.',eq='∫<sub>0</sub><sup>vᵣ</sup> vᵣ dvᵣ = ω²∫<sub>r₀</sub><sup>r</sup> r dr<br>vᵣ² = ω²(r² − r₀²)<br>vᵣ = |ω|√(r² − r₀²)')
add('예제 5 · 횡방향 힘은 회전과 미끄럼의 결합에서 나옵니다','Problem Solving 32:59–34:00',
    'Transverse equation(횡방정식)의 signed component(부호 있는 성분)는 Fθ = 2mωvᵣ입니다. 앞서 구한 outward radial velocity(바깥쪽 반지름 속도)를 대입하면 force magnitude(힘의 크기) |Fθ| = 2mω²√(r² − r₀²)입니다.',
    'Angular acceleration(각가속도)이 0이어도 force(힘)가 0인 것은 아닙니다. Increasing radius(증가하는 반지름)를 가진 collar(칼라)가 같은 angular velocity(각속도)를 유지하도록 arm(막대)이 횡방향으로 계속 작용합니다. 원본의 결과는 r ≥ r₀인 outward branch(바깥쪽 해)에 해당합니다.',eq='|Fθ| = 2mω²√(r² − r₀²)')
add('예제 5 · 절대 반지름 성분과 막대 상대가속도를 구분합니다','Problem Solving 34:02–34:38',
    'Absolute radial acceleration component(절대가속도의 반지름 성분)는 aᵣ = r̈ − rω² = 0입니다. 반면 acceleration relative to the rod(막대에 대한 상대가속도)는 r̈eᵣ이며 r̈ = rω²입니다. 서로 다른 물리량이므로 하나가 0이고 다른 하나가 0이 아니어도 모순이 아닙니다.',
    '전체 absolute acceleration(절대가속도)에는 aθ = 2ṙω가 남습니다. 이 예는 force component(힘 성분)가 어떤 coordinate acceleration(좌표의 두 번째 미분)과 연결되는지 먼저 확인해야 함을 보여줍니다. Polar coordinates(극좌표)에서는 ΣFᵣ = mr̈라고 줄여 쓰지 않습니다.')
add('그룹 예제 2 · 회전속도 식이 원본에서 누락되어 있습니다','원본 68장 · 해당 예제 영상 해설 없음',
    'Mass(질량) 3 kg의 collar B(칼라 B)가 frictionless arm(마찰 없는 막대) AA′를 따라 움직이고, drum D(드럼 D)가 arm(막대)을 horizontal plane(수평평면)에서 회전시킵니다. 원본 문장은 “at the rate where …”로 이어지지만 그 사이 angular velocity law(각속도 법칙)가 실제 슬라이드에 보이지 않습니다.',
    '확보한 Problem Solving(문제풀이 영상)은 예제 5에서 끝나므로 누락된 식을 복원할 추가 근거도 없습니다. 임의의 ω(t)를 넣어 numeric answer(수치 답)를 만들지 않습니다. 이후 해설은 ω(t) = θ̇(t)를 미지의 주어진 함수로 남긴 일반식입니다.')
add('그룹 예제 2 · 일정한 것은 반지름 방향 속도입니다','원본 69장 · 시험용 보강',
    'Drum mechanism(드럼 기구)이 cord(줄)를 풀어 collar(칼라)가 O에서 outward(바깥쪽)로 constant speed(일정한 속력) 0.5 m/s로 이동하도록 합니다. 여기서 고정된 값은 radial velocity(반지름 방향 속도) ṙ = 0.5 m/s이지 total speed(전체 속력)가 아닙니다.',
    '다음 장의 r(0) = 0을 함께 사용하면 r = 0.5t, r̈ = 0입니다. 그러나 absolute radial acceleration(절대 반지름 가속도)은 aᵣ = −rω²로 0이 아닐 수 있습니다. Rope tension(줄 장력)은 inward(안쪽), arm reaction(막대 반력)은 transverse(횡방향)으로 작용합니다.',eq='r = 0.5t,  ṙ = 0.5 m/s,  r̈ = 0')
add('그룹 예제 2 · 장력과 수평 반력의 크기가 같아지는 조건','원본 70장 · 시험용 보강',
    'Tension(장력)의 크기를 T, arm horizontal reaction(막대 수평반력)의 signed transverse component(부호 있는 횡성분)를 Fθ로 둡니다. Radial equation(반지름방정식)은 −T = m(−rω²), 따라서 T = mrω²입니다. Transverse equation(횡방정식)은 Fθ = m(rω̇ + 2ṙω)입니다.',
    '요구 조건은 T = |Fθ|입니다. m = 3 kg, r = ct, c = 0.5 m/s를 대입하면 공통 mc를 소거하여 tω(t)² = |tω̇(t) + 2ω(t)|를 얻습니다. ω(t)가 누락되어 있으므로 이 식에서 time(시간)의 숫자는 결정할 수 없습니다.',eq='T = mrω²<br>Fθ = m(rω̇ + 2ṙω)<br>tω² = |tω̇ + 2ω|')
add('그룹 예제 2 · 식이 보완되면 이 순서로 마무리합니다','원본 71장 · 시험용 보강',
    'FBD(자유물체도)에서 inward tension(안쪽 장력) T와 transverse arm force(횡방향 막대 힘) Fθ를 구별한 뒤, KD(운동도)에 maᵣ와 maθ를 표시합니다. Kinematics(운동학)로 r, ṙ, r̈를 정하고, 빠진 ω(t)가 제공되면 derivative(도함수) ω̇(t)를 구하여 앞 장의 equality condition(등식 조건)에 대입합니다.',
    'Time(시간) 해가 여러 개면 t ≥ 0, T ≥ 0, contact condition(접촉조건), 문제에서 요구한 시점을 확인합니다. 현재 확인된 원본에는 numeric solution(수치 풀이)을 완성할 정보가 부족합니다. 이 한계는 학습자의 계산 오류가 아니라 source condition(원자료 조건)의 누락입니다.')
add('References(참고문헌)','원본 참고문헌','Beer, Johnston, Cornwell, Self, Sanghi, <em>Vector Mechanics for Engineers: Dynamics</em>, 12th Edition, Chapter 12.',role='References')
assert len(records) == 72, len(records)

summary = ''.join([
    card('1. 운동학에서 구한 가속도를 힘과 연결합니다.',
         'Kinematics(운동학)는 position(위치)·velocity(속도)·acceleration(가속도)을 기술하고, kinetics(운동역학)는 그 운동과 forces(힘)를 연결합니다. 이번 렉처의 중심식은 Σ<b>F</b> = m<b>a</b>입니다. Left-hand side(좌변)는 선택한 물체에 작용하는 external forces(외력)의 vector sum(벡터합), right-hand side(우변)는 mass(질량)와 absolute acceleration(절대가속도)의 곱입니다.',
         '이 형태는 constant mass(일정한 질량)와 inertial reference frame(관성 기준좌표계)을 전제로 합니다. Inertial(관성적인) 기준은 다른 관성계에 대해 accelerating(가속)하거나 rotating(회전)하지 않습니다. At rest(정지)여야 하는 것은 아니며 constant-velocity translation(등속 병진)도 허용됩니다. Moving wedge(움직이는 쐐기)에 대한 relative acceleration(상대가속도)을 그대로 우변에 넣으면 이 조건을 어기게 됩니다.', kind='callout'),
    card('2. 힘은 속도가 아니라 속도의 변화율과 연결됩니다.',
         'Resultant force(합력)가 zero(0)이면 constant-mass particle(일정 질량 입자)의 velocity vector(속도벡터)는 constant(일정)합니다. 이미 움직이던 물체가 저절로 정지한다는 뜻은 아닙니다. 반대로 starts from rest(정지 출발)는 initial velocity(초기속도)만 지정하므로 initial acceleration(초기가속도)은 0이 아닐 수 있습니다.',
         'Linear momentum(선운동량)을 <b>L</b> = m<b>v</b>로 정의하면 Σ<b>F</b> = d<b>L</b>/dt입니다. 따라서 net force(알짜힘)가 0일 때 momentum(운동량)의 magnitude(크기)와 direction(방향)이 모두 보존됩니다. 이 강의의 <b>L</b>은 linear momentum(선운동량) 기호이며 angular momentum(각운동량)이 아닙니다.',
         formula('Σ<b>F</b> = d(m<b>v</b>)/dt = d<b>L</b>/dt')),
    card('3. 먼저 힘의 그림과 가속도의 그림을 분리합니다.',
         'Free-body diagram(자유물체도, FBD)은 body of interest(관심 물체)를 isolate(분리)하고 weight(중량), tension(장력), normal reaction(수직반력), friction(마찰), applied force(작용력)를 그린 그림입니다. 제거한 support(지지물)의 효과를 reaction force(반력)로 replace(대체)합니다. System boundary(계의 경계)를 정해야 internal force(내력)와 external force(외력)가 구별됩니다.',
         'Kinetic diagram(운동도, KD)은 같은 물체의 m<b>a</b> 또는 그 component(성분)를 표시합니다. FBD(자유물체도)에 실제 힘과 m<b>a</b>를 함께 추가하지 않습니다. Unknown direction(미지의 방향)은 positive axis(양의 축)로 가정하고 negative result(음수 결과)가 나오면 방향을 수정합니다. Action-reaction pair(작용·반작용 쌍)는 서로 다른 물체에 작용하며, 두 물체를 하나로 묶었을 때만 internal(내부) 쌍으로 상쇄됩니다.'),
    card('4. 좌표계가 달라도 같은 뉴턴 법칙입니다.',
         'Rectangular coordinates(직교좌표)는 fixed axes(고정축)마다 ΣFₓ = maₓ, ΣFᵧ = maᵧ로 씁니다. Path coordinates(경로좌표)는 tangent(접선)과 inward normal(안쪽 법선)에 따라 ΣFₜ = m dv/dt, ΣFₙ = mv²/ρ로 씁니다. Polar coordinates(극좌표)는 outward radial(바깥쪽 반지름)과 increasing-angle transverse(각도 증가 횡방향)에 따라 아래 식을 사용합니다.',
         'Speed change(속력 변화)와 path curvature(경로 곡률)가 주어지면 path coordinates(경로좌표), 회전각과 막대 길이가 주어지면 polar coordinates(극좌표)가 편리합니다. Contact normal force(접촉 수직항력)는 면에 수직인 실제 힘이고 path-normal resultant(경로 법선 합력)은 곡률중심 쪽의 성분 합입니다. Centripetal force(구심력)를 새 힘으로 더하지 않습니다.',
         formula('ΣFᵣ = m(r̈ − rθ̇²)<br>ΣFθ = m(rθ̈ + 2ṙθ̇)')),
    card('5. 수직항력과 마찰은 문제의 조건으로 구합니다.',
         'SI units(SI 단위계)에서 1 N = 1 kg·m/s²이며 weight(중량)는 W = mg입니다. Normal force(수직항력) N은 항상 mg가 아닙니다. 예제 1에서 downward push(아래로 누르는 힘) P가 있으므로 N = mg + P sin30°입니다. Kinetic friction(운동마찰)은 Fₖ = μₖN이고, 이를 수평식 P cos30° − μₖN = maₓ에 넣으면 P ≈ 535 N입니다.',
         'Static friction(정지마찰)은 |Fₛ| ≤ μₛN이며 impending sliding(미끄러지기 직전)에만 한계값 μₛN입니다. 마찰 방향은 접촉면에서의 relative sliding(상대 미끄럼) 또는 그 경향에 반대입니다. Rotating arm(회전 막대)의 θ increasing(θ 증가)만으로 inward/outward sliding(안쪽/바깥쪽 미끄럼)을 결정할 수 없습니다. 이 방향은 따로 확인해야 합니다.'),
    card('6. 도르래는 줄 길이와 힘의 개수를 동시에 셉니다.',
         '예제 2는 +xₐ rightward(오른쪽), +yᵦ downward(아래쪽)에서 −xₐ + 2yᵦ = C이므로 aₐ = 2aᵦ입니다. A의 식은 T₁ = mₐaₐ, B의 식은 mᵦg − T₂ = mᵦaᵦ, massless pulley(질량 없는 도르래)의 식은 T₂ = 2T₁입니다. 이 네 식으로 aₐ ≈ 8.40 m/s², aᵦ ≈ 4.20 m/s², T₁ ≈ 840 N, T₂ ≈ 1680 N을 얻습니다.',
         'Same ideal cable(같은 이상 케이블)의 tension(장력)은 같지만 다른 연결부 T₂까지 T₁과 같지는 않습니다. Massless(질량 없음)는 zero acceleration(가속도 0)이 아니라 zero inertial term(관성항 0)을 뜻합니다. B와 움직도르래를 하나로 묶으면 T₂는 internal force(내력)가 되어 식에서 사라집니다. 그룹 예제 1은 줄 끝도 B에 부착되어 aₐ = 3aᵦ, B의 upward force(위쪽 힘)는 3T입니다.'),
    card('7. 움직이는 경사면에서는 상대가속도와 절대가속도를 구분합니다.',
         '예제 3의 15 kg wedge(쐐기)는 수평 오른쪽으로 움직이고, 6 kg block(블록)은 쐐기의 30° 경사면을 따라 아래로 slide(미끄러짐)합니다. <b>a</b>ᵦ = <b>a</b>ₐ + <b>a</b>ᵦ/ₐ에서 relative acceleration(상대가속도)만 경사면 아래 방향입니다. B의 absolute acceleration(절대가속도)은 두 벡터의 합입니다.',
         '쐐기 식 N₁ sin30° = mₐaₐ와 B의 경사면 수직식 N₁ − mᵦg cos30° = −mᵦaₐ sin30°를 연립하면 aₐ ≈ 1.545 m/s² rightward(오른쪽)입니다. B의 경사면 방향식은 aᵦ/ₐ = aₐ cos30° + g sin30°이므로 상대가속도는 약 6.24 m/s² down the incline(경사면 아래쪽)입니다. 면에 대해 수직 상대가속도가 0이어도 절대가속도의 그 성분은 0이 아닙니다.'),
    card('8. 뱅크각이 기울어진 반력을 구심 방향으로 분해합니다.',
         'Banked curve(경사진 곡선도로)의 rated speed(설계속도)는 no lateral friction(횡마찰 없음) 조건의 속력입니다. Vertical balance(수직 평형)는 R cosθ = mg, inward equation(안쪽 방정식)은 R sinθ = mv²/ρ입니다. 둘을 나누면 tanθ = v²/(gρ), 따라서 v = √(gρ tanθ)입니다.',
         'ρ = 120 m, θ = 18°이면 v ≈ 19.56 m/s = 70.4 km/h입니다. Mass(질량)는 소거됩니다. 같은 ρ에서 bank angle(뱅크각)이 크면 rated speed(설계속도)가 커집니다. 이 값은 이상 모델의 횡마찰 없는 조건이지 모든 실제 상황의 maximum safe speed(최대 안전속도)는 아닙니다.'),
    card('9. 반지름 방향 힘이 없어도 칼라는 막대를 따라 빨라질 수 있습니다.',
         '예제 5의 frictionless arm(마찰 없는 막대)은 horizontal plane(수평평면)에서 constant angular velocity(일정한 각속도) ω로 회전합니다. Radial force(반지름 방향 힘)가 0이므로 r̈ − rω² = 0입니다. 따라서 aᵣ = 0이지만 rod-relative acceleration(막대 상대가속도) r̈ = rω²는 남습니다.',
         'As a function of r(r의 함수로)라는 요구에 맞춰 r̈ = vᵣ dvᵣ/dr를 사용합니다. Initial radial velocity(초기 반지름 속도) vᵣ(r₀)=0으로 적분하면 vᵣ² = ω²(r² − r₀²)입니다. Outward motion(바깥쪽 운동)에서 vᵣ = |ω|√(r² − r₀²)이고, arm force magnitude(막대 힘의 크기)는 |Fθ| = 2mω²√(r² − r₀²)입니다. Constant angular velocity(일정한 각속도)여도 2ṙω가 있으므로 횡방향 힘이 필요합니다.'),
    card('전체 풀이 흐름',
         '먼저 determine(구하라)의 대상이 force(힘)인지 acceleration(가속도)인지, absolute(절대)인지 relative(상대)인지 읽습니다. 다음으로 system boundary(계의 경계)와 axes(좌표축)를 정하고 FBD(자유물체도)·KD(운동도)를 분리합니다. Cable length(줄 길이), contact(접촉), constant angular velocity(일정 각속도) 등의 constraint(구속조건)를 식으로 바꿉니다.',
         '그 뒤 각 축의 ΣF = ma와 constraint equations(구속방정식)을 함께 풀고, 필요하면 initial conditions(초기조건)를 써서 integrate(적분)합니다. 마지막에는 force direction(힘 방향), unit(단위), friction assumption(마찰 가정), relative/absolute distinction(상대·절대 구분)을 확인합니다. 원본 68–71장의 마지막 그룹 문제는 ω(t)가 누락되어 일반식까지만 결정됩니다. 모르는 조건을 임의 숫자로 채우지 않습니다.',kind='exam-card'),
    '<div class="evidence"><span>슬라이드 05–71 종합</span><span>Contents 1·2 및 Problem Solving</span><span>Summary 00:17–00:44</span></div>',
])

exam_items = [
    ('State Newton’s second law(뉴턴 제2법칙) and its assumptions(가정).',
     'For a constant-mass particle, the resultant external force equals the mass times the absolute acceleration: ΣF = ma. The acceleration must be measured with respect to an inertial reference frame.',
     'Constant mass(일정한 질량), resultant external force(외력의 합력), absolute acceleration(절대가속도), inertial frame(관성계)을 포함합니다.'),
    ('Distinguish a free-body diagram(자유물체도) from a kinetic diagram(운동도).',
     'A free-body diagram shows the external forces acting on an isolated body. A kinetic diagram shows its mass times acceleration. The ma term is not an additional applied force on the free-body diagram.',
     'External forces(외력)는 FBD(자유물체도), inertial terms(관성항)는 KD(운동도)에 둡니다. 같은 효과를 double-count(중복 계산)하지 않습니다.'),
    ('When is linear momentum(선운동량) conserved(보존되는가)?',
     'The linear momentum of a particle is conserved when the resultant force is zero. Both its magnitude and direction remain constant because d(mv)/dt = 0.',
     'Magnitude(크기)와 direction(방향)을 모두 말해야 합니다. Constant speed(일정한 속력)만으로는 충분하지 않습니다.'),
    ('Determine the pushing force(미는 힘) in Sample Problem 1.',
     'Taking rightward as positive x and upward as positive y, P cos30° − μ_k N = ma and N − P sin30° − mg = 0. Eliminating N gives P = m(a + μ_k g)/(cos30° − μ_k sin30°) ≈ 535 N, using the kinetic-friction model.',
     'Downward component(아래쪽 성분)가 normal force(수직항력)를 증가시키므로 N = mg로 두지 않습니다. Kinetic-friction model(운동마찰 모델)의 답이라는 조건을 명시합니다.'),
    ('Does a massless pulley(질량 없는 도르래) have zero acceleration(가속도 0)?',
     'No. A massless pulley may accelerate, but its inertial term is zero in the ideal model. In Sample Problem 2, the force balance on the pulley gives T_2 = 2T_1.',
     'Massless(질량 없음)와 stationary(정지해 있음)는 다릅니다. Zero inertial term(관성항 0)이 force balance(힘의 평형)를 줍니다.'),
    ('Explain the dependent motion(종속운동) in Sample Problem 2.',
     'With x_A positive to the right and y_B positive downward, the constant cable length gives −x_A + 2y_B = C. Differentiating twice yields a_A = 2a_B. This relation must be combined with the equations of motion.',
     'Positive directions(양의 방향), constant cable length(일정 줄 길이), differentiation twice(두 번 미분)를 순서대로 씁니다.'),
    ('Why is the acceleration of B not necessarily down the incline(경사면 아래쪽인가)?',
     'Only the acceleration relative to the nonrotating wedge is constrained to the incline. The absolute acceleration is a_B = a_A + a_B/A. The horizontal acceleration of the wedge must also be included in the kinetic diagram.',
     'Relative acceleration(상대가속도)과 absolute acceleration(절대가속도)의 차이를 설명합니다. Nonrotating wedge(회전하지 않는 쐐기)라는 조건도 중요합니다.'),
    ('Derive the rated speed(설계속도) of a banked curve(경사진 곡선도로).',
     'With no lateral friction, R cosθ = mg and R sinθ = mv²/ρ. Dividing gives tanθ = v²/(gρ), so v = √(gρ tanθ). For ρ = 120 m and θ = 18°, v ≈ 19.56 m/s or 70.4 km/h.',
     'No lateral friction(횡마찰 없음)을 전제로 vertical balance(수직 평형)와 inward acceleration(안쪽 가속도)을 연결합니다.'),
    ('Is centripetal force(구심력) an additional force(추가 힘)?',
     'No. It is the inward resultant of the actual forces. The normal component of Newton’s law is ΣF_n = mv²/ρ, so an extra mv²/ρ force must not be added to the free-body diagram.',
     'Inward resultant(안쪽 합력)의 역할을 별개의 applied force(작용력)로 추가하지 않습니다.'),
    ('Find radial velocity(반지름 속도) as a function of r(r의 함수로) in Sample Problem 5.',
     'The radial equation gives r̈ = rω². Using r̈ = v_r dv_r/dr and v_r(r_0) = 0, integration gives v_r² = ω²(r² − r_0²). For outward motion, v_r = |ω|√(r² − r_0²).',
     'Chain rule(연쇄법칙), initial radial velocity(초기 반지름 속도), outward branch(바깥쪽 해)를 포함합니다.'),
    ('Can radial acceleration(반지름 가속도) be zero while the collar speeds up relative to the rod(막대에 대해 빨라지는가)?',
     'Yes. The radial component of absolute acceleration is a_r = r̈ − rω². Thus a_r = 0 implies r̈ = rω², not r̈ = 0. The acceleration relative to the rotating rod may be nonzero.',
     'Absolute radial component(절대 반지름 성분)와 rod-relative acceleration(막대 상대가속도)은 서로 다른 양입니다.'),
    ('What information is missing(누락된 정보) in the final group problem?',
     'The angular velocity as a function of time is missing. Using r = ct, the condition T = |F_θ| reduces to tω² = |tω̇ + 2ω|. A numerical time cannot be determined without ω(t).',
     'Missing condition(누락 조건)을 밝히고 가능한 governing equation(지배방정식)까지만 제시합니다. 주어지지 않은 angular velocity law(각속도 법칙)를 추정하지 않습니다.'),
]

terms = [
    ('kinetics','운동역학','힘과 운동을 연결하는 해석'),('resultant / net force','합력 / 알짜힘','실제 작용하는 힘들의 벡터합'),
    ('inertial reference frame','관성 기준좌표계','다른 관성계에 대해 가속하거나 회전하지 않는 기준'),('constant mass','일정한 질량','시간에 따라 m이 변하지 않는 가정'),
    ('linear momentum','선운동량','m<b>v</b>; 이번 원본의 기호는 <b>L</b>'),('conserved','보존되는','시간에 따라 해당 양이 변하지 않는'),
    ('free-body diagram / FBD','자유물체도','분리한 물체에 작용하는 외력을 표시'),('kinetic diagram / KD','운동도','질량×절대가속도 항을 표시'),
    ('isolate','분리하라','관심 물체를 주변에서 개념적으로 떼어냄'),('system boundary','계의 경계','해석에 포함하는 물체의 범위'),
    ('external / internal force','외력 / 내력','계 밖에서 작용 / 계 안 구성원 사이에 작용'),('normal reaction','수직반력','접촉면에 수직인 힘'),
    ('weight / mass','중량 / 질량','W=mg인 힘 / 관성의 척도; SI 단위는 N / kg'),('tension','장력','줄 방향으로 당기는 힘'),
    ('static friction','정지마찰','미끄러지지 않는 접촉에서 한계값 이내로 조절되는 마찰'),('kinetic friction','운동마찰','미끄러질 때 상대 운동을 방해하는 마찰'),
    ('impending motion','임박 운동','막 움직이기 시작하려는 한계 상태'),('coefficient of friction','마찰계수','마찰과 수직항력을 연결하는 무차원 계수'),
    ('frictionless / smooth','마찰 없는 / 매끈한','해당 접촉에서 마찰력을 무시하는 조건'),('massless / negligible mass','질량 없는 / 무시 가능한 질량','모델에서 관성항을 생략하는 조건'),
    ('inextensible / constant length','늘어나지 않는 / 일정한 길이','줄 길이 구속조건을 만드는 가정'),('movable pulley','움직도르래','중심이 함께 이동하는 도르래'),
    ('dependent motion','종속운동','기하학적 구속으로 서로 연결된 운동'),('absolute / relative acceleration','절대 / 상대가속도','관성계 기준 / 다른 물체 기준의 가속도'),
    ('down the incline','경사면 아래쪽','이동 또는 상대가속도 방향을 지정'),('rightward / downward','오른쪽 / 아래쪽','성분식의 방향과 부호를 지정'),
    ('tangential / normal','접선 방향의 / 법선 방향의','경로의 진행 방향 / 곡률중심 방향'),('radial / transverse','반지름 방향의 / 횡방향의','원점에서 바깥 방향 / 각도 증가 방향'),
    ('centripetal','구심의','곡률중심을 향하는'),('banked curve / bank angle','경사진 곡선도로 / 뱅크각','노면의 기울기와 관련된 표현'),
    ('rated speed','설계속도','이 예제에서 횡마찰 없이 선회하는 속력'),('no lateral friction','횡마찰 없음','도로를 가로지르는 방향의 마찰이 0인 조건'),
    ('constant angular velocity','일정한 각속도','θ̇=ω가 일정하고 θ̈=0인 조건'),('released from rest relative to the arm','막대에 대해 정지 상태에서 놓임','초기 ṙ=0; 절대속도 0과 다름'),
    ('as a function of','…의 함수로','답의 독립변수를 지정'),('resolve into components','성분으로 분해하라','축별 투영과 부호를 구하라는 지시'),
    ('determine / substitute / integrate','구하라 / 대입하라 / 적분하라','문제와 풀이에서 반복되는 지시 표현'),('magnitude','크기','부호 없는 벡터의 길이; 성분과 구별'),
]

audit = [
    ('Overview 00:35–01:05','yelling / border torque / fiscal stamping','yawing(요 회전) / motor torque(모터 토크) / viscous damping(점성 감쇠)','운동 원인 문맥과 Lecture 1의 동일 용어. 이번 입자 계산의 추가 힘으로 임의 사용하지 않음'),
    ('Contents 1 01:56·03:49·03:51','mess / mirror','mass(질량) / meter(미터)','원본 07·11의 정의와 SI 단위'),
    ('Contents 1 06:28–09:35 및 Summary 00:39','free by / freeway diagram','free-body diagram(자유물체도)','원본 15–19 제목과 정의'),
    ('Contents 1 10:45–10:51','pulleys are also not needed','A에 부착된 도르래를 계에 포함하고 케이블 작용력을 보존','원본 17–19의 명시 조건과 최종 FBD'),
    ('Contents 2 00:28–02:08','on / horn / color','arm(막대) / collar(칼라)','원본 21–23 장치 명칭'),
    ('Contents 2 03:24–03:47','vehicles Vector / rho V squared','velocity vector(속도벡터) / v²/ρ','원본 25의 법선가속도 식'),
    ('Problem Solving 20:09–20:24','radius speed / weighted speed','rated speed(설계속도)','원본 55의 정의'),
    ('Problem Solving 25:25','18.50 second meter per second','19.56 m/s','원본 59와 √(9.81×120×tan18°) 재계산'),
    ('Problem Solving 33:20–33:31','f equals m minus','Fθ = m(rθ̈ + 2ṙθ̇)','원본 64·66 및 극좌표 가속도 식'),
    ('원본 12','U.S. customary length(m), lb 혼용','ft, 힘 lbf와 질량 lbm을 구별','같은 슬라이드의 ft/s²와 slug 식'),
    ('원본 14','ΣFₓ = mÿ','ΣFᵧ = mÿ','동일 슬라이드 위 줄의 y성분 방정식'),
    ('원본 21–23','θ 증가 조건과 안쪽 마찰 화살표','마찰 방향은 바깥쪽 상대 미끄럼 가정임을 명시','θ̇의 부호는 ṙ의 부호를 결정하지 않음; 편집자 조건 검토'),
    ('원본 26','Normal and Tangential Coordinates 제목','본문을 반지름·횡좌표 적용 사례로 해설','같은 장 본문 및 다음 장 27'),
    ('원본 34','정지마찰 F = μₛN','최대정지마찰의 한계식으로 한정','정지마찰과 운동마찰 조건 구분; 편집자 보강'),
    ('원본 42','T₂ − 2T₁ = 1680 N','T₂ = 2T₁ = 1680 N','원본 40의 T₂ − 2T₁ = 0과 수치'),
    ('원본 68–71','각속도 법칙 누락','ω(t)를 미지 함수로 유지하고 수치 시각은 미결정','전체 원본 시각 검토; 확보한 문제풀이 영상은 67장 예제에서 종료'),
]

def table(headers, rows):
    return '<table class="term-table"><thead><tr>' + ''.join('<th>'+x+'</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows) + '</tbody></table>'

template = (SITE / 'templates/lecture-page.template.html').read_text(encoding='utf-8')
source_pattern = r'<section class="source-section"[\s\S]*?</section>'
source_template = re.search(source_pattern, template).group()
sections = []
for n,(title,evidence,blocks,role) in enumerate(records,1):
    section = source_template
    values = {'NN':f'{n:02d}','SLIDE_ROLE':role,'SLIDE_HEADING':title,'LECTURE_SLUG':'lecture04','DESCRIPTIVE_ALT_TEXT':f'Lecture 4 원본 슬라이드 {n:02d}: {escape(title)}','CURRENT_PAGE':str(n),'PAGE_COUNT':'72','TRANSCRIPT_TIME_OR_SLIDE_ROLE':evidence,'SLIDE_EXPLANATION_BLOCKS':blocks}
    for key,value in values.items():
        section = section.replace('{{'+key+'}}',value)
    sections.append(section)
template = re.sub(source_pattern,lambda _: '\n\n'.join(sections),template,count=1)
exam_html = ''.join('<div class="exam-card"><h3>'+q+'</h3><div class="answer"><span class="answer__label">Model answer</span>'+a+'</div><p style="margin-top: 12px">'+ko+'</p></div>' for q,a,ko in exam_items)
template = re.sub(r'<div class="exam-card">\s*<h3>\{\{EXAM_QUESTION\}\}</h3>[\s\S]*?</div>\s*</div>',lambda _: exam_html+'\n          </div>',template,count=1)
videos = [('Overview','P3v32piVDzs'),('Contents 1','EaxqQg-9DyY'),('Contents 2','uB88GSmUx0Y'),('Problem Solving','GwPQhYgqnKo'),('Summary','ryIk9g0SVyg')]
toc = [('overview','전체 개요'),('concept-map','개념 지도'),('concept-summary','핵심 개념 요약')] + [(f'slide-{i:02d}',f'{i:02d} · {row[0]}') for i,row in enumerate(records,1)] + [('exam-english','시험 영어'),('glossary','용어집'),('asr-log','원본·스크립트 교정'),('sources','출처')]
values = {
    'LECTURE_NUMBER':'Lecture 4','LECTURE_TITLE':'Kinetics of Particles',
    'ONE_SENTENCE_DESCRIPTION':'3주차 입자의 운동역학: 원본 72장과 영어 영상 5개를 종합한 한국어 수업 대체 노트',
    'WEEK':'Week 03','DATE_OR_날짜_미기재':'2026-09-16','PAGE_COUNT':'72',
    'LECTURE_PROMISE':'Newton’s second law(뉴턴 제2법칙)로 force(힘)와 acceleration(가속도)을 연결하고, free-body diagram(자유물체도)에서 실제 문제의 풀이까지 이어갑니다.',
    'VIDEO_SET':'Overview · Contents 1·2 · Problem Solving · Summary',
    'ALL_CONTENTS_AND_PROBLEM_SOLVING_BUTTONS':'\n'.join(f'<a class="button button--primary" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상 열기</a>' for label,vid in videos[1:4]),
    'ORIGINAL_PDF_URL':'https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/lecture04_note.pdf',
    'LECTURE_NOTE_FILENAME':'lecture04_note.pdf',
    'CORE_RELATIONSHIP_HEADLINE':'힘을 분리하고, 가속도를 연결하고, 함께 풉니다.',
    'CORE_RELATIONSHIP_EXPLANATION':'Kinetics(운동역학)는 kinematics(운동학)에서 기술한 motion(운동)을 force(힘)와 연결합니다. 같은 Newton’s law(뉴턴 법칙)를 직교·경로·극좌표로 표현하고, constraint(구속조건)와 함께 풀어 실제 가속도와 반력을 구합니다.',
    'CONCEPT_MAP_HEADLINE':'외력의 그림과 운동의 조건을 하나의 방정식으로 연결합니다.',
    'CONCEPT_MAP_BLOCKS':'<div class="grid-3">'+card('Forces(힘)','관심 물체를 분리하고 weight(중량), tension(장력), normal force(수직항력), friction(마찰)을 FBD(자유물체도)에 표시합니다.')+card('Motion(운동)','KD(운동도)에 absolute acceleration(절대가속도)을 표현하고 cable length(줄 길이)와 relative motion(상대운동)의 조건을 정합니다.')+card('Equations(방정식)','각 축에서 ΣF = ma를 쓰고 constraint equations(구속방정식)을 연립합니다. 필요한 경우 initial conditions(초기조건)로 적분합니다.')+'</div>',
    'STANDALONE_CONCEPT_SUMMARY':summary,'DISTINCT_SUMMARY_VIDEO_SECTION_IF_NEEDED':'',
    'EXAM_SECTION_TITLE':'힘과 운동의 관계를 설명하는 영어 답안',
    'BILINGUAL_GLOSSARY_TABLE':table(['영어(한국어)','의미와 사용'],[(f'{en}({ko})',meaning) for en,ko,meaning in terms]),
    'AUDIT_SECTION_TITLE':'원본 슬라이드·자동생성 스크립트 교정 기록',
    'ASR_CORRECTION_TABLE':p('영어 자동생성 스크립트와 원본 슬라이드는 그대로 보존했습니다. 아래는 본문에서 채택한 해석과 교정 근거입니다. 음성을 별도로 재판독하지 않은 항목은 실제 발화 오류인지 자동인식 오류인지 단정하지 않습니다.')+table(['위치','원문 또는 문제','본문 처리','근거'],audit),
    'SOURCE_LIST_AND_PROVENANCE_NOTE':'<ul class="plain-list"><li>원본 PDF: Lecture 4, MC2103, Fall 2026, 72장.</li>'+''.join(f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상</a> · 영어 자동생성 스크립트, 2026-09-11 확보.</li>' for label,vid in videos)+'<li>주차·날짜: Teams에서 보존한 강의 인덱스의 Week 03 · 2026-09-16.</li></ul>'+p('Summary 00:17–00:44는 Newton’s law(뉴턴 법칙), FBD(자유물체도), KD(운동도)의 실제 복습으로 핵심 개념 요약에 반영했습니다. 00:47–00:58의 central-force motion(중심력 운동)과 위성 예고는 다음 단원 안내이며 현재 개념 요약과 구분합니다.')+p('문제풀이 영상은 원본 67장 예제까지 설명합니다. 53–54장 그룹 예제의 수치 풀이는 원본 조건으로 계산한 시험용 보강이고, 68–71장 그룹 예제는 각속도 식이 없어 일반식만 제시했습니다. 타임스탬프는 관련 설명 구간이며 영상의 정확한 슬라이드 전환 시각을 뜻하지 않습니다.')+p('계산은 g = 9.81 m/s²를 사용하며 원본의 중간 반올림 결과와 마지막 자리가 다를 수 있습니다. 원본 밖의 조건 검토·추가 계산은 시험용 보강 또는 편집자 보강으로 구분합니다.'),
    'TABLE_OF_CONTENTS_LINKS':''.join(f'<li><a href="#{id}">{label}</a></li>' for id,label in toc),
}
for key,value in values.items():
    template = template.replace('{{'+key+'}}',value)
template = template.replace('이 부분만 읽어도 렉처의 핵심 정의, 개념 관계, 가정과 풀이 흐름을 이해할 수 있도록 작성합니다.','원본 슬라이드와 본강의·문제풀이·Summary의 개념 설명을 종합했습니다. 뉴턴 법칙의 전제부터 힘의 그림, 구속조건, 주요 예제의 풀이를 한 흐름으로 읽을 수 있습니다.')
template = re.sub(r'\s*<!--[\s\S]*?-->','',template)
template = '\n'.join(line.rstrip() for line in template.splitlines())+'\n'
assert not re.search(r'\{\{[^}]+\}\}',template)
(SITE/'lecture04.html').write_text(template,encoding='utf-8')
print(f'BUILT lecture04.html: {len(records)} source sections, {len(exam_items)} exam cards, {len(terms)} terms')
