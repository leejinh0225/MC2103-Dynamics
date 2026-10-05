"""Lecture 7: fill the fixed Lecture 1 template with source-reviewed explanations."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
records = []

def p(s):
    return s if s.startswith('<table') else '<p>'+s+'</p>'

def card(title, *body, kind='card'):
    return f'<div class="{kind}"><h3>{title}</h3>'+''.join(p(s) for s in body)+'</div>'

def table(head, rows):
    return '<table class="term-table"><thead><tr>'+''.join('<th>'+s+'</th>' for s in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+s+'</td>' for s in row)+'</tr>' for row in rows)+'</tbody></table>'

def add(n, title, evidence, *body, eq='', extra='', correction='', role='Concept'):
    assert n == len(records)+1, n
    blocks = card('원본 교정 · 적용 조건',correction,kind='callout') if correction else ''
    blocks += card('핵심 해설' if role=='Concept' else '슬라이드 안내',*body,kind='card' if role=='Concept' else 'quiet-card')
    if eq:
        blocks += card('식과 기호','<span class="formula">'+eq+'</span>')
    records.append((title,evidence,blocks+extra,role))

summary = ''.join([
    card('1. 충격량은 힘의 시간 적분이며 운동량을 변화시킵니다.',
        'Linear momentum(선운동량)은 <b>p</b>=m<b>v</b>, impulse(충격량)는 <b>J</b>=∫Σ<b>F</b>dt입니다. Newton’s second law(뉴턴 제2법칙)를 시간에 대해 적분하면 m<b>v</b>₁+<b>J</b>=m<b>v</b>₂가 됩니다. J는 원본의 Imp를 짧게 쓴 편집 표기이며, 여기서는 constant mass(일정 질량)의 particle(입자)와 inertial frame(관성 기준계)을 사용합니다.',
        'Momentum(운동량)과 impulse(충격량)는 모두 vector(벡터)입니다. 속력 두 개를 빼는 것이 아니라 velocity components(속도 성분들)를 같은 좌표축에서 빼야 합니다. 단위는 kg·m/s=N·s입니다. Work(일)의 단위 N·m와 다릅니다. Work–energy(일·에너지)는 힘을 displacement(변위)에 대해, impulse–momentum(충격량·운동량)은 time(시간)에 대해 적분한 관계입니다.',kind='callout'),
    card('2. 짧은 충돌뿐 아니라 긴 제동에도 같은 원리가 적용됩니다.',
        'Impulse(충격량)는 모든 시간 구간에 정의됩니다. Impulsive force(충격력)는 매우 짧은 contact time(접촉 시간)에 유의미한 momentum change(운동량 변화)를 만드는 큰 힘입니다. 일정한 force(힘)는 J=FΔt이고, 변하는 힘도 average force(평균 힘) Favg=J/Δt를 쓰면 같은 형태로 표현됩니다. Favg는 peak force(최대 힘)가 아닙니다.',
        'Nonimpulsive force(비충격력)를 neglect(무시)하는 기준은 힘이 존재하지 않는다는 뜻이 아니라 그 impulse(충격량)가 비교 대상보다 충분히 작은가입니다. 야구공 예제에서 중량의 충격량은 0.01766 N·s, 타격의 충격량은 약 6.784 N·s라서 약 0.26%입니다. 반면 9초가량 걸리는 자동차 제동에서는 mg sin5°의 충격량을 생략할 수 없습니다.'),
    card('3. 운동량 보존은 계와 방향을 지정해야 의미가 있습니다.',
        'System(계)을 여러 입자로 잡으면 internal impulses(내부 충격량)는 작용·반작용으로 합에서 상쇄됩니다. 따라서 <b>P</b>₂−<b>P</b>₁=<b>J</b>ext이며, external impulse(외부 충격량)가 0 또는 무시할 만큼 작을 때만 total momentum(총운동량)이 conserved(보존)됩니다. 한 입자만 떼어 보면 접촉력은 external force(외력)가 되어 그 입자의 운동량을 바꿉니다.',
        '카트+포장물의 경우 수평 외부 충격량은 거의 0이지만 바퀴를 통한 수직 충격량은 큽니다. 따라서 horizontal momentum(수평 운동량)만 보존됩니다. 줄에 매달린 공도 tension impulse(장력의 충격량)가 외부에서 작용할 수 있습니다. “충돌이므로 모든 방향의 운동량 보존”이라고 쓰지 말고, free-body/impulse diagram(자유물체도/충격량도)을 먼저 그립니다.'),
    card('4. 충돌선과 이동 방향은 서로 다른 분류 기준입니다.',
        'Line of impact(충돌선)는 접촉점의 common normal(공통 법선)입니다. 두 mass centers(질량중심)가 이 선 위에 있으면 central impact(중심충돌), 그렇지 않으면 eccentric impact(편심충돌)입니다. 두 initial velocities(초기 속도)가 충돌선과 나란하면 direct central impact(직선 중심충돌), 다른 방향 성분도 있으면 oblique central impact(경사 중심충돌)입니다.',
        'Smooth contact(매끈한 접촉)에서는 contact impulse(접촉 충격량)가 normal direction(법선 방향) n에만 작용합니다. Tangential direction(접선 방향) t는 접촉면을 따릅니다. 여기서 n,t는 경로의 곡률 좌표가 아니라 충돌 접촉면의 좌표이며, 경사 충돌이라고 편심충돌인 것은 아닙니다.'),
    card('5. 반발계수는 법선 상대속도의 비입니다.',
        'A가 B를 따라잡는 방향을 positive(양)로 정하고 vA&gt;vB라면 coefficient of restitution(반발계수)는 e=(v′B−v′A)/(vA−vB)입니다. 분모는 relative speed of approach(접근 상대속력), 분자는 relative speed of separation(분리 상대속력)입니다. 프라임 ′은 immediately after impact(충돌 직후)를 뜻하며 미분 표시가 아닙니다.',
        'Direct central impact(직선 중심충돌)의 deformation period(변형 단계) 끝에는 두 물체가 순간적으로 common velocity(공통 속도) u를 갖습니다. 일반적인 경사 충돌에서는 먼저 normal relative velocity(법선 상대속도)가 0이라는 뜻입니다. Restitution period(복원 단계)에서 갈라집니다. 원본은 e를 restitution impulse/deformation impulse(복원 충격량/변형 충격량)로 정의하고 u를 소거해 상대속도 식을 얻습니다. e는 접촉 쌍과 충돌 조건의 특성이며 한 물체의 속력비나 에너지비가 아닙니다. 이 강의의 수동적 충돌 모델은 0≤e≤1입니다.'),
    card('6. 운동량 식과 반발계수 식을 함께 풀어야 합니다.',
        'Direct central impact(직선 중심충돌)에서 external impulse(외부 충격량)를 무시하면 mAvA+mBvB=mAv′A+mBv′B입니다. 미지수는 v′A와 v′B 두 개이므로 이 식만으로 부족합니다. v′B−v′A=e(vA−vB)를 함께 풀어야 합니다.',
        '시험용 보강: v′A=[(mA−emB)vA+(1+e)mBvB]/(mA+mB), v′B=[(1+e)mAvA+(mB−emA)vB]/(mA+mB)입니다. e=0이면 common final velocity(공통 최종 속도)로 합쳐지고, e=1이면 kinetic energy(운동에너지)도 보존됩니다. e=1이라는 이유만으로 두 속도를 맞바꾸는 것은 아니며, 그 교환 결과는 equal masses(같은 질량)인 직선 중심충돌에서 성립합니다.'),
    card('7. 탄성 여부와 운동량 보존 여부를 혼동하지 않습니다.',
        'Perfectly plastic impact(완전소성충돌), 즉 perfectly inelastic impact(완전비탄성충돌)에서도 외부 충격량이 없으면 운동량은 보존됩니다. 다만 운동에너지가 변형·열·소리 등으로 전환됩니다. Perfectly elastic impact(완전탄성충돌)는 e=1인 이상적 한계입니다. Energy lost(손실 에너지)는 전체 에너지가 사라진다는 뜻이 아니라 계산에 포함한 kinetic/mechanical energy(운동/역학적 에너지)의 감소입니다.',
        '시험용 보강: 외부 충격량이 없는 직선 중심충돌의 ΔTloss=½[mAmB/(mA+mB)](1−e²)(vA−vB)²입니다. 이는 위 두 속도 식을 운동에너지 차이에 대입한 결과입니다. Initial kinetic energy(초기 운동에너지) 전체에 항상 1−e²를 곱하는 식이 아니며, e=0이어도 mass center(질량중심)의 병진 운동에너지는 남을 수 있습니다.'),
    card('8. 경사 충돌은 접선 성분과 법선 성분을 나누어 풉니다.',
        '두 물체가 free(구속되지 않은) 상태이고 접촉이 smooth(매끈한) 경우 네 미지수 v′At,v′An,v′Bt,v′Bn가 있습니다. 각 물체의 tangential velocity(접선 속도)가 유지되는 두 식, 계 전체의 normal momentum(법선 운동량) 보존식, normal relative velocity(법선 상대속도)의 반발계수 식을 사용합니다.',
        '구속된 블록이나 줄에 매달린 공에는 이 네 식을 그대로 적용하지 않습니다. 지면 반력 또는 줄 장력의 impulsive component(충격 성분)를 먼저 확인합니다. 예제 4에서는 공 A의 접선 성분, 두 공 계의 수평 운동량, 법선 상대속도 관계를 사용합니다. 공 B는 줄이 수직인 충돌 순간에 수평으로만 움직이며, A는 오른쪽 위 16.1° 방향으로 0.721v₀, B는 왼쪽으로 0.693v₀입니다.'),
    card('9. 처음 두 예제는 시간과 벡터 힘을 구하는 기본형입니다.',
        '자동차: m=1800 kg, downhill(내리막) 5°, v₁=100 km/h=27.7778 m/s, braking force(제동력) 7000 N입니다. 내리막 양수에서 mv₁+(mg sin5°−7000)t=0이므로 t≈9.156 s입니다. 중력은 제동을 돕는 것이 아니라 내리막 운동을 돕습니다.',
        '야구공: m=0.120 kg, v₁x=−24 m/s, v₂=(36cos40°,36sin40°) m/s, Δt=0.015 s입니다. 중량 충격량을 무시하면 Favg≈(412.621,185.123) N, 크기 452.246 N입니다. Incoming velocity(들어오는 속도)의 음수를 보존해야 하며, 36−24만으로 속도 변화를 계산하면 안 됩니다.'),
    card('10. 카트 예제는 원본의 24 kg와 25 kg를 분리해 읽습니다.',
        '문제 슬라이드 44와 자막 09:21은 cart mass(카트 질량) 24 kg, 풀이 슬라이드 47·51은 25 kg을 사용합니다. 포장물은 10 kg이고 3 m/s로 수평 아래 30° 방향에서 들어옵니다. 이 노트의 주 계산은 problem statement(문제 조건) 24 kg을 사용하고, 원본 풀이의 25 kg 답은 비교값으로 따로 표시합니다.',
        '24 kg 기준: v′=10·3cos30°/34≈0.76414 m/s 오른쪽, 포장물에 작용한 impulse(충격량)는 약 (−18.339,15.000) N·s, 크기 23.692 N·s입니다. T₁=45 J, T₂≈9.926 J이므로 loss fraction(손실 비율)은 약 77.94%입니다. 25 kg 기준 원본 답은 v′≈0.7423 m/s, loss fraction(손실 비율)≈78.57%이며 서로 섞지 않습니다.'),
    card('11. 낙하·충돌·스프링 압축은 세 구간으로 나눕니다.',
        '30 kg block(블록)이 2 m 낙하하여 10 kg pan(받침)에 완전소성충돌합니다. 낙하 구간에서 energy conservation(에너지 보존)으로 v₂=√(2g·2)≈6.264 m/s, 짧은 충돌 구간에서 외부 충격량을 무시한 momentum conservation(운동량 보존)으로 v₃=(30/40)v₂≈4.698 m/s입니다. 충돌을 통과하면서 운동에너지는 588.6 J에서 441.45 J로 줄어듭니다.',
        'k=20000 N/m인 스프링은 받침 무게 때문에 이미 x₃=10g/k=0.004905 m 압축되어 있습니다. 이후 하강량을 h라 하면 441.45+40gh=½k[(x₃+h)²−x₃²]입니다. 양의 근은 h≈0.22534 m, natural length(자연길이) 기준 총 압축은 x₄≈0.23024 m입니다. 처음부터 마지막까지 한 번에 역학적 에너지 보존을 적용하면 충돌 손실을 놓칩니다.'),
    card('12. 복합 문제에서는 구간·계·축을 식과 함께 적습니다.',
        'Force–acceleration(힘–가속도)은 순간 힘·가속도, work–energy(일·에너지)는 거리·높이·속력, impulse–momentum(충격량·운동량)은 시간·충돌 전후 속도에 맞습니다. 마지막 그룹 문제는 spring release/sliding(스프링 해제/미끄럼) → impact(충돌) → pendulum rise(진자 상승) → tension(장력) 계산의 순서입니다.',
        '시험용 보강: 원본에 최종 답이 없는 그룹 문제는 접촉 법선을 경사면 방향으로 두고 충돌 중 블록의 접촉 구속이 유지되는 이상 모델을 명시하여 풀이합니다. 충돌 직전 A는 약 2.973 m/s, 직후 B는 약 3.636 m/s, α=40°에서 B의 speed(속력)는 약 2.937 m/s, tension(장력)은 약 16.143 N입니다. 핵심은 구속된 B의 속도를 수평으로 두고 법선으로 투영하는 것이며, 일차원 정면충돌 공식을 그대로 쓰지 않는 것입니다.'),
])

add(1,'Lecture 7 · 충격량과 운동량 원리','강의 인덱스 · Week 06 · 2026-10-07',
    'Impulse and Momentum Principle(충격량과 운동량 원리)을 다룹니다. 앞 렉처에서 force(힘)를 displacement(변위)에 대해 적분했다면, 이번에는 time(시간)에 대해 적분하여 velocity change(속도 변화)를 연결합니다.',role='Title')
add(2,'Lecture 7-1 · 도입','Overview 00:20–00:55',
    'Overview(도입 영상)는 공을 때리는 contact time(접촉 시간)과 impact force(충돌력), 여러 pendula(진자들)가 충돌할 때 끝의 공이 움직이는 현상을 질문합니다. 힘의 시간 적분과 충돌 전후 운동을 연결하는 동기입니다. 확보된 자동자막은 첫 질문을 문장 중간부터 담고 있으므로 누락된 앞부분을 임의 복원하지 않았습니다.',role='Divider')
add(3,'원본의 보조 영상 링크','원본 PDF 링크 페이지',
    '원본 링크: <a href="https://youtu.be/pnnJaVTqODs" target="_blank" rel="noreferrer">슬라이드 3 보조 영상 열기</a>. 강의 인덱스의 본강의 5편과 별도입니다. 링크를 보존하며, 이 보조 영상의 내용을 본문 설명 근거로 사용하지 않았습니다.',role='Video link')
add(4,'Lecture 7-2 · 충격량과 운동량의 관계','Contents 1',
    'Impulse(충격량)의 정의, Newton’s second law(뉴턴 제2법칙)에서의 유도, impulsive/nonimpulsive force(충격력/비충격력)의 구별을 설명하는 본강의 구분 페이지입니다.',role='Divider')
add(5,'추력은 시간에 걸쳐 운동을 변화시킵니다.','Contents 1 00:17–00:25',
    'Rocket thrust(로켓 추력)는 일정 시간 동안 작용하여 linear momentum(선운동량)을 변화시킨다는 도입 예시입니다. 작은 force(힘)라도 긴 시간 작용하면 큰 impulse(충격량)를 만들 수 있습니다.',
    '편집자 보강: 실제 로켓은 연료 방출로 mass(질량)가 변하는 open system(열린 계)입니다. 사진을 근거로 로켓 한 물체에 constant-mass(일정 질량) 식 mΔv=∫Fdt를 그대로 쓰지는 않습니다. 뒤의 자동차·공·블록 문제에서는 일정 질량 입자 모델을 사용합니다.')
add(6,'정지시키는 충격량은 초기 운동량과 반대입니다.','Contents 1 00:32–00:44',
    'Railcar(철도 차량)가 벽과 충돌하여 정지하면 final momentum(최종 운동량)은 0입니다. 따라서 net impulse(알짜 충격량)는 −m<b>v</b>₁이고, 초기 운동 방향과 반대입니다.',
    '시험용 보강: 같은 Δp(운동량 변화)를 더 긴 stopping time(정지 시간)에 걸쳐 만들면 average force magnitude(평균 힘 크기)가 줄어듭니다. 이것은 J=FavgΔt의 결과이며 충돌력의 peak(최댓값)나 실제 차량 안전성을 이 식 하나로 확정한다는 뜻은 아닙니다.',eq='<b>J</b>net = 0−m<b>v</b>₁')
add(7,'충격량의 단위는 N·s입니다.','Contents 1 00:52–01:09',
    'Impulse of a force(힘의 충격량)는 force(힘)의 time integral(시간 적분)입니다. 시간에 따라 크기나 방향이 바뀌면 성분별로 적분합니다. Dimensions(차원)는 force×time(힘×시간), SI unit(SI 단위)는 N·s=kg·m/s입니다.',
    '시험용 보강: Force–time graph(힘–시간 그래프)의 signed area(부호 있는 면적)는 그 성분의 충격량입니다. 높이가 Fmax이고 폭이 Δt인 삼각형 펄스의 J는 ½FmaxΔt이며 FmaxΔt가 아닙니다.',eq='<b>J</b>₁→₂ = ∫[t₁→t₂] <b>F</b>(t)dt<br>[J] = N·s = kg·m/s')
add(8,'뉴턴 제2법칙을 시간으로 적분합니다.','Contents 1 01:13–02:28',
    'Net force(알짜 힘) Σ<b>F</b>=d(m<b>v</b>)/dt의 양변에 dt를 곱하여 Σ<b>F</b>dt=d(m<b>v</b>)를 얻습니다. t₁에서 t₂까지 적분하면 우변은 final momentum minus initial momentum(최종 운동량−초기 운동량)입니다.',
    '이렇게 얻은 impulse–momentum principle(충격량·운동량 원리)은 새로운 독립 법칙이 아니라 Newton’s second law(뉴턴 제2법칙)의 적분형입니다. 여러 힘이 있으면 모든 힘의 impulse(충격량)를 vectorially(벡터적으로) 더합니다. 원본의 F는 합력으로 읽습니다.',eq='∫Σ<b>F</b>dt = m<b>v</b>₂−m<b>v</b>₁<br>m<b>v</b>₁+Σ<b>J</b> = m<b>v</b>₂')
add(9,'초기 운동량과 충격량은 벡터로 더합니다.','Contents 1 02:31–02:48',
    '원본 화살표 그림은 initial momentum(초기 운동량)에 impulse(충격량)를 더해 final momentum(최종 운동량)을 얻는 vector addition(벡터 덧셈)을 보여 줍니다. 서로 다른 방향의 크기를 단순히 더하는 그림이 아닙니다.',
    'Plane motion(평면운동)에서는 x와 y 각각에 mv₁x+Jx=mv₂x, mv₁y+Jy=mv₂y를 씁니다. Positive direction(양의 방향)을 먼저 정하고 incoming(들어오는) 속도와 outgoing(나가는) 속도에 부호를 붙이면 방향 반전을 자연스럽게 처리할 수 있습니다.',eq='mv₁x+∫ΣFxdt=mv₂x<br>mv₁y+∫ΣFydt=mv₂y')
add(10,'충격력은 짧은 시간에 유의미한 운동량 변화를 만듭니다.','Contents 1 02:55–03:28',
    'Impulsive force(충격력)는 short time interval(짧은 시간 구간)에 충분히 크게 작용하여 significant momentum change(유의미한 운동량 변화)를 만드는 힘입니다. 타자가 공의 진행 방향을 바꾸는 경우가 대표적입니다.',
    'Impulse(충격량)라는 적분량 자체가 반드시 짧은 충돌에만 쓰이는 것은 아닙니다. 영상도 이 차이를 먼저 설명합니다. 힘의 크기만 보지 말고 ∫Fdt의 크기와 분석 구간을 함께 봅니다.')
add(11,'변하는 충격력에는 평균 힘을 사용합니다.','Contents 1 03:33–04:27',
    '원본은 짧은 충돌 동안 m<b>v</b>₁+Σ<b>F</b>Δt=m<b>v</b>₂로 씁니다. 실제 contact force(접촉력)는 급격히 변하므로 여기의 <b>F</b>는 constant force(일정한 힘) 또는 average force(평균 힘)로 읽어야 합니다.',
    'Nonimpulsive forces(비충격력들)의 작은 충격량을 생략한 근사식입니다. Short interval(짧은 구간)이라는 이유만으로 모든 외력을 버리는 것은 아닙니다. 구속을 유지하는 normal force(수직항력)나 tension(장력)도 충격력을 가질 수 있습니다.',eq='<b>F</b>avg = (1/Δt)∫<b>F</b>dt<br>m<b>v</b>₁+Σ<b>F</b>avgΔt ≈ m<b>v</b>₂',
    extra=card('시험용 보강 · 평균값과 최댓값','동일한 impulse(충격량)를 만드는 force–time pulse(힘–시간 펄스)는 여러 모양일 수 있습니다. 운동량 변화와 접촉 시간만으로 평균값은 정해져도 peak force(최대 힘)는 정해지지 않습니다.'))
add(12,'무시하는 것은 중량이 아니라 중량의 충격량입니다.','Contents 1 04:35–05:15',
    'Bat(야구방망이)의 큰 contact force(접촉력)는 짧은 시간에도 공의 방향을 뒤집습니다. 반면 weight(중량)의 impulse(충격량) mgΔt는 같은 구간에서 작아 nonimpulsive(비충격적)로 취급할 수 있습니다.',
    '이 근사는 타격의 아주 짧은 시간 구간에만 해당합니다. 공이 날아가는 flight(비행) 구간에서는 중력을 버릴 수 없습니다. 예제 2에서 실제 수치로 비교합니다.')
add(13,'Lecture 7-3 · 충돌과 반발계수','Contents 2',
    'Direct/oblique central impact(직선/경사 중심충돌), coefficient of restitution(반발계수), 구속된 물체의 충돌과 여러 원리의 결합을 다루는 구분 페이지입니다.',role='Divider')
add(14,'반발계수는 접촉 쌍의 튀어 오르는 성질을 나타냅니다.','Contents 2 00:19–00:43',
    'Golf(골프) 사진은 coefficient of restitution(반발계수, COR)을 도입하는 예시입니다. 같은 입사 조건에서도 접촉 재료·구조와 충돌 조건에 따라 분리 속도가 달라집니다. e는 그 결과를 상대속도 관계로 나타내는 무차원 수입니다.',
    '편집자 보강: e를 한 물체의 고정된 고유값이나 에너지 전달 비율 자체로 읽지 않습니다. 앞으로의 시험 문제에서는 주어진 e와 적용 방향을 사용합니다.',
    correction='원본은 “golf balls … 0.83”을 규정으로 제시하지만 이를 골프공의 보편적 현행 규정으로 외우지 않습니다. <a href="https://www.usga.org/content/usga/home-page/articles/2025/05/what-happens-collision-between-club-ball.html" target="_blank" rel="noreferrer">USGA의 2025년 공식 설명</a>은 golf club(골프 클럽)의 COR와 clubface(클럽 페이스) 검사로 설명합니다. 이 노트에서는 원본 예시와 규정 적용 대상을 구별하며 해당 숫자를 역학 법칙으로 사용하지 않습니다.')
add(15,'충돌은 짧은 시간에 큰 상호작용력이 작용하는 사건입니다.','Contents 2 00:55–01:10',
    'Impact(충돌)는 두 bodies(물체)가 짧은 시간 동안 큰 힘을 서로 가하는 collision(충돌 사건)입니다. 두 물체 사이의 contact impulses(접촉 충격량)는 크기가 같고 방향이 반대입니다.',
    '시험용 보강: 두 물체를 함께 system(계)으로 선택하면 이 내부 충격량은 합에서 사라집니다. 그러나 wall(벽), ground(지면), cord(줄)에서 오는 external impulse(외부 충격량)는 여전히 남을 수 있습니다. 이것이 운동량 보존을 판단하는 첫 단계입니다.')
add(16,'중심충돌과 직선·경사 충돌을 구분합니다.','Contents 2 01:16–02:43',
    'Line of impact(충돌선)는 접촉면의 common normal(공통 법선)입니다. Central impact(중심충돌)는 두 mass centers(질량중심)가 충돌선에 있는 경우이고, eccentric impact(편심충돌)는 그렇지 않은 경우입니다. 질량중심 위치에 관한 분류입니다.',
    'Direct central impact(직선 중심충돌)는 velocity(속도)가 충돌선과 나란한 경우, oblique central impact(경사 중심충돌)는 하나 이상의 물체에 충돌선과 다른 방향의 속도 성분이 있는 경우입니다. 원본 두 그림은 모두 중심충돌입니다.',
    extra=card('시험용 보강 · 충돌선은 상대속도 방향이 아닙니다.','구의 매끈한 접촉에서는 접촉 순간 두 중심을 잇는 선이 n축입니다. 먼저 접촉 기하학으로 n,t축을 정한 뒤 velocity(속도)를 투영합니다. 초기 속도 화살표를 n축이라고 임의로 정하면 경사 충돌에서 반발계수를 잘못 적용합니다.'))
add(17,'최대 변형 순간에는 법선 상대속도가 0입니다.','Contents 2 02:47–03:57',
    '직선 위에서 A가 더 빨라 vA&gt;vB라면 A가 B를 따라잡습니다. Deformation period(변형 단계) 동안 A는 감속하고 B는 가속하여 maximum deformation(최대 변형)에서 common velocity(공통 속도) u가 됩니다.',
    '이어서 restitution period(복원 단계)가 진행되면 두 물체는 원래 모양을 회복하거나 permanent deformation(영구 변형)을 남기며 분리합니다. Maximum deformation(최대 변형)에서의 u와 충돌이 끝난 뒤의 v′A,v′B는 일반적으로 다릅니다. e=0인 직선 중심충돌에서는 최종 속도도 공통입니다.')
add(18,'운동량 보존만으로 최종 속도 둘을 정할 수는 없습니다.','Contents 2 04:03–06:03',
    '외부 충격량이 무시 가능한 two-body system(두 물체 계)의 total momentum(총운동량)은 보존됩니다. 초기값을 모두 알아도 최종 속도 v′A,v′B 두 개에 대해 식이 하나뿐입니다. 두 번째 관계가 coefficient of restitution(반발계수)입니다.',eq='mAvA+mBvB = mAv′A+mBv′B',
    correction='원본 우변은 mBv′B+mBv′B로 같은 항이 반복되어 있습니다. 두 물체의 총운동량이므로 첫 항은 mAv′A여야 합니다. 앞뒤 그림과 다음 단계의 두 미지수 설명에 맞춰 수정하여 풉니다.')
add(19,'변형 단계와 복원 단계의 충격량을 각각 씁니다.','Contents 2 06:07–06:33',
    'A의 초기 운동 방향을 양수로 둡니다. B가 A를 미는 힘은 두 단계 모두 반대 방향입니다. 변형 단계의 contact-force magnitude(접촉력 크기)를 P, 복원 단계의 크기를 R이라 하면 JD=∫Pdt=mA(vA−u), JR=∫Rdt=mA(u−v′A)입니다.',
    'JD와 JR은 양의 impulse magnitude(충격량 크기)입니다. A에 작용하는 signed impulse(부호 있는 충격량)는 −JD, −JR입니다. 힘 방향과 적분의 크기를 구별하면 다음 비율에서 불필요한 음수가 생기지 않습니다.',eq='mAvA−JD=mAu<br>mAu−JR=mAv′A')
add(20,'반발계수는 복원 충격량과 변형 충격량의 비입니다.','Contents 2 06:38–06:56',
    'Coefficient of restitution(반발계수) e=JR/JD입니다. 앞의 식에 대입하면 A에 대해 e=(u−v′A)/(vA−u)이고 질량 mA는 약분됩니다. 복원 충격량이 작을수록 충돌 후 두 물체가 서로 멀어지는 정도가 작습니다.',
    '원본의 0≤e≤1은 이 강의에서 다루는 passive collision(외부·내부 저장에너지의 추가 방출이 없는 수동적 충돌) 모델입니다. 이 범위를 사용하여 계산 결과의 물리적 타당성을 확인합니다. e가 force ratio(힘의 비)라는 뜻은 아니며 각 단계의 시간 적분 비입니다.',eq='e = JR/JD = (u−v′A)/(vA−u)')
add(21,'공통 속도를 소거하면 상대속도 관계가 됩니다.','Contents 2 07:00–07:54',
    'B는 접촉력과 같은 양의 방향으로 가속되므로 e=(v′B−u)/(u−vB)입니다. A 식을 u−v′A=e(vA−u), B 식을 v′B−u=e(u−vB)로 적고 더하면 u가 사라집니다.',
    '따라서 v′B−v′A=e(vA−vB)입니다. Approach(접근)와 separation(분리)의 상대속력 비이므로 e는 보통 양수입니다. 같은 순서 vA−vB를 전후에 쓰면 상대속도의 부호가 반대로 바뀌어야 합니다.',eq='v′B−v′A = e(vA−vB)<br>또는 v′A−v′B = −e(vA−vB)')
add(22,'완전소성충돌과 완전탄성충돌은 서로 다른 한계입니다.','Contents 2 08:02–08:59',
    'Perfectly plastic impact(완전소성충돌) e=0이면 직선 중심충돌의 v′A=v′B=v′입니다. 운동량 보존으로 v′=(mAvA+mBvB)/(mA+mB)를 구합니다. Perfectly elastic impact(완전탄성충돌) e=1이면 접근 상대속력과 분리 상대속력이 같고 이 모델의 total kinetic energy(총 운동에너지)도 보존됩니다.',
    '편집자 보강: e=1인 일반 질량에서는 운동량과 반발계수 식을 함께 풀어야 합니다. Equal masses(같은 질량)일 때만 v′A=vB, v′B=vA가 됩니다. 경사 충돌에서는 e=0이어도 접선 상대속도가 남을 수 있으므로 모든 속도벡터가 같다고 일반화하지 않습니다.',
    correction='자막 08:35–08:45는 완전탄성충돌에서 두 속도가 서로 교환된다고 설명합니다. 이는 equal masses(같은 질량)의 직선 중심충돌 조건을 추가해야 맞습니다. 원본의 “total energy”는 충돌 역학에서 구별하려는 kinetic energy(운동에너지) 보존으로 명확히 합니다.',
    extra=card('시험용 보강 · 두 속도의 일반해',
        '<span class="formula">v′A = [(mA−emB)vA+(1+e)mBvB]/(mA+mB)<br>v′B = [(1+e)mAvA+(mB−emA)vB]/(mA+mB)</span>',
        '예를 들어 mA=2mB, vA=u, vB=0, e=1이면 v′A=u/3, v′B=4u/3입니다. 탄성충돌이지만 속도 교환이 아니라는 반례입니다. 원본에 없는 조건 검토용 예입니다.'))
add(23,'경사 중심충돌에서는 네 속도 성분이 미지수입니다.','Contents 2 09:05–09:53',
    '두 입자 각각에 normal component(법선 성분)와 tangential component(접선 성분)가 있어 v′An,v′At,v′Bn,v′Bt 네 미지수가 생깁니다. 먼저 원본 그림의 n축을 충돌선, t축을 접촉면 방향으로 고정합니다.',
    '여기서는 smooth contact(매끈한 접촉), 짧은 충돌 중 무시 가능한 외부 충격량, 회전 효과를 제외하는 중심충돌 모델을 사용합니다. 다음 세 장의 식을 세면 접선 두 개+법선 운동량 한 개+반발계수 한 개, 총 네 식입니다.')
add(24,'접선 충격량이 없으므로 각 입자의 접선 속도가 유지됩니다.','Contents 2 10:03–10:20',
    'Smooth contact(매끈한 접촉)의 접촉력은 n방향입니다. 외부의 t방향 충격량도 없다면 각 입자에 m(v′t−vt)=0이므로 v′At=vAt, v′Bt=vBt입니다. 이는 전체 계의 합뿐 아니라 각각의 입자에 대한 보존식입니다.',
    'Rough contact(거친 접촉)로 tangential friction impulse(접선 마찰 충격량)가 있거나 외부 구속 충격량이 t성분을 가지면 이 식을 쓸 수 없습니다. 다음 블록 문제에서 어떤 입자에 적용할지 다시 판단합니다.',eq='v′At = vAt<br>v′Bt = vBt')
add(25,'법선 방향에서는 두 입자의 운동량 합을 보존합니다.','Contents 2 10:29–10:47',
    'n방향의 internal contact impulses(내부 접촉 충격량)는 A와 B에 반대로 작용해 계 전체에서 상쇄됩니다. 외부 n충격량이 무시 가능하므로 법선 성분의 total momentum(총운동량)을 보존합니다.',
    '각 물체의 법선 속도가 그대로 유지되는 것은 아닙니다. 법선 방향에서는 충격량이 실제로 전달되며, 한 물체가 잃은 운동량을 다른 물체가 얻습니다.',eq='mAvAn+mBvBn = mAv′An+mBv′Bn')
add(26,'반발계수는 법선 상대속도에만 적용합니다.','Contents 2 10:58–11:01',
    'Restitution(반발)을 만드는 압축과 복원은 contact normal(접촉 법선)을 따라 발생합니다. 따라서 e 식에도 전체 speed(속력)가 아니라 normal velocity component(법선 속도 성분)를 넣습니다.',
    '네 식을 풀고 나면 Cartesian components(직교좌표 성분)로 돌아가거나 n,t 성분의 제곱합으로 magnitude(크기)를 구합니다. 방향각은 부호와 quadrant(사분면)를 확인해야 합니다.',eq='v′Bn−v′An = e(vAn−vBn)')
add(27,'지면에 구속된 블록에는 외부 충격량이 생길 수 있습니다.','Contents 2 11:04–12:08',
    'Block(블록) A는 horizontal surface(수평면)를 따라 움직이고 ball(공) B가 경사진 면과 충돌합니다. A의 최종 속도는 수평 크기 하나, B는 두 성분이므로 세 미지수입니다.',
    '접촉면의 internal force(내력) ±F뿐 아니라 지면의 vertical external force(수직 외력)도 impulse(충격량)를 줄 수 있습니다. 따라서 두 입자가 자유롭게 움직일 때의 “전체 n운동량 보존”을 그대로 가져오면 안 됩니다. 원본의 지면은 수평 마찰 충격량이 없는 모델입니다.')
add(28,'공의 접선 속도는 보존되지만 블록까지 같지는 않습니다.','Contents 2 12:11–12:21',
    'Ball(공) B에 작용하는 충격력은 접촉면의 n방향이므로 t성분의 impulse(충격량)는 0입니다. 따라서 B만의 tangential momentum(접선 운동량)이 보존됩니다.',
    'Block(블록) A에는 지면의 수직 반력 충격량이 추가되고, 이 힘은 일반적으로 경사진 t축에 성분을 가집니다. A에도 v′At=vAt라고 쓰면 구속 조건을 무시한 셈입니다.',eq='v′Bt = vBt')
add(29,'두 물체의 수평 운동량은 보존됩니다.','Contents 2 12:28–12:53',
    'A+B를 하나의 system(계)으로 잡으면 접촉 충격량은 상쇄되고 지면 충격량은 vertical(수직)입니다. Horizontal external impulse(수평 외부 충격량)가 없으므로 x방향의 전체 운동량은 보존됩니다.',
    '원본의 A 속도 vA,v′A는 수평으로만 움직이므로 그대로 x성분입니다. B의 속도는 x성분으로 투영해야 합니다. 수직 방향에는 지면 충격량이 있으므로 같은 보존식을 적용하지 않습니다.',eq='mAvA+mBvBx = mAv′A+mBv′Bx')
add(30,'구속된 블록의 속도도 법선으로 투영합니다.','Contents 2 12:58–13:03',
    '세 번째 식은 n방향의 relative velocity(상대속도)에 대한 restitution relation(반발 관계)입니다. A가 수평으로 움직여도 vAn과 v′An은 수평 속도 자체가 아니라 n축으로의 projection(투영)입니다.',
    '원본처럼 n축이 x축에서 θ만큼 기울면 vAn=vAcosθ, v′An=v′Acosθ입니다. B는 최종 두 성분을 n,t축 또는 x,y축 중 일관된 한 체계로 표현합니다.',eq='v′Bn−v′An = e(vAn−vBn)')
add(31,'구속 반력을 고려한 별도의 유도가 필요합니다.','Contents 2 13:12–13:30',
    '원본은 앞의 restitution expression(반발 식)이 자유 입자 두 개의 유도에서 자동으로 따라오지 않으며 separate derivation(별도 유도)이 필요하다고 주의합니다. 지면 구속이 A의 운동과 충격량 관계를 바꾸기 때문입니다.',
    '시험용 보강: n방향 접촉 충격량 크기를 J, n과 수평의 각도를 θ라 하면 A의 수평 속도 변화는 ΔvA=−Jcosθ/mA, B의 법선 변화는 ΔvBn=J/mB입니다. 따라서 상대 법선속도 변화는 J[1/mB+cos²θ/mA]입니다. 이 계수를 변형·복원 두 단계에 각각 사용하면 공통 계수가 약분되어 같은 상대속도형 e 식을 얻습니다. 접촉 기하학 고정·매끈한 접촉·이상적 수평 구속이라는 전제 안의 유도입니다.')
add(32,'세 원리는 같은 운동방정식을 다른 변수와 연결합니다.','Contents 2 13:35–13:51',
    'Newton’s second law(뉴턴 제2법칙)는 force–acceleration(힘–가속도), work–energy principle(일·에너지 원리)은 force–displacement(힘–변위), impulse–momentum principle(충격량·운동량 원리)은 force–time(힘–시간)의 관계를 이용합니다.',
    '어느 하나가 항상 더 우수한 방법은 아닙니다. Time(시간)을 묻는 제동 문제, velocity jump(속도 불연속 변화)를 다루는 충돌 문제, height(높이)를 묻는 진자 문제는 직접 연결되는 변수가 다릅니다.')
add(33,'충돌 전·충돌 중·충돌 후에 다른 식을 씁니다.','Contents 2 13:59–14:38',
    '원본 진자 그림은 낙하 구간의 energy conservation(에너지 보존), 접촉 순간의 momentum(운동량)·restitution(반발), 이후 상승 구간의 energy conservation(에너지 보존)을 순서대로 사용합니다.',
    '충돌 시간은 짧아 position change(위치 변화)가 거의 없다고 볼 수 있지만 velocity(속도)는 크게 바뀔 수 있습니다. 반대로 충돌 전후의 긴 진자 운동에서는 중력이 지속적으로 속도를 바꾸므로 선운동량을 보존하지 않습니다. 구간을 먼저 나누는 것이 공식 선택보다 앞섭니다.')
add(34,'Lecture 7-4 · 예제 풀이','Problem Solving',
    '제동 시간, 타격 평균 힘, 카트와 포장물, 구속된 두 공의 탄성충돌, 충돌 후 스프링 압축을 차례로 풉니다. 원본의 마지막 group problem(그룹 문제)도 함께 보존합니다.',role='Divider')

add(35,'예제 1 · 내리막 자동차의 정지 시간','Problem Solving 00:19–01:07',
    'Mass(질량) 1800 kg인 자동차가 5° downhill(내리막)에서 100 km/h로 이동합니다. 일정한 braking force(제동력) 7000 N을 가했을 때 come to a stop(정지하다)까지 걸리는 시간을 구합니다. 원본의 “weighing 1800 kg”는 질량을 일상적으로 표현한 말이며 weight(중량)는 mg N입니다.',
    'Downhill direction(내리막 방향)을 positive(양)로 둡니다. 초기 속도는 +100/3.6=+27.7778 m/s, final velocity(최종 속도)는 0입니다. 경사면에 수직인 normal force(수직항력)는 이 방향 운동량을 바꾸지 않습니다.')
add(36,'예제 1 · 시간이 미지수이므로 힘을 시간에 대해 적분합니다.','Problem Solving 01:13–01:34',
    'Impulse–momentum principle(충격량·운동량 원리)은 time(시간)을 직접 포함하므로 이 문제에 적합합니다. 원본의 에너지 방법에 대한 설명은 work–energy equation(일·에너지 식) 하나만으로 정지 시간을 직접 결정하기 어렵다는 뜻입니다.',
    'Braking(제동) 중에는 mechanical energy(역학적 에너지)가 보존되지 않습니다. 다만 제동력이 한 negative work(음의 일)를 포함하는 일·에너지 원리 자체는 여전히 성립합니다. 이를 이동거리와 연결하고 다른 운동학 식을 추가하는 풀이도 가능합니다.')
add(37,'예제 1 · 중력은 제동과 반대 방향입니다.','Problem Solving 01:38–03:16',
    '경사면 방향 resultant force(합력)는 mg sin5°−7000입니다. 두 힘이 일정하므로 impulse(충격량)는 그 합에 t를 곱하면 됩니다. 초기 momentum(운동량)을 0으로 낮추려면 이 순충격량이 음수여야 합니다.',
    '1800(27.7778)+[1800(9.81)sin5°−7000]t=0을 풀면 t=9.15583 s≈9.16 s입니다. 제동력 7000 N에서 중력의 경사 성분 약 1538.996 N을 뺀 값이 실제 감속에 기여합니다.',
    eq='t = mv₁/(7000−mg sin5°) ≈ 9.156 s')
add(38,'예제 1 · 결과는 가속도 식으로도 검산됩니다.','Problem Solving 03:18–03:53',
    '시험용 보강: a=g sin5°−7000/1800≈−3.03389 m/s²이므로 v₂=v₁+at=0에서 같은 정지 시간이 나옵니다. 이는 충격량·운동량 원리와 Newton’s second law(뉴턴 제2법칙)가 같은 법칙임을 확인하는 검산입니다.',
    '이 문제의 9초가량 구간에서는 중력이 만든 impulse(충격량)를 무시하면 안 됩니다. 짧은 impact(충돌)에서 중량 충격량을 생략하는 근사와 제동 문제의 조건은 서로 다릅니다.')

add(39,'예제 2 · 야구공을 때리는 평균 힘','Problem Solving 04:02–04:53',
    'Mass(질량) 0.120 kg인 baseball(야구공)이 왼쪽으로 24 m/s로 들어왔다가 오른쪽 위 40° 방향으로 36 m/s로 나갑니다. Contact time(접촉 시간)은 0.015 s입니다. 구할 것은 bat(배트)이 가한 average impulsive force(평균 충격력)입니다.',
    '오른쪽 +x, 위쪽 +y로 두면 incoming velocity(들어오는 속도)는 (−24,0), outgoing velocity(나가는 속도)는 (36cos40°,36sin40°) m/s입니다. 먼저 같은 좌표계의 벡터로 표현해야 부호를 잃지 않습니다.')
add(40,'예제 2 · 두 성분의 운동량 변화로 평균 힘을 구합니다.','Problem Solving 04:58–05:08',
    'Contact force(접촉력)의 실제 시간 파형은 주어지지 않았습니다. 따라서 peak force(최대 힘)가 아니라 같은 impulse(충격량)를 만드는 average force(평균 힘)를 구합니다. x,y방향에 각각 m v₁+FavgΔt=m v₂를 적용합니다.',
    '먼저 short impact interval(짧은 충돌 구간)에서 weight impulse(중량 충격량)를 무시하고, 계산 뒤 그 크기를 비교합니다. 이를 무시하지 않으면 y식의 외력은 Fbat,y−mg입니다.',
    correction='원본 40–43장의 “Determine the time”는 이 문제의 구할 양과 다릅니다. 시간 0.015 s는 주어진 조건이며, 본문에서는 average force(평균 힘)를 구합니다.')
add(41,'예제 2 · 수평 속도는 방향까지 뒤집힙니다.','Problem Solving 05:13–06:23',
    'x방향 식은 0.120(−24)+Fx(0.015)=0.120(36cos40°)입니다. 따라서 Fx=0.120[36cos40°+24]/0.015=412.621 N으로 오른쪽을 향합니다.',
    '24 m/s와 36 m/s를 단순히 빼면 안 됩니다. 초기 x속도가 negative(음)이므로 최종 x속도에서 빼면 +24가 더해집니다. 수평 impulse(충격량)는 FxΔt≈6.18931 N·s입니다.',eq='Favg,x ≈ +412.621 N')
add(42,'예제 2 · 수직 성분과 합력의 크기를 구합니다.','Problem Solving 06:26–07:24',
    '초기 y속도는 0입니다. 중량을 무시한 근사에서 Fy(0.015)=0.120(36sin40°)이므로 Fy=185.123 N입니다. 두 성분을 합성하면 magnitude(크기)는 √(Fx²+Fy²)=452.246 N입니다.',
    '시험용 보강: average force direction(평균 힘의 방향)은 atan2(Fy,Fx)=24.16°로 오른쪽 위입니다. 나가는 공의 velocity direction(속도 방향) 40°와 다릅니다. 힘은 최종 속도 자체가 아니라 velocity change(속도 변화) 방향을 가집니다.',eq='Favg ≈ (412.621, 185.123) N; |Favg| ≈ 452.246 N')
add(43,'예제 2 · 중량을 무시해도 되는지 수치로 확인합니다.','Problem Solving 07:27–08:47',
    'Weight(중량)는 mg=1.1772 N이고, 0.015 s 동안의 downward impulse(아래 방향 충격량)는 0.017658 N·s입니다. 계산된 타격 충격량 크기 약 6.78369 N·s의 약 0.26%이므로 이 예제의 근사는 타당합니다.',
    '시험용 보강: 중량까지 포함하면 배트의 y방향 평균 힘은 185.123+1.1772≈186.300 N입니다. 처음 구한 185.123 N은 정확히는 net average force(순평균 힘)의 y성분이며, 타격력과 거의 같은 값으로 근사한 것입니다. 이 구분 없이 “중력이 없다”고 설명하지 않습니다.')

add(44,'예제 3 · 포장물이 카트에 들어가 함께 움직입니다.','Problem Solving 08:52–09:58',
    'Package(포장물) 10 kg이 chute(슈트)를 따라 3 m/s로 수평 아래 30° 방향에서 들어와, 처음 정지해 있던 cart(카트)에 남습니다. 카트는 수평면에서 freely rolling(자유롭게 구르는) 이상 모델입니다. Common final speed(공통 최종 속력), 포장물에 작용한 impulse(충격량), kinetic energy lost(손실 운동에너지)의 비율을 구합니다.',
    '오른쪽 +x, 위쪽 +y이면 포장물의 초기 속도는 (3cos30°,−3sin30°) m/s입니다. 최종 두 물체의 속도는 (V,0)입니다.',
    correction='문제 슬라이드와 영상 09:21은 카트 질량 24 kg, 원본 풀이 47·51장은 25 kg입니다. 이 노트는 주어진 문제의 24 kg을 주 계산으로 채택하고 25 kg 풀이값은 비교로 분리합니다. 두 값 중 실제 출제 의도가 무엇인지는 자료만으로 확정하지 않습니다.')
add(45,'예제 3 · 계 전체와 포장물 하나를 구분합니다.','Problem Solving 10:04–10:42',
    '먼저 package+cart(포장물+카트)를 한 system(계)으로 잡아 horizontal momentum(수평 운동량) 보존으로 V를 구합니다. 그다음 package(포장물)만 선택해 impulse–momentum(충격량·운동량) 식으로 접촉 충격량의 두 성분을 구합니다.',
    '마지막에는 충돌 전후 kinetic energy(운동에너지)를 직접 계산합니다. 두 물체가 붙어 같은 속도로 움직이는 perfectly inelastic impact(완전비탄성충돌)이므로 에너지를 보존시켜 V를 구하지 않습니다.')
add(46,'예제 3 · 외부 수직 충격량은 남아 있습니다.','Problem Solving 10:49–11:34',
    '전체 계에서는 package–cart contact impulse(포장물–카트 접촉 충격량)가 internal(내부)이어서 상쇄됩니다. 그러나 지면이 바퀴에 주는 vertical impulse(수직 충격량)는 external(외부)이므로 사라지지 않습니다.',
    '수평의 외부 충격량은 무시 가능하므로 Px만 conserved(보존)됩니다. 처음 아래 방향이던 포장물의 운동량이 최종 0으로 바뀌므로, 수직 방향에는 반드시 순외부 충격량이 필요합니다.')
add(47,'예제 3 · 문제 조건 24 kg으로 공통 속도를 계산합니다.','Problem Solving 11:44–13:32',
    '수평 momentum equation(운동량 식)은 10(3cos30°)+24(0)=(10+24)V입니다. 따라서 V=0.764140 m/s 오른쪽입니다. 카트와 포장물은 충돌 후 함께 움직이므로 두 질량을 더합니다.',
    '원본 풀이처럼 25 kg을 넣으면 V=10(3cos30°)/35=0.742307 m/s입니다. 이 값은 다른 조건의 비교값이며, 이후 주 계산에 섞지 않습니다.',eq='V₂₄ = 0.764140 m/s; V₂₅ = 0.742307 m/s')
add(48,'예제 3 · 포장물의 운동량 변화가 접촉 충격량입니다.','Problem Solving 13:41–14:10',
    '이제 package(포장물)만 따로 그립니다. 카트가 포장물에 가한 contact impulse(접촉 충격량)는 이 작은 계에서는 external(외부)입니다. 최종 속도를 구했으므로 Jx=m(V−v₁x), Jy=m(0−v₁y)로 계산할 수 있습니다.',
    '여기서는 short impact(짧은 충돌) 중 중량 충격량을 neglect(무시)합니다. 정확히는 Jy,contact−mgΔt=mΔvy이며, 접촉 시간이 주어지지 않아 중량 보정을 수치화할 수 없습니다.')
add(49,'예제 3 · 포장물은 수평 운동량을 카트에 전달합니다.','Problem Solving 14:14–15:35',
    '24 kg 조건에서 Jx=10(0.764140−3cos30°)=−18.339361 N·s입니다. Negative(음)인 이유는 포장물이 오른쪽으로 가는 속도가 줄었기 때문입니다. 카트에는 반대로 +18.339361 N·s의 접촉 충격량이 전달됩니다.',
    '25 kg 비교값은 −18.557687 N·s입니다. 원본의 약 18.56이라는 크기는 이 25 kg 계산에서 나온 값입니다.',
    correction='원본 대입 줄에서 초기 momentum(운동량)과 FxΔt 사이의 기호가 등호처럼 표시되지만, 원리식은 초기 운동량 + impulse(충격량) = 최종 운동량입니다.',eq='10(3cos30°)+Jx = 10V')
add(50,'예제 3 · 아래로 들어오는 운동량을 위 충격량으로 제거합니다.','Problem Solving 15:42–16:45',
    'Jy=10[0−(−3sin30°)]=+15.000 N·s입니다. Upward(위 방향) 충격량이 포장물의 하향 운동량을 제거합니다. 이 값은 두 카트 질량 분기에서 같습니다.',
    '24 kg 주 계산의 resultant impulse(합성 충격량)는 √(18.339361²+15²)=23.692450 N·s입니다. 방향은 왼쪽 위입니다. 25 kg 비교값의 크기는 23.861847 N·s입니다. Impulse(충격량) 단위는 N·s이며 force(힘) 단위 N과 구별합니다.')
add(51,'예제 3 · 운동에너지 손실 비율을 계산합니다.','Problem Solving 16:52–18:12',
    'Initial kinetic energy(초기 운동에너지)는 포장물에만 있으므로 T₁=½(10)(3²)=45 J입니다. 충돌 후 24 kg 카트와 함께 움직이므로 T₂=½(34)V²=9.926471 J입니다.',
    'Loss fraction(손실 비율)은 (T₁−T₂)/T₁=0.779412, 즉 약 77.94%입니다. 에너지 차이 35.073529 J와 무차원 비율 0.779412를 구별합니다. 25 kg 비교 계산은 T₂=9.642857 J, 손실 약 78.57%이며 원본의 9.63 J는 반올림한 속도를 다시 대입한 값입니다.',eq='Fraction lost = 1−T₂/T₁ ≈ 0.7794 = 77.94%')
add(52,'예제 3 · 운동량 보존과 에너지 손실은 양립합니다.','Problem Solving 18:21–18:35',
    '이 perfectly inelastic impact(완전비탄성충돌)에서는 수평 운동량이 보존되어도 kinetic energy(운동에너지)는 감소합니다. 접촉 변형·열·소리 등으로 전환된 에너지는 현재의 입자 병진 운동에너지 계산에 남지 않습니다.',
    '원본의 에너지 비보존 설명은 이 강의의 passive collision(수동적 충돌) 모델에서 운동·역학적 에너지에 대한 말입니다. 전체 에너지 보존 법칙 자체가 깨진다는 의미가 아닙니다.')
add(53,'예제 3 · 보존 여부는 방향별 외부 충격량으로 판단합니다.','Problem Solving 18:42–19:02',
    '전체 initial vertical momentum(초기 수직 운동량)은 −15 kg·m/s, final vertical momentum(최종 수직 운동량)은 0입니다. 따라서 전체 계에 작용한 upward external impulse(위 방향 외부 충격량)가 약 +15 N·s여야 합니다.',
    '충돌에서는 접촉력의 세부 시간 변화를 몰라도 impulse–momentum(충격량·운동량)으로 전후 상태를 연결할 수 있습니다. 다만 적용 때마다 system(계), axis(축), neglected impulse(무시한 충격량)를 함께 명시해야 합니다.')

add(54,'예제 4 · 낙하하는 공과 줄에 매달린 공의 탄성충돌','Problem Solving 19:12–20:44',
    'Identical balls(동일한 공들) A와 B 중 B는 vertical inextensible cord(수직 비신축성 줄)에 매달려 있습니다. A는 그 줄 옆을 접하며 아래로 v₀로 낙하해 정지한 B와 충돌합니다. Smooth contact(매끈한 접촉), perfectly elastic impact(완전탄성충돌), e=1입니다.',
    '두 공의 질량과 반지름이 같아도 direct impact(직선충돌)가 아닙니다. A의 낙하 방향과 line of impact(충돌선)가 다르고 B에는 줄 구속이 있습니다. 따라서 단순한 “두 속도 교환” 규칙을 사용할 수 없습니다.')
add(55,'예제 4 · B는 충돌 직후 수평으로 움직입니다.','Problem Solving 20:51–21:28',
    '충돌 순간 B의 줄은 vertical(수직)이며 길이가 일정합니다. B의 velocity(속도)는 줄에 perpendicular(수직)이므로 충돌 직후 horizontal(수평)입니다. A는 두 성분, B는 수평 크기 하나로 최종 미지수가 세 개입니다.',
    'A의 tangential component(접선 성분) 보존, 전체 horizontal momentum(수평 운동량) 보존, normal restitution relation(법선 반발 관계)을 함께 사용합니다. 줄의 tension impulse(장력 충격량)가 있으므로 전체 수직 운동량은 보존되지 않습니다.')
add(56,'예제 4 · 충돌 좌표와 고정 좌표를 구별합니다.','Problem Solving 21:34–21:52',
    '오른쪽 x, 위쪽 y를 양수로 잡습니다. n축은 A에서 B로 향하는 왼쪽 아래 법선, t축은 오른쪽 아래 접선입니다. B의 왼쪽 속력은 b&gt;0, A의 충돌 후 signed normal component(부호 있는 법선 성분)는 a로 씁니다.',
    '편집자 보강: 원본의 기호와 부호를 명확히 읽기 위해 n=(−sinθ,−cosθ), t=(cosθ,−sinθ)로 정의합니다. a가 negative(음)이면 실제 법선 운동은 선택한 n의 반대 방향입니다.')
add(57,'예제 4 · 충돌선의 기울기는 30°입니다.','Problem Solving 21:59–22:24',
    '공 A가 줄 옆에 닿아 내려오므로 두 공 중심의 horizontal separation(수평 간격)은 radius(반지름) r입니다. 공끼리 닿는 순간 center distance(중심 거리)는 2r이므로 충돌선과 수직의 각도 θ에 대해 sinθ=r/(2r)=1/2입니다.',
    '따라서 θ=30°입니다. 이 각도는 수평과의 각도가 아니라 수직과의 각도입니다. A의 초기 속도 (0,−v₀)를 투영하면 vAn=v₀cos30°, vAt=v₀sin30°입니다.')
add(58,'예제 4 · A의 접선 성분은 0.5v₀로 유지됩니다.','Problem Solving 22:29–23:15',
    'A에 작용하는 contact impulse(접촉 충격량)는 n방향에만 있습니다. 따라서 t방향 운동량 변화는 0이고 v′At=vAt=v₀sin30°=0.5v₀입니다.',
    'B에는 줄의 외부 충격량이 있으므로 같은 t성분 보존을 적용하지 않습니다. A의 최종 속도는 a n+0.5v₀ t이고, x성분은 −a sin30°+0.5v₀cos30°입니다.',eq='v′At = 0.5v₀')
add(59,'예제 4 · 전체 수평 운동량은 처음과 같이 0입니다.','Problem Solving 23:17–25:07',
    '초기에는 A가 수직으로 낙하하고 B가 정지해 있으므로 Px=0입니다. 충돌 중 외부의 줄 충격량은 수직이며 중량 충격량은 무시하므로 수평 운동량을 보존할 수 있습니다.',
    'A의 오른쪽 성분과 B의 왼쪽 속도 −b를 넣으면 0=m[−a sin30°+0.5v₀cos30°]−mb입니다. 같은 질량을 약분하여 0.5a+b=0.433013v₀를 얻습니다.',eq='0.5a+b = (√3/4)v₀')
add(60,'예제 4 · B의 수평 속도를 법선에 투영합니다.','Problem Solving 25:14–25:58',
    'B의 속도는 (−b,0)이므로 normal component(법선 성분)는 v′Bn=b sin30°=0.5b입니다. A의 초기 법선 성분은 v₀cos30°, B는 0입니다.',
    'e=1을 적용하면 0.5b−a=v₀cos30°=0.866025v₀입니다. B의 speed(속력) b를 투영 없이 그대로 넣거나, A의 전체 초기 속력 v₀를 분모에 넣으면 다른 충돌 문제를 풀게 됩니다.',eq='0.5b−a = (√3/2)v₀')
add(61,'예제 4 · 음의 법선 성분을 실제 방향으로 해석합니다.','Problem Solving 26:04–26:31',
    '두 연립식을 풀면 a=−0.519615v₀, b=0.692820v₀입니다. A의 x,y성분은 v′Ax=−a sin30°+0.5v₀cos30°=0.692820v₀, v′Ay=−a cos30°−0.5v₀sin30°=0.200000v₀입니다.',
    '따라서 A의 speed(속력)는 0.721110v₀, 방향은 오른쪽 위 atan(0.2/0.692820)=16.10°입니다. B는 왼쪽으로 0.692820v₀입니다. 원본 그림의 0.520v₀ 화살표는 −n 방향의 양의 크기이고, 식의 a=−0.520v₀는 +n 기준의 음의 성분이므로 서로 모순이 아닙니다.',eq='v′A = (0.692820, 0.200000)v₀; v′B = (−0.692820, 0)v₀')
add(62,'예제 4 · 탄성충돌의 에너지 검산','Problem Solving 26:37–26:51',
    '시험용 보강: 최종 squared speeds(속력 제곱)의 합은 (0.692820²+0.2²+0.692820²)v₀²=(0.52+0.48)v₀²=v₀²입니다. 따라서 ½m v₀²가 보존되며 e=1 조건과 일치합니다.',
    '반면 초기 Py=−mv₀, 최종 Py=+0.2mv₀이므로 줄이 계에 약 +1.2mv₀의 vertical impulse(수직 충격량)를 전달했습니다. 운동에너지 보존과 모든 방향의 선운동량 보존은 같은 조건이 아닙니다.')

add(63,'예제 5 · 블록이 스프링 받침에 떨어진 뒤의 최대 처짐','Problem Solving 26:54–27:27',
    'Block(블록) A의 mass(질량)는 30 kg이고 pan(받침) B의 질량은 10 kg입니다. A를 받침 위 2 m에서 released from rest(정지 상태에서 놓음)하며 spring constant(스프링 상수)는 20 kN/m=20000 N/m입니다. 충돌은 perfectly plastic(완전소성), e=0입니다.',
    '구하는 maximum deflection(최대 처짐) h는 처음 정지해 있던 받침 위치에서 추가로 내려간 거리입니다. Natural length(자연길이)에서 잰 스프링 총 압축 x₄와 다릅니다.')
add(64,'예제 5 · 네 상태를 세 구간으로 연결합니다.','Problem Solving 27:30–28:20',
    '상태 1은 A를 놓는 순간, 2는 impact 직전(충돌 직전), 3은 impact 직후(충돌 직후), 4는 maximum compression(최대 압축)입니다. 1→2 낙하에는 energy(에너지), 2→3 짧은 충돌에는 momentum(운동량), 3→4 압축에는 energy(에너지)를 사용합니다.',
    '2와 3에서 position(위치)은 거의 같지만 velocity(속도)는 불연속적으로 달라집니다. 충돌을 가로질러 mechanical energy(역학적 에너지)가 보존된다고 놓지 않는 것이 핵심입니다.')
add(65,'예제 5 · 낙하 직전 속도는 6.264 m/s입니다.','Problem Solving 28:22–28:49',
    'Air resistance(공기저항)를 무시하면 A의 gravitational potential energy(중력 위치에너지) 감소가 kinetic energy(운동에너지)로 바뀝니다. 30g(2)=½(30)v₂²입니다.',
    '따라서 v₂=√(2g·2)=6.264184 m/s downward(아래 방향)입니다. 원본의 6.26 m/s는 반올림값입니다. B는 충돌 전 정지 상태입니다.',eq='v₂ = √(2g·2) ≈ 6.264184 m/s')
add(66,'예제 5 · 짧은 충돌에서 두 물체의 공통 속도를 구합니다.','Problem Solving 28:56–29:35',
    'Downward(아래 방향)를 양수로 두고 A+B를 system(계)으로 선택합니다. 충돌 시간 동안 gravity(중력)와 spring force(스프링 힘)의 impulse(충격량)가 큰 접촉 충격량에 비해 작다는 근사에서 30v₂+10(0)=40v₃입니다.',
    'e=0이라 두 물체는 common velocity(공통 속도)를 가지며 v₃=4.698138 m/s입니다. 시험용 보강: 운동에너지는 충돌 직전 588.6 J, 직후 441.45 J이므로 147.15 J, 즉 25%가 소산됩니다. 중력·스프링을 이후 구간에서도 무시한다는 뜻은 아닙니다.',eq='v₃ = (30/40)v₂ ≈ 4.698138 m/s')
add(67,'예제 5 · 받침의 무게 때문에 스프링은 이미 압축되어 있습니다.','Problem Solving 29:44–30:15',
    '충돌 전 B는 static equilibrium(정적 평형)이므로 kx₃=mBg입니다. 따라서 initial compression(초기 압축) x₃=10(9.81)/20000=0.004905 m입니다. 짧은 충돌 직전·직후의 위치는 같다고 봅니다.',
    '3→4에서 추가 하강량 h가 생기면 final compression(최종 압축)은 x₄=x₃+h입니다. 스프링 에너지는 ½kx²이므로 처음의 작은 압축도 식에 포함해야 합니다.',eq='x₃ = 0.004905 m; x₄ = x₃+h')
add(68,'예제 5 · 충돌 이후에는 중력이 계속 일을 합니다.','Problem Solving 30:17–31:20',
    '상태 3의 kinetic energy(운동에너지)는 441.45 J이고 상태 4에서는 순간적으로 0입니다. 두 물체가 함께 h만큼 하강하므로 중력이 하는 positive work(양의 일)는 40gh입니다. 이는 스프링 에너지의 증가량과 함께 계산합니다.',
    '441.45+40gh=½k[(x₃+h)²−x₃²]입니다. 초기 스프링 에너지 ½kx₃²를 양변에 더하면 원본처럼 초기·최종 전체 에너지를 비교하는 형태가 됩니다.',eq='441.45+392.4h = 10000[(0.004905+h)²−0.004905²]')
add(69,'예제 5 · 추가 처짐과 총 압축을 따로 답합니다.','Problem Solving 31:24–31:39',
    '식을 전개하면 10000h²−294.3h−441.45=0입니다. 처음부터 더 내려가는 maximum deflection(최대 처짐)에 해당하는 positive root(양의 근)를 선택하면 h=0.225337 m입니다.',
    '총 압축은 x₄=x₃+h=0.230242 m입니다. 원본의 반올림 답 h≈0.225 m, x₄≈0.230 m와 일치합니다. 영어 답에서는 “The maximum additional deflection of the pan is 0.225 m.”처럼 additional(추가)을 명시하면 기준점이 분명합니다.',
    correction='Problem Solving 자동자막 31:35의 “0.25”는 원본 답과 계산의 0.225 m에 맞지 않습니다. 본문은 원본 조건으로 검산한 0.22534 m를 사용하며 원문 자막은 보존합니다.')
add(70,'예제 5 · 하나의 보존식을 전 구간에 쓰지 않습니다.','Problem Solving 31:41–32:04',
    '낙하와 충돌 후 압축은 각각 mechanical energy conservation(역학적 에너지 보존)으로 연결하지만 충돌 중에는 kinetic energy(운동에너지)가 감소합니다. 반대로 충돌 중 근사적으로 쓴 momentum conservation(운동량 보존)은 긴 낙하·압축 구간에는 적용되지 않습니다.',
    '시험용 보강: 최대 압축은 velocity(속도)가 0인 turning point(방향 전환점)이지 static equilibrium(정적 평형)이 아닙니다. 이 순간 스프링 힘은 전체 중량보다 커서 곧 위쪽으로 가속합니다. v=0과 a=0을 동일하게 취급하지 않습니다.')

add(71,'그룹 문제 · 스프링에서 출발한 블록과 진자의 충돌','Problem Solving 32:07–32:53',
    'Block(블록) A는 2 kg, ball(공) B는 1 kg입니다. Spring(스프링) k=800 N/m를 x=0.1 m 압축했다 놓으면 A가 20° incline(경사면)을 내려옵니다. Kinetic friction coefficient(운동마찰계수)는 μₖ=0.2이며, unstretched spring position(스프링 자연길이 위치)에서 충돌 지점까지 d=1.5 m입니다.',
    '따라서 A가 실제 미끄러지는 총 거리는 x+d=1.6 m입니다. d만을 중력·마찰의 이동거리에 넣으면 압축 해제 중 이동한 0.1 m를 빠뜨립니다. B는 길이 1 m의 줄에 매달려 정지해 있습니다.')
add(72,'그룹 문제 · 충돌 후 40°에서 속력과 장력을 구합니다.','Problem Solving 32:57–33:49',
    'Coefficient of restitution(반발계수)는 e=0.8입니다. 충돌 뒤 진자가 수직에서 α=40°만큼 올라간 위치에서 ball speed(공의 속력)와 cord tension(줄 장력)을 구합니다. 원본과 영상은 문제·전략까지만 제시하며 최종 수치 풀이가 없습니다.',
    '시험용 보강의 모델: 그림의 블록 앞면에 대한 contact normal(접촉 법선)을 경사면 방향으로 둡니다. 매끈한 중심 접촉, 충돌 중 A의 경사면 구속 유지, B의 이상적 팽팽한 줄, 중량·마찰의 충격량 무시를 가정합니다. 접촉면 기하학이나 충격 마찰을 다르게 설정하면 결과도 달라지며, 아래 수치는 강의가 제공한 공식 답이 아닙니다.')
add(73,'그룹 문제 · 에너지 → 구속 충돌 → 진자 운동 → 장력','Problem Solving 33:50–34:36',
    '원본의 strategy(풀이 전략)는 충돌 전·후를 분리하는 것입니다. 아래는 원본에 생략된 대수와 수치를 채운 시험용 보강이며 앞 장의 이상화 조건을 사용합니다.',
    extra=card('시험용 보강 1 · 충돌 직전 A의 속력',
        '스프링에서 받은 energy(에너지)는 ½kx²=4 J입니다. 전체 이동거리 L=x+d=1.6 m에 대해 ½mAu²=½kx²+mAgLsin20°−μₖmAgLcos20°입니다. 따라서 u=2.972697 m/s입니다. 스프링이 자연길이에 도달한 뒤 A와 분리되고, 마찰은 전체 미끄럼 구간에서 작용하는 모델입니다.')+
    card('시험용 보강 2 · 수평으로 움직이는 B의 구속을 반영',
        '접촉 법선 n=(cos20°,−sin20°), A의 충돌 직후 경사 방향 속도를 a, B의 오른쪽 수평 속도를 b라 둡니다. 접촉 충격량 크기 J에 대해 a=u−J/mA, b=Jcos20°/mB입니다. B의 수직 속도는 줄 구속으로 0이며 줄의 vertical impulse(수직 충격량)가 이를 유지합니다.',
        'Normal relative velocity(법선 상대속도) 식은 bcos20°−a=eu입니다. 대입하면 J=(1+e)u/[1/mA+cos²20°/mB]=3.868958 N·s, a=1.038218 m/s, b=3.635632 m/s입니다. B의 속도 b 자체를 법선 속도로 취급하는 일차원 충돌 공식은 이 기하학에 맞지 않습니다.',
        '검산: 이 모델에서는 mAu cos20°=mAa cos20°+mBb로 수평 운동량이 보존됩니다. 그러나 줄의 외부 수직 충격량 때문에 경사면 방향 전체 운동량을 보존시켜서는 안 됩니다.')+
    card('시험용 보강 3 · α=40°에서 속력',
        '충돌 후 진자 운동에는 energy conservation(에너지 보존)을 적용합니다. 높이 증가는 Δh=ℓ(1−cos40°)이며 ½mBb²=½mBv₄₀²+mBgℓ(1−cos40°)입니다. ℓ=1 m를 넣으면 v₄₀=2.937279 m/s입니다. 제곱근 안이 양수이므로 공은 이 각도에 도달할 수 있습니다.')+
    card('시험용 보강 4 · 줄 장력',
        '줄 방향 inward(중심을 향하는) 축에 Newton’s second law(뉴턴 제2법칙)를 쓰면 T−mBgcos40°=mBv₄₀²/ℓ입니다. 따라서 T=16.142505 N≈16.14 N입니다. T=mBgcos40°라는 정적 평형식은 centripetal acceleration(구심가속도)을 누락합니다.',
        '모델 기반 보강 답: α=40°에서 speed(속력)≈2.937 m/s, tension(장력)≈16.14 N. 구속과 접촉 법선의 가정을 답과 함께 유지합니다.'))
add(74,'참고문헌','원본 Reference 페이지',
    '원본이 제시한 Beer, Johnston, Cornwell, Self, Sanghi의 <i>Vector Mechanics for Engineers: Dynamics</i>, 12th edition(제12판), Chapter 13(제13장)을 보존한 참고문헌 페이지입니다. 별도의 교재 내용을 새로 인용하거나 대조한 것은 아닙니다.',role='Reference')

exam_items = [
    ('State the principle of impulse and momentum(충격량·운동량 원리를 서술하라).',
     'For a particle of constant mass in an inertial frame, the net impulse equals the change in linear momentum: ∫ΣF dt = mv₂ − mv₁. This is a vector equation.',
     'Constant mass(일정 질량), inertial frame(관성 기준계), net impulse(순충격량), change in linear momentum(선운동량 변화)를 연결하는 답안입니다. 성분별 부호까지 포함하는 vector equation(벡터 방정식)임을 명시합니다.'),
    ('Explain why horizontal momentum is conserved(수평 운동량이 보존되는 이유를 설명하라).',
     'For the package–cart system, the contact impulses are internal and cancel. The external horizontal impulse is negligible, so total horizontal momentum is conserved. Vertical momentum is not conserved because of the ground impulse.',
     'System(계)과 horizontal direction(수평 방향)을 함께 지정합니다. Internal(내부) 접촉 충격량 상쇄와 negligible external impulse(무시 가능한 외부 충격량)가 논리적 근거입니다.'),
    ('Define the coefficient of restitution(반발계수를 정의하라).',
     'The coefficient of restitution is the ratio of the relative speed of separation to the relative speed of approach, measured along the line of impact: e = (v′Bn − v′An)/(vAn − vBn).',
     'Relative speed(상대속력), separation(분리), approach(접근), line of impact(충돌선)를 빠뜨리지 않습니다. 한 물체의 최종·초기 speed ratio(속력비)가 아닙니다.'),
    ('Distinguish perfectly elastic and perfectly inelastic impact(완전탄성충돌과 완전비탄성충돌을 구별하라).',
     'For an isolated direct central impact, e = 1 corresponds to perfectly elastic impact and kinetic energy is conserved. For e = 0, the bodies have a common final velocity and kinetic energy generally decreases. Momentum is conserved in both cases when the external impulse is negligible.',
     'Isolated direct central impact(고립된 직선 중심충돌)라는 조건 안의 답입니다. Common final velocity(공통 최종 속도)는 여기서 직선 속도 전체에 적용됩니다. 일반적인 경사 충돌에서 e=0은 먼저 법선 상대속도가 0이라는 뜻입니다.'),
    ('Determine the average force during impact(충돌 중 평균 힘을 구하라).',
     'Neglecting the impulse of the weight, Favg = m(v₂ − v₁)/Δt. For the baseball, Favg ≈ (412.621, 185.123) N, with a magnitude of 452.246 N. This is an average force, not the peak force.',
     'Neglecting(무시하면)으로 근사를 밝히고 component(성분), magnitude(크기), average versus peak(평균과 최대의 차이)를 구별합니다. Initial velocity(초기 속도)는 −24 m/s입니다.'),
    ('Determine the fraction of kinetic energy lost(손실 운동에너지 비율을 구하라).',
     'Using the stated cart mass of 24 kg, the final speed is 0.764140 m/s. The initial and final kinetic energies are 45 J and 9.926471 J. The fraction lost is (45 − 9.926471)/45 ≈ 0.7794, or 77.94%.',
     'Stated mass(명시된 질량)를 써서 24 kg 기준임을 분명히 합니다. Fraction(비율)은 dimensionless(무차원)이며 energy lost(손실 에너지) 자체의 J 단위와 다릅니다.'),
    ('Explain which momentum components are conserved(어느 운동량 성분이 보존되는지 설명하라).',
     'In the two-ball example, ball A has no tangential contact impulse, so its tangential velocity is unchanged. The cord exerts a vertical impulse on ball B. Thus, total horizontal momentum is conserved, but total vertical momentum is not.',
     'Tangential contact impulse(접선 접촉 충격량)가 없는 A와, cord impulse(줄 충격량)를 받는 B를 구별합니다. Unchanged(변하지 않는) 성분을 물체별로 특정합니다.'),
    ('Determine the maximum additional deflection(최대 추가 처짐을 구하라).',
     'Apply energy conservation before impact, momentum conservation during the short impact, and energy conservation after impact. The post-impact speed is 4.698138 m/s. Including the initial spring compression of 0.004905 m gives an additional deflection of 0.225337 m and a total compression of 0.230242 m.',
     'Before/during/after impact(충돌 전/중/후)를 나누고 initial compression(초기 압축), additional deflection(추가 처짐), total compression(총 압축)을 서로 다른 값으로 제시합니다.'),
    ('Explain how to determine the cord tension(줄 장력을 구하는 방법을 설명하라).',
     'After finding the speed from energy conservation, apply Newton’s second law toward the center: T − mg cosα = mv²/ℓ. The centripetal acceleration must be included; the pendulum is not in static equilibrium.',
     'Toward the center(중심을 향해)를 positive direction(양의 방향)으로 정합니다. Centripetal acceleration(구심가속도)을 빼고 static equilibrium(정적 평형)으로 풀면 장력을 작게 구하게 됩니다.'),
]

terms = [
    ('linear momentum / total momentum','선운동량 / 총운동량','mv / 선택한 계의 각 입자 운동량의 벡터합'),
    ('impulse / net impulse','충격량 / 순충격량','힘의 시간 적분 / 모든 외력 충격량의 합'),
    ('impulsive / nonimpulsive force','충격력 / 비충격력','짧은 시간에 큰 운동량 변화를 만드는 힘 / 그 구간 충격량이 상대적으로 작은 힘'),
    ('average force / peak force','평균 힘 / 최대 힘','구간 충격량을 시간으로 나눈 힘 / 시간 파형의 최대값'),
    ('contact time / time interval','접촉 시간 / 시간 구간','접촉이 지속되는 시간 / 적분의 시작과 끝 사이 시간'),
    ('constant mass / inertial frame','일정 질량 / 관성 기준계','시간에 따라 질량이 일정한 모델 / 관성 법칙이 성립하는 기준계'),
    ('system / internal / external','계 / 내부의 / 외부의','함께 분석할 물체 집합 / 계 안의 상호작용 / 계 밖에서 들어오는 작용'),
    ('conserved / negligible','보존되는 / 무시할 만큼 작은','선택한 구간에서 일정한 / 비교 기준에 비해 효과가 충분히 작은'),
    ('impact / collision','충돌 / 충돌','매우 짧은 접촉 동안 큰 상호작용이 일어나는 사건'),
    ('line of impact / common normal','충돌선 / 공통 법선','접촉점에서 양쪽 접촉면에 수직인 선'),
    ('central / eccentric impact','중심충돌 / 편심충돌','충돌선이 두 질량중심을 지남 / 그렇지 않음'),
    ('direct / oblique central impact','직선 / 경사 중심충돌','초기 속도들이 충돌선과 나란함 / 법선 외의 성분도 가짐'),
    ('normal / tangential component','법선 / 접선 성분','접촉면에 수직인 성분 / 접촉면을 따르는 성분'),
    ('smooth / frictionless contact','매끈한 / 마찰 없는 접촉','충돌 접선 방향의 마찰 충격량을 무시하는 이상 모델'),
    ('deformation / restitution period','변형 / 복원 단계','접촉 압축이 증가하는 단계 / 접촉이 복원되어 분리하는 단계'),
    ('coefficient of restitution','반발계수','법선 분리 상대속력÷접근 상대속력, 이 강의에서는 0≤e≤1'),
    ('approach / separation','접근 / 분리','두 접촉 물체가 가까워짐 / 서로 멀어짐'),
    ('relative velocity / projection','상대속도 / 투영','두 속도의 차 / 지정한 축에 대한 성분을 구함'),
    ('perfectly elastic / perfectly plastic','완전탄성 / 완전소성','이 강의의 e=1 충돌 / e=0 충돌'),
    ('perfectly inelastic / common velocity','완전비탄성 / 공통 속도','e=0인 충돌 / 여러 물체가 함께 갖는 속도'),
    ('kinetic energy / energy lost','운동에너지 / 손실 에너지','½mv² / 여기서는 충돌 전후 운동에너지 감소분'),
    ('fraction / percentage','비율 / 백분율','부분량÷기준량 / 비율에 100을 곱한 % 표현'),
    ('immediately before / after impact','충돌 직전 / 직후','충돌 구간의 앞 상태 / 뒤 상태; 프라임은 뒤 상태 표기'),
    ('signed component / magnitude','부호 있는 성분 / 크기','기준 축 방향을 부호로 표시한 값 / 벡터의 비음수 길이'),
    ('braking / downhill / come to a stop','제동 / 내리막 / 정지하다','운동을 줄이는 작용 / 경사면 아래 방향 / 최종 속도 0'),
    ('bat / baseball / outgoing','배트 / 야구공 / 나가는','타격 도구 / 타격받는 공 / 충돌 후 접촉에서 벗어나는 상태'),
    ('package / cart / chute','포장물 / 카트 / 슈트','이동하는 짐 / 바퀴가 달린 수레 / 짐이 내려오는 안내 통로'),
    ('freely rolling / initially at rest','자유롭게 구르는 / 처음 정지한','수평 저항을 무시하는 구름 모델 / 초기 속도 0'),
    ('identical / constrained / free','동일한 / 구속된 / 자유로운','질량·크기 등 제시 조건이 같음 / 운동 방향이 제한됨 / 해당 구속이 없음'),
    ('inextensible / taut cord','늘어나지 않는 / 팽팽한 줄','길이 일정 / 장력을 전달하며 느슨하지 않은 줄'),
    ('pan / released from rest','받침 / 정지 상태에서 놓인','블록을 받는 쟁반 형태의 물체 / 초기 속도 0으로 운동 시작'),
    ('natural length / initial compression','자연길이 / 초기 압축','스프링 변형 0인 길이 / 이미 존재하는 압축량'),
    ('additional deflection / total compression','추가 처짐 / 총 압축','처음 위치에서 더 내려간 거리 / 자연길이 기준 전체 압축'),
    ('turning point / static equilibrium','방향 전환점 / 정적 평형','순간 속도 0으로 방향이 바뀌는 위치 / 정지 상태의 합력 0'),
    ('incline / kinetic friction / tension','경사면 / 운동마찰 / 장력','기울어진 면 / 미끄럼을 거스르는 힘 / 줄의 당기는 힘'),
    ('centripetal / inward','구심의 / 안쪽 방향의','곡률중심을 향하는 가속도 / 중심을 향하는 방향'),
    ('determine / state / distinguish','구하라 / 서술하라 / 구별하라','계산해 결정 / 원리나 조건을 명시 / 차이와 기준을 설명'),
    ('neglect / assume / verify','무시하라 / 가정하라 / 검산하라','모델에서 작은 효과 제외 / 적용 전제 명시 / 독립 관계로 확인'),
]

audit = [
    ('Overview 00:20–00:30','문장 중간부터 시작 / first','누락 도입은 복원하지 않음 / force(힘)','확보된 원문 시작과 접촉 시간 문맥'),
    ('Contents 1 00:52–01:09·02:42','inputs, inverse / factorially','impulse(충격량) / vectorially(벡터적으로)','원본 7–9의 정의·벡터합'),
    ('Contents 1 02:55–03:28·04:35–05:15','impressive, non-inclusive / bed, bet, basement','impulsive/nonimpulsive(충격성/비충격성) / bat, baseball(배트, 야구공)','원본 10–12의 분류와 그림'),
    ('원본 5','로켓 그림과 일정 질량 입자식의 연결','변하는 로켓 질량은 별도 운동량 유출입 분석 필요','constant mass(일정 질량)인 이번 유도의 적용 범위'),
    ('원본 14 · Contents 2 00:19–00:43','골프공의 e 상한을 0.83으로 소개','보편적 공의 반발계수 규정으로 암기하지 않음','USGA 공식 설명은 클럽·클럽페이스의 적합성 검사 맥락; 본문 링크'),
    ('Contents 2 01:16–02:43','line of inputs / unclick / oblique','line of impact(충돌선) / 원본의 direct·oblique 분류','원본 16의 기하학 정의'),
    ('원본 18','우변 mBv′B+mBv′B','mAv′A+mBv′B','충돌 후 A와 B의 총운동량'),
    ('Contents 2 06:13–06:46','receives inputs / restitution inputs / deformation inputs','impulse(충격량), 복원·변형 충격량으로 해석','원본 19–21의 단계별 식'),
    ('Contents 2 08:35–08:45','e=1이면 두 물체 속도 교환','equal masses(같은 질량)의 직선 중심충돌에서만 교환','운동량·반발계수 연립식'),
    ('원본 22','e=0이면 같은 속도','직선 중심충돌의 공통 속도; 경사 충돌은 법선 성분부터 해석','원본 23–30의 성분 분석'),
    ('원본 27–31','구속 문제에도 자유 입자 유도를 그대로 사용하기 쉬움','지면 충격량 및 법선 투영 포함, 별도 유도 보강','원본 31의 separate derivation 안내'),
    ('Problem Solving 01:03 / 원본 35–38','start completely / energy method를 쓸 수 없다는 설명','stop completely(완전히 정지) / 일·에너지식 단독으로 시간 직접 계산 불가','문제의 정지 조건; 시간 포함 원리 선택'),
    ('원본 40–43','Determine the time','Determine the average force(평균 힘을 구하라)','0.015 s는 이미 주어진 접촉 시간'),
    ('원본 44·47·51 / Problem Solving 09:21','문제 24 kg, 풀이 25 kg','24 kg을 주 계산; 25 kg 원본 답 비교','문제 진술·영상은 24 kg, 의도는 확정 불가'),
    ('Problem Solving 08:57–09:58','friction / shoot / card','fraction(비율) / chute(슈트) / cart(카트)','원본 문제의 에너지 비율과 물체 명칭'),
    ('원본 49','대입 줄에서 초기 운동량과 충격량 사이 등호','초기 운동량 + 충격량 = 최종 운동량','위 원리식과 차원·운동량 변화'),
    ('원본 51','T₂=9.63 J','25 kg·반올림 속도로 얻은 값; 24 kg 주 계산 T₂=9.92647 J','반올림 없는 두 질량 분기 재계산'),
    ('원본 52','충돌에서 에너지가 보존되지 않는다는 문구','수동적 충돌의 운동·역학적 에너지 감소로 한정','전체 에너지 보존과 구별'),
    ('원본 61','음의 −0.520v₀와 그림의 양의 0.520v₀','부호 있는 +n 성분과 −n방향 크기 구별','원본 축과 x,y 성분 재구성'),
    ('원본 65–69','6.26, 4.70, 442 등 반올림값','전 과정 반올림 없는 계산과 원본 반올림 답 병기','g=9.81 m/s² 재계산; 최종 답 일치'),
    ('Problem Solving 31:35','height 0.25','additional deflection(추가 처짐)≈0.22534 m','원본 69의 0.225 m와 이차방정식'),
    ('원본 71–73','그룹 문제는 전략만 있고 최종 풀이 없음','접촉 법선·구속 가정과 함께 보강 계산 표시','단순 일차원 충돌식 배제; 원본 공식 답으로 표시하지 않음'),
    ('Summary 00:18–00:54','in-person, impressive / Ally elastic','impulse(충격량) / perfectly elastic(완전탄성)','원본 정의 및 요약 문맥'),
    ('Summary 00:56–01:11','system of particles, rigid bodies','다음 단원 안내로 분리','현재 단원 복습과 이후 과정 구분'),
]

roadmap = '''<section class="editorial-section section-divider" id="course-roadmap" aria-labelledby="roadmap-title">
<p class="section-kicker">Summary video · Course roadmap</p>
<h2 class="section-title" id="roadmap-title">Summary 영상 후반: 다음은 입자계입니다.</h2>
<p class="section-lead">Summary 00:18–00:54의 impulse–momentum(충격량·운동량), direct/oblique impact(직선/경사 충돌), restitution(반발) 복습은 위 핵심 개념 요약에 반영했습니다. 뒤의 다음 단원 안내만 여기서 구분합니다.</p>
</section>
<section class="editorial-section" id="roadmap-detail" aria-labelledby="roadmap-detail-title">
<p class="section-kicker">What comes next</p>
<h2 class="section-title" id="roadmap-detail-title">개별 입자에서 여러 입자의 계로 확장합니다.</h2>
<div class="card"><h3>Systems of particles(입자계)</h3><p>다음 렉처에서는 여러 입자를 묶어 분석하고 이후 rigid-body dynamics(강체 동역학)로 이어집니다. 보존된 강의 인덱스의 다음 일정은 Week 07 · 2026-10-14 · Lecture 8입니다. 이 예고는 이번 강의의 개념 복습을 대신하지 않습니다.</p></div>
<div class="evidence"><span>Summary 00:56–01:11</span><span>강의 인덱스 대조</span></div>
</section>'''

template = (SITE/'templates/lecture-page.template.html').read_text(encoding='utf-8')
source_pattern = r'<section class="source-section"[\s\S]*?</section>'
source_template = re.search(source_pattern,template).group()
sections = []
assert len(records)==74
for n,(title,evidence,blocks,role) in enumerate(records,1):
    section = source_template
    replacements = {'NN':f'{n:02d}', 'SLIDE_ROLE':role, 'SLIDE_HEADING':title,
        'LECTURE_SLUG':'lecture07','DESCRIPTIVE_ALT_TEXT':f'Lecture 7 원본 슬라이드 {n:02d}: {escape(title)}',
        'CURRENT_PAGE':str(n),'PAGE_COUNT':'74','TRANSCRIPT_TIME_OR_SLIDE_ROLE':evidence,
        'SLIDE_EXPLANATION_BLOCKS':blocks}
    for key,value in replacements.items():
        section = section.replace('{{'+key+'}}',value)
    sections.append(section)
template = re.sub(source_pattern,lambda _: '\n\n'.join(sections),template,count=1)
exam_html = ''.join('<div class="exam-card"><h3>'+q+'</h3><div class="answer"><span class="answer__label">Model answer</span>'+escape(a)+'</div><p style="margin-top: 12px">'+ko+'</p></div>' for q,a,ko in exam_items)
template = re.sub(r'<div class="exam-card">\s*<h3>\{\{EXAM_QUESTION\}\}</h3>[\s\S]*?</div>\s*</div>',lambda _:exam_html+'\n          </div>',template,count=1)
videos = [('Overview','N5RhmnCqtZg'),('Contents 1','VY_wTpAjoI8'),('Contents 2','jvt8mX2OSfs'),('Problem Solving','PdgyxxL0DeA'),('Summary','-2JYBx5dGEo')]
toc = [('overview','전체 개요'),('concept-map','개념 지도'),('concept-summary','핵심 개념 요약')] + [(f'slide-{i:02d}',f'{i:02d} · {r[0]}') for i,r in enumerate(records,1)] + [('course-roadmap','Summary · 다음 단원 안내'),('exam-english','시험 영어'),('glossary','용어집'),('asr-log','원본·스크립트 교정'),('sources','출처')]
values = {
    'LECTURE_NUMBER':'Lecture 7','LECTURE_TITLE':'Impulse and Momentum Principle',
    'ONE_SENTENCE_DESCRIPTION':'6주차 충격량과 운동량 원리: 원본 74장과 영어 영상 5편을 대조한 한국어 수업 대체 학습 노트',
    'WEEK':'Week 06','DATE_OR_날짜_미기재':'2026-10-07','PAGE_COUNT':'74',
    'LECTURE_PROMISE':'Impulse(충격량)와 momentum(운동량)으로 힘과 시간을 연결하고, restitution(반발)·구속 조건·에너지 손실을 적용해 제동과 충돌 문제를 단계별로 설명합니다.',
    'VIDEO_SET':'Overview · Contents 1·2 · Problem Solving · Summary',
    'ALL_CONTENTS_AND_PROBLEM_SOLVING_BUTTONS':'\n'.join(f'<a class="button button--primary" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상 열기</a>' for label,vid in videos[1:4]),
    'ORIGINAL_PDF_URL':'https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/lecture07_note.pdf',
    'LECTURE_NOTE_FILENAME':'lecture07_note.pdf',
    'CORE_RELATIONSHIP_HEADLINE':'힘이 작용한 시간으로, 충돌 전후의 운동을 연결합니다.',
    'CORE_RELATIONSHIP_EXPLANATION':'Force(힘)의 시간 적분인 impulse(충격량)는 linear momentum(선운동량)을 변화시킵니다. 여러 물체를 묶을 때는 외부 충격량이 사라지는 방향만 운동량을 보존하며, impact(충돌)의 나머지 관계는 coefficient of restitution(반발계수)와 constraint(구속 조건)로 채웁니다.',
    'CONCEPT_MAP_HEADLINE':'충격량의 정의에서 구속된 충돌과 복합 문제까지.',
    'CONCEPT_MAP_BLOCKS':'<div class="grid-3">'+card('Impulse(충격량)','∫ΣF dt=mΔv. 시간 적분으로 속도 변화를 연결하고 성분별 부호를 정합니다.')+card('Impact(충돌)','계와 방향별 외부 충격량을 확인합니다. 법선 상대속도에 반발계수를 적용합니다.')+card('Combined methods(원리의 결합)','낙하·충돌·상승을 나눕니다. 거리에는 에너지, 충돌에는 운동량, 장력에는 운동방정식을 씁니다.')+'</div>',
    'STANDALONE_CONCEPT_SUMMARY':summary,'DISTINCT_SUMMARY_VIDEO_SECTION_IF_NEEDED':roadmap,
    'EXAM_SECTION_TITLE':'충격량과 충돌을 설명하는 영어 답안',
    'BILINGUAL_GLOSSARY_TABLE':table(['영어(한국어)','의미와 사용'],[(f'{en}({ko})',escape(meaning)) for en,ko,meaning in terms]),
    'AUDIT_SECTION_TITLE':'원본 슬라이드·자동생성 스크립트 교정 기록',
    'ASR_CORRECTION_TABLE':p('원본 PDF와 영어 자동생성 자막은 수정하지 않았습니다. 이 표는 본문에 채택한 해석과 자료의 불일치를 기록합니다. 오표기가 실제 발화인지 자동인식 오류인지는 별도의 음성 판독 없이 단정하지 않습니다. 중요한 수식·조건 불일치는 해당 슬라이드 아래에도 명시했습니다.')+table(['위치','원문 또는 문제','본문 처리','근거'],audit),
    'SOURCE_LIST_AND_PROVENANCE_NOTE':'<ul class="plain-list"><li>원본 PDF: Lecture 7, MC2103, Fall 2026, 74장.</li>'+''.join(f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상</a> · 영어 자동생성 원문, 2026-10-06 확보.</li>' for label,vid in videos)+'<li>주차·날짜: 보존된 강의 인덱스, Week 06 · 2026-10-07.</li><li>골프 예시의 적용 대상 확인: <a href="https://www.usga.org/content/usga/home-page/articles/2025/05/what-happens-collision-between-club-ball.html" target="_blank" rel="noreferrer">USGA 공식 클럽–공 충돌 설명</a>.</li></ul>'+p('원본 74장의 이미지와 영어 자막 5편을 대조했습니다. 시간 표시는 관련 설명 구간으로 정확한 슬라이드 전환 시각을 뜻하지 않습니다. 원본 3장의 보조 링크는 보존하되 그 영상의 내용은 설명 근거로 사용하지 않았습니다. Overview의 앞부분은 확보된 자막에 완전하게 나타나지 않아 임의 복원하지 않았습니다.')+p('자동자막 원문은 별도 로컬 텍스트로 보존했습니다. 개념 요약은 원본·본강의·Summary의 실제 복습을 종합했으며, 다음 강의 안내는 분리했습니다. 생략된 대수, 일반 해, 에너지 손실식, 검산, 마지막 그룹 문제의 완성 풀이는 시험용 보강 또는 편집자 보강입니다. 그룹 문제 수치는 명시한 접촉 법선·구속 모델의 계산값이며 원본 공식 답이 아닙니다. 모든 수치 계산은 별도 언급이 없으면 g=9.81 m/s²를 사용했습니다.'),
    'TABLE_OF_CONTENTS_LINKS':''.join(f'<li><a href="#{id}">{label}</a></li>' for id,label in toc),
}
for key,value in values.items():
    template = template.replace('{{'+key+'}}',value)
template = template.replace('이 부분만 읽어도 렉처의 핵심 정의, 개념 관계, 가정과 풀이 흐름을 이해할 수 있도록 작성합니다.','충격량의 정의, 방향별 운동량 보존, 반발계수와 구속 충돌, 다섯 예제와 복합 문제를 연결한 독립형 요약입니다. 상세한 원본 슬라이드별 해설은 아래에서 별도로 이어집니다.')
template = re.sub(r'\s*<!--[\s\S]*?-->','',template)
template = '\n'.join(line.rstrip() for line in template.splitlines())+'\n'
assert not re.search(r'\{\{[^}]+\}\}',template)
(SITE/'lecture07.html').write_text(template,encoding='utf-8')
print(f'BUILT lecture07.html: {len(records)} source sections, {len(exam_items)} exam cards, {len(terms)} terms')
