"""Fill the fixed Lecture 1 template with source-reviewed Lecture 8 content."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT/'site'
records = []

def p(s):
    return s if s.startswith('<table') else '<p>'+s+'</p>'

def card(title,*body,kind='card'):
    return f'<div class="{kind}"><h3>{title}</h3>'+''.join(p(s) for s in body)+'</div>'

def table(head,rows):
    return '<table class="term-table"><thead><tr>'+''.join('<th>'+s+'</th>' for s in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+s+'</td>' for s in row)+'</tr>' for row in rows)+'</tbody></table>'

def add(n,title,evidence,*body,eq='',extra='',correction='',role='Concept'):
    assert n==len(records)+1,n
    blocks = card('원본 교정 · 적용 조건',correction,kind='callout') if correction else ''
    blocks += card('핵심 해설' if role=='Concept' else '슬라이드 안내',*body,kind='card' if role=='Concept' else 'quiet-card')
    if eq:
        blocks += card('식과 기호','<span class="formula">'+eq+'</span>')
    records.append((title,evidence,blocks+extra,role))

summary = ''.join([
    card('1. 여러 입자를 함께 보면 내부 상호작용과 전체 운동이 분리됩니다.',
        'System of particles(입자계)는 분석할 여러 particle(입자)를 하나의 system(계)으로 묶은 것입니다. 각 입자는 Fᵢ+Σⱼfᵢⱼ=mᵢaᵢ를 따릅니다. Fᵢ는 계 밖에서 오는 external force(외력), fᵢⱼ는 계 안의 입자 사이에 작용하는 internal force(내력)입니다. 같은 접촉력도 어디까지 계에 포함하느냐에 따라 분류가 바뀝니다.',
        '이 강의는 고정된 입자 집합과 constant masses(일정한 질량들), inertial/Newtonian frame(관성/뉴턴 기준계)을 사용합니다. 내력이 equal, opposite, and collinear(크기가 같고 반대 방향이며 동일 작용선상)인 쌍이면 전체 힘과 모멘트의 합에서 상쇄됩니다. 따라서 ΣFext=Σmᵢaᵢ, ΣMext,O=Σ(rᵢ×mᵢaᵢ)입니다. 이는 각 입자에 내력이 없다는 뜻은 아닙니다.',kind='callout'),
    card('2. Effective force(유효력)와 equipollent(합력·합모멘트가 같은)의 의미를 구별합니다.',
        'Effective force(유효력)는 mᵢaᵢ입니다. 이미 존재하는 접촉력·중력에 더해서 그려야 할 새 외력이 아닙니다. 각 입자의 모든 실제 힘의 합을 질량×가속도로 표현한 것입니다. 또한 부호가 반대인 inertia force(관성력) −mᵢaᵢ와 구별합니다.',
        '원본이 external-force system(외력계)과 effective-force system(유효력계)을 equipollent(합력과 합모멘트가 같은)하지만 generally not equivalent(일반적으로 개별 운동 효과까지 동등하지 않은)라고 구분하는 이유는 deformable system(변형 가능한 계)에서 각 입자가 다르게 움직일 수 있기 때문입니다. 전체 합을 안다고 내부 운동까지 모두 결정되는 것은 아닙니다.'),
    card('3. 총 선운동량은 전체 질량과 질량중심 속도의 곱입니다.',
        'Total mass(전체 질량) m=Σmᵢ, mass center(질량중심) G의 위치는 rG=Σmᵢrᵢ/m입니다. 질량으로 가중한 평균이므로 단순한 위치 평균과 다릅니다. 미분하면 vG=Σmᵢvᵢ/m, aG=Σmᵢaᵢ/m입니다. 따라서 linear momentum(선운동량) L=Σmᵢvᵢ=mvG, ΣFext=dL/dt=maG입니다.',
        'G는 전체 질량과 외력이 그 점에 집중된 것처럼 이동합니다. 다만 이 식은 G의 motion(운동)을 알려 줄 뿐 개별 입자의 relative motion(상대운동)을 없애지 않습니다. 힘의 합이 0이면 vG가 constant(일정)이지 반드시 0인 것은 아닙니다. 이 강의의 L은 선운동량, H는 angular momentum(각운동량) 표기입니다.'),
    card('4. 고정점과 질량중심의 각운동량 식은 기준점을 명시합니다.',
        'Fixed point(고정점) O에 대한 angular momentum(각운동량)은 HO=Σ(rᵢ×mᵢvᵢ)입니다. 여기서 rᵢ는 O에서 입자로 향하는 위치, vᵢ는 absolute velocity(절대속도)입니다. O가 관성 기준계에 고정되어 있으면 ΣMext,O=dHO/dt입니다. 곱을 미분할 때 drᵢ/dt×mᵢvᵢ=vᵢ×mᵢvᵢ=0이 됩니다.',
        '시험용 보강: HO=rG×mvG+HG로 나눌 수 있습니다. 첫 항은 질량중심 전체의 병진 운동이 O에 대해 만드는 각운동량, 둘째 항은 G 주변의 상대운동이 만드는 각운동량입니다. 일반적으로 움직이는 임의의 점에 고정점 공식을 그대로 쓰면 안 됩니다. G가 특별한 경우인 이유는 질량 가중 상대위치의 합이 0이기 때문입니다.'),
    card('5. 이번 강의의 프라임은 충돌 후가 아니라 상대량입니다.',
        'Centroidal frame(질량중심 기준계) Gx′y′z′는 G와 함께 translates without rotating(회전 없이 병진)하며 축 방향은 관성 기준계와 같습니다. rᵢ=rG+r′ᵢ, vᵢ=vG+v′ᵢ, aᵢ=aG+a′ᵢ입니다. 이번 ′ 표시는 relative quantity(상대량)이며 Lecture 7의 after-impact(충돌 후) 표기와 다릅니다.',
        '질량중심 정의로 Σmᵢr′ᵢ=0이고, 미분하면 Σmᵢv′ᵢ=0입니다. G가 가속하면 이 기준계는 noninertial(비관성)이지만 Σ(r′ᵢ×mᵢaG)=[Σmᵢr′ᵢ]×aG=0이므로 G에 대한 전체 모멘트 식에서는 병진 가속 항이 사라집니다. 회전하는 축까지 이 단순 관계를 확장하지 않습니다.'),
    card('6. G에 대한 각운동량은 절대속도와 상대속도로 같은 값입니다.',
        'HG=Σ(r′ᵢ×mᵢvᵢ), H′G=Σ(r′ᵢ×mᵢv′ᵢ)를 비교합니다. 차이는 [Σmᵢr′ᵢ]×vG=0이므로 HG=H′G입니다. 따라서 두 방식 중 계산하기 편한 것을 택할 수 있고, ΣMext,G=dHG/dt=dH′G/dt입니다.',
        '중요한 구분: HG 자체는 momentum(운동량)이고 ΣMG는 moment(모멘트)이므로 같지 않습니다. 원본 27장의 HG=H′G=ΣMG는 시간미분 기호가 빠진 식입니다. 본문에서는 HG=H′G와 dHG/dt=ΣMG를 별도로 씁니다.'),
    card('7. 선운동량·각운동량·에너지는 각각 다른 보존 조건을 가집니다.',
        'Linear momentum(선운동량)은 해당 방향의 resultant external force(외력 합력)가 0인 동안 보존됩니다. 유한 구간의 앞뒤만 비교하면 net external impulse(순외부 충격량)가 0인지 보면 됩니다. Angular momentum(각운동량)은 선택한 기준점에 대한 external moment(외력 모멘트) 또는 angular impulse(각충격량)를 확인합니다.',
        'Central force(중심력)는 O를 향하므로 O에 대한 모멘트가 0입니다. 합력이 0이 아니어도 HO는 보존될 수 있습니다. 반대로 서로 다른 작용선의 force couple(우력)은 합력이 0이어도 모멘트를 만들 수 있습니다. 따라서 L 보존을 근거로 H 또는 kinetic energy(운동에너지)까지 보존된다고 쓰면 안 됩니다. 우력 예시는 시험용 보강입니다.'),
    card('8. 전체 운동에너지는 질량중심 병진과 상대운동으로 나뉩니다.',
        'Kinetic energy(운동에너지)는 T=½Σmᵢvᵢ²입니다. vᵢ=vG+v′ᵢ를 대입하여 전개하면 T=½mvG²+½Σmᵢ(v′ᵢ)²가 됩니다. 교차항 vG·Σmᵢv′ᵢ가 0이기 때문입니다. 첫 항은 G의 translational motion(병진운동), 둘째 항은 G에 대한 relative motion(상대운동)의 에너지입니다.',
        '시험용 보강: 같은 질량 두 개가 서로 반대로 같은 속력으로 움직이면 L=0, vG=0이어도 T는 양수입니다. 계를 G의 한 입자로 바꿔 T=½mvG²만 쓰면 내부 운동 에너지를 놓칩니다. 일반적인 입자계의 상대운동은 rotation(회전)뿐 아니라 separation/deformation(분리/변형)도 포함합니다.'),
    card('9. 내력의 힘·모멘트 합은 0이어도 내력이 한 일은 남을 수 있습니다.',
        'Work–energy principle(일·에너지 원리)은 T₁+Uext+Uint=T₂입니다. Equal and opposite forces(크기가 같고 반대인 힘들) fᵢⱼ, fⱼᵢ의 일은 dU=fᵢⱼ·(drᵢ−drⱼ)이며 두 작용점의 displacement(변위)가 다르면 일반적으로 0이 아닙니다. 내부 스프링이 풀리는 상황이 대표적인 시험용 보강 예입니다.',
        'Conservative forces(보존력)의 일은 U=V₁−V₂=−ΔV로 바꿀 수 있습니다. 모든 일을 그렇게 처리할 수 있으면 T₁+V₁=T₂+V₂입니다. 위치에너지 V에는 필요한 내부 상호작용도 포함하며 중복 계산하지 않습니다. Ideal constraints(이상 구속)의 전체 일이 0이면 별도 에너지 항 없이 처리합니다.'),
    card('10. 두 가지 충격량 식은 전체 벡터합과 모멘트합을 연결합니다.',
        'Impulse–momentum principle(충격량·운동량 원리)은 L₁+∫ΣFext dt=L₂, HO,₁+∫ΣMext,O dt=HO,₂입니다. 외부 충격량이 작으면 보존식이 되지만, 각 입자의 속도는 내력에 의해 크게 달라질 수 있습니다. 평면에서는 x,y 선운동량 두 식과 z 각운동량 한 식을 얻습니다.',
        '미지수를 먼저 셉니다. 속력 둘이 미지수이고 방향을 알면 선운동량 두 식으로 충분할 수 있습니다. 방향도 모르는 속도는 성분 둘이 미지수입니다. 마지막 당구 문제는 네 미지수이므로 선운동량 두 식+각운동량+완전탄성 에너지 식을 사용합니다.'),
    card('11. 폭발과 당구공 예제는 성분 부호와 질량중심을 확인합니다.',
        '폭발 예제: 10 kg, 30 m/s가 2.5 kg의 위쪽 45° 파편 A와 7.5 kg의 아래쪽 30° 파편 B로 나뉩니다. 짧은 폭발 동안 중력 충격량을 무시하면 2.5vAcos45°+7.5vBcos30°=300, 2.5vAsin45°−7.5vBsin30°=0입니다. 재계산은 vA≈62.117 m/s, vB≈29.282 m/s이며 원본의 A 답 62.2 m/s와 작은 수치 차이가 있습니다. 폭발 에너지 방출이 있으므로 운동에너지 보존은 쓰지 않습니다.',
        '당구공 세 개 예제: 같은 질량이고 초기 A만 v₀=4 m/s로 움직입니다. B의 최종 y성분은 아래 방향이므로 음수입니다. 올바른 두 성분 식으로 vA≈2.131 m/s, vB≈2.342 m/s입니다. 전체 mass-center velocity(질량중심 속도)는 vG=v₀/3으로, 초기 진행 방향을 유지합니다. 속력 크기는 4/3 m/s이며 원본의 “같은 방향”은 “같은 속력”이 아닙니다.'),
    card('12. 움직이는 카트의 최고점에서는 공의 절대속도가 0이 아닙니다.',
        'Frictionless cart(마찰 없는 카트) A에 공 B가 길이 ℓ의 줄로 매달려 있습니다. 처음 A는 정지, B만 오른쪽으로 v₀입니다. 공이 첫 maximum elevation(최대 높이)에 도달하면 relative velocity(상대속도)가 0이 되어 vA,₂=vB,₂=V입니다. 수평 운동량 보존으로 V=mBv₀/(mA+mB)입니다.',
        '계 전체의 에너지 보존 ½mBv₀²=½(mA+mB)V²+mBgh를 쓰면 h=[mA/(mA+mB)]v₀²/(2g)입니다. 문제 53장은 v₀=√(2gℓ), 62장의 회고는 v₀²&lt;2gℓ로 다릅니다. 주 계산은 일반식 뒤 문제의 등호 조건을 대입하여 h=mAℓ/(mA+mB)&lt;ℓ로 정리합니다. 양의 유한 질량에서 공은 지지점보다 낮고, 최고점에도 계의 병진 운동에너지가 남습니다.'),
    card('13. 연속 탄성충돌은 경로의 모멘트팔까지 활용합니다.',
        '마지막 당구 문제에서 A는 위쪽, C는 오른쪽, B는 오른쪽 아래로 이동합니다. A의 위쪽 속력 a, B의 오른쪽·아래쪽 크기 bx,by, C의 속력 c를 쓰면 bx+c=3, a=by입니다. 좌하단 O에 대한 각운동량식은 −0.6(3)=2.4a−2.1by−0.9c이므로 a=by=3c−6입니다.',
        'Perfectly elastic collisions(완전탄성충돌들)이므로 a²+bx²+by²+c²=9입니다. 대입해 20c²−78c+72=0의 근 c=2.4와 1.5를 얻습니다. 후자는 a&lt;0으로 주어진 A의 위쪽 진행과 모순이므로 버립니다. 답은 vA=1.2j, vB=0.6i−1.2j, vC=2.4i m/s, |vB|≈1.342 m/s입니다. 모두 쿠션과 충돌하기 직전의 속도로, 쿠션 반발은 이 분석에 포함하지 않습니다.'),
])

add(1,'Lecture 8 · 입자계의 운동','강의 인덱스 · Week 07 · 2026-10-14',
    'Systems of Particles(입자계)를 다룹니다. 여러 입자의 전체 운동과 내부 상대운동을 구분하고, mass center(질량중심)·momentum(운동량)·energy(에너지)의 관계를 연결합니다.',role='Title')
add(2,'Lecture 8-1 · 도입','Overview 00:17–00:51',
    'Overview(도입 영상)는 pool balls(당구공들)의 충돌과 여러 cart(차량)가 연결된 roller coaster(롤러코스터)를 예로 듭니다. 한 물체의 식을 여러 물체의 system(계)으로 확장해야 하는 동기를 보여 주는 구분 페이지입니다.',role='Divider')
add(3,'원본 보조 영상 링크','원본 PDF 링크 페이지',
    '원본의 <a href="https://youtu.be/VmifDvvlawk" target="_blank" rel="noreferrer">보조 영상 링크</a>를 보존합니다. 강의 인덱스의 본강의 5편과 별도이며, 이 보조 영상의 내용은 본문 설명 근거에 포함하지 않았습니다.',role='Video link')
add(4,'Lecture 8-2 · 외력과 전체 운동량','Contents 1',
    'Effective force(유효력), internal/external force(내력/외력)의 합, linear/angular momentum(선/각운동량)을 정의하는 본강의 구분 페이지입니다.',role='Divider')
add(5,'입자계의 원리는 강체와 유체 해석의 기초입니다.','Contents 1 00:17–00:29',
    '하나의 particle(입자)은 크기·모양을 무시하지만 system of particles(입자계)는 여러 입자의 위치와 운동을 함께 다룹니다. 이 입자들 사이의 거리가 고정되면 rigid body(강체)로 이어지고, 상대위치가 바뀌는 모델은 fluid dynamics(유체역학) 등으로 확장될 수 있습니다.',
    '편집자 보강: 로켓 사진은 응용의 동기입니다. 이번 유도는 고정된 입자 집합과 constant mass(일정 질량)를 전제로 합니다. 연료가 경계를 드나드는 control volume(검사체적)에 같은 식을 그대로 쓰려면 질량·운동량 유출입을 별도로 고려해야 합니다.')
add(6,'유효력은 질량과 가속도의 곱입니다.','Contents 1 00:33–01:02',
    'Effective force(유효력)는 입자 i의 mᵢaᵢ입니다. 실제 힘들의 resultant(합력)와 같은 값을 갖는 동역학적 표현으로, 중력이나 접촉력처럼 새롭게 추가되는 힘이 아닙니다.',
    '전체 external-force system(외력계)은 각 입자에 놓인 effective forces(유효력들)의 계와 같은 resultant force and moment(합력과 합모멘트)를 갖게 됩니다. 뒤에서 이 관계를 equipollent(합력·합모멘트가 같은)라고 부릅니다.',eq='Effective force(유효력) = mᵢaᵢ')
add(7,'질량중심과 에너지·충격량 원리를 함께 사용합니다.','Contents 1 01:05–01:23',
    'Mass center(질량중심)는 전체 질량의 평균 위치를 나타내며, 이 점의 운동으로 계의 전체 병진운동을 설명합니다. 이후 work–energy(일·에너지)와 impulse–momentum(충격량·운동량) 원리를 입자계에 적용합니다.',
    'Rigidly connected particles(강하게 연결되어 상대거리가 고정된 입자들)에도 이 결과가 적용되므로 다음 강체 단원의 기반이 됩니다. 다만 전체 운동만으로 각 입자의 상대운동이 자동으로 정해지는 것은 아닙니다.')
add(8,'각 입자에는 외력과 내력을 모두 넣습니다.','Contents 1 01:25–02:16',
    '입자 Pᵢ에 작용하는 external resultant(외력 합력)를 Fᵢ, 다른 입자 j가 i에 가하는 internal force(내력)를 fᵢⱼ라 둡니다. 각 입자에는 Fᵢ+Σⱼfᵢⱼ=mᵢaᵢ를 씁니다. 자신의 힘 fᵢᵢ는 0으로 처리합니다.',
    'Fixed point(고정점) O에서 Pᵢ까지의 rᵢ를 양변에 cross product(벡터곱)하면 rᵢ×Fᵢ+Σⱼ(rᵢ×fᵢⱼ)=rᵢ×mᵢaᵢ입니다. 입자 위치를 바꾸거나 내력을 미리 지우지 않습니다.',
    correction='원본 우측 범례의 mᵢaᵢ = external force는 앞 장 정의와 맞지 않습니다. mᵢaᵢ는 effective force(유효력)이며 그 입자의 외력과 내력의 합입니다.',eq='Fᵢ + Σⱼfᵢⱼ = mᵢaᵢ')
add(9,'입자별 동등 관계를 전체 합으로 확장합니다.','Contents 1 02:20–02:37',
    '한 particle(입자)에 작용하는 모든 실제 힘의 합은 그 자리의 effective force(유효력)와 같습니다. 이를 모든 입자에 각각 적용하면 external+internal force system(외력+내력계)과 effective-force system(유효력계)이 입자별로 대응합니다.',
    '여기서는 internal forces(내력들)를 아직 버리지 않았습니다. 다음 단계에서 전체 합만 취한 뒤 내부 작용·반작용을 제거하면 개별 정보는 줄어들지만 전체 운동량을 다루는 간단한 식을 얻게 됩니다.')
add(10,'전체 합에서 내력은 이중 합으로 나타납니다.','Contents 1 02:41–02:49',
    '바깥 Σᵢ는 system(계)에 포함된 모든 입자를 더하고, 안쪽 Σⱼ는 입자 i에 작용하는 internal forces(내력들)를 더합니다. 따라서 힘 식은 ΣᵢFᵢ+ΣᵢΣⱼfᵢⱼ=Σᵢmᵢaᵢ입니다.',
    'Moment equation(모멘트 식)도 같은 방식으로 더합니다. 이중 합에는 fᵢⱼ와 fⱼᵢ가 함께 들어갑니다. 각 항을 무조건 0이라 두는 것이 아니라 쌍으로 합쳤을 때 상쇄되는지 확인하는 과정입니다.')
add(11,'내력의 합력과 합모멘트는 쌍별로 상쇄됩니다.','Contents 1 02:55–06:05',
    'Newton’s third law(뉴턴 제3법칙)의 equal and opposite(크기가 같고 반대 방향인) 쌍에 대해 fⱼᵢ=−fᵢⱼ이므로 합력은 0입니다. 모멘트 합은 rᵢ×fᵢⱼ+rⱼ×fⱼᵢ=(rᵢ−rⱼ)×fᵢⱼ입니다.',
    '이 강의에서는 두 입자의 내력이 collinear(동일 작용선상)이며 두 입자를 잇는 방향이므로 위 벡터곱도 0입니다. Equal and opposite(같고 반대)만으로 떨어진 작용점의 모멘트까지 0이라고 결론 내릴 수는 없고, 동일 작용선 조건이 필요합니다.',eq='ΣFext = Σmᵢaᵢ<br>ΣMext,O = Σ(rᵢ×mᵢaᵢ)')
add(12,'합력과 합모멘트가 같다고 내부 운동까지 같지는 않습니다.','Contents 1 06:08–06:30',
    'Equipollent systems(합력과 합모멘트가 같은 계들)은 전체 force resultant(합력)와 moment resultant(합모멘트)가 같습니다. 원본 그림처럼 동일 작용선을 따라 힘의 작용점을 A에서 B로 옮기면 전체 합력·모멘트는 같게 만들 수 있습니다.',
    '하지만 연결이 변형 가능한 system of particles(입자계)에서는 어느 입자가 직접 힘을 받는지가 relative motion(상대운동)에 영향을 줍니다. 원본의 not equivalent(동등하지 않음)는 이러한 개별 운동 효과까지 같다는 보장은 없다는 뜻입니다. 강체에서 익숙한 힘의 작용선 이동을 임의의 입자계 전체에 적용하지 않습니다.',
    correction='원본의 “equipollent by not equivalent”는 문맥상 “equipollent but not equivalent”로 읽습니다. 자막의 equivalent 반복은 두 다른 용어의 구별을 잃으므로 정의와 원본의 두 용어를 기준으로 설명합니다.')
add(13,'선운동량은 입자 운동량의 벡터합입니다.','Contents 1 06:33–07:00',
    'Linear momentum(선운동량) L=Σmᵢvᵢ입니다. 각 vᵢ는 같은 inertial frame(관성 기준계)에서 측정한 velocity vector(속도벡터)입니다. 단순한 speed sum(속력 합)이 아니므로 반대 방향은 서로 상쇄될 수 있습니다.',
    '각 mass(질량)가 constant(일정)이면 dL/dt=Σmᵢdvᵢ/dt=Σmᵢaᵢ입니다. 단위는 L이 kg·m/s, 그 시간미분은 N입니다. 원본의 L은 길이가 아니라 선운동량 기호입니다.',eq='L = Σmᵢvᵢ; dL/dt = Σmᵢaᵢ')
add(14,'총 선운동량의 변화율은 외력의 합력입니다.','Contents 1 07:03–07:12',
    '앞 장의 dL/dt=Σmᵢaᵢ와 내력을 상쇄한 ΣFext=Σmᵢaᵢ를 결합하면 ΣFext=dL/dt입니다. Internal forces(내력들)는 개별 입자의 운동량을 바꾸지만 전체 합에서는 서로 전달하는 만큼 상쇄됩니다.',
    '시험용 보강: 수평 외력만 0이면 Lx만 constant(일정)입니다. 다른 방향의 중력이나 지지력이 남아 있어도 수평 성분은 따로 보존될 수 있습니다. “외력이 존재한다”와 “외력 합력의 특정 성분이 0이 아니다”를 구별합니다.',eq='ΣFext = dL/dt')
add(15,'고정점 각운동량을 미분하면 하나의 항이 사라집니다.','Contents 1 07:19–09:03',
    'Fixed point(고정점) O에 대한 angular momentum(각운동량)은 HO=Σ(rᵢ×mᵢvᵢ)입니다. rᵢ와 vᵢ 모두 변하므로 product rule(곱의 미분법)로 두 항을 얻습니다.',
    'O가 관성 기준계에 고정되어 drᵢ/dt=vᵢ입니다. 따라서 Σ(vᵢ×mᵢvᵢ)=0이고 dHO/dt=Σ(rᵢ×mᵢaᵢ)만 남습니다. 자기 자신과 평행한 벡터의 cross product(벡터곱)가 0이라는 성질을 사용한 것입니다.',eq='HO = Σ(rᵢ×mᵢvᵢ)<br>dHO/dt = Σ(vᵢ×mᵢvᵢ)+Σ(rᵢ×mᵢaᵢ) = Σ(rᵢ×mᵢaᵢ)')
add(16,'고정점 각운동량을 바꾸는 것은 그 점에 대한 외력 모멘트입니다.','Contents 1 09:06–09:17',
    '내부 moment(모멘트)가 쌍별로 상쇄되므로 ΣMext,O=dHO/dt입니다. 같은 O를 사용하여 각운동량과 모멘트를 계산해야 합니다. 힘의 합만 보고 각운동량 보존을 판단하지 않습니다.',
    '시험용 보강: 평면 운동에서는 HO,z=Σmᵢ(xᵢvᵢy−yᵢvᵢx)입니다. Counterclockwise(반시계) 방향을 양으로 정하면 각 항의 부호를 일관되게 계산할 수 있습니다. Angular momentum(각운동량)의 단위 kg·m²/s와 torque(토크)의 단위 N·m는 시간 차원이 다릅니다.',eq='ΣMext,O = dHO/dt')
add(17,'Lecture 8-3 · 질량중심과 에너지','Contents 2',
    'Mass center(질량중심)의 운동, 그 점에 대한 angular momentum(각운동량), energy(에너지) 분해와 보존 원리를 다루는 구분 페이지입니다.',role='Divider')
add(18,'질량중심은 질량으로 가중한 위치의 평균입니다.','Contents 2 00:17–01:40',
    '전체 질량 m=Σmᵢ에 대해 mrG=Σmᵢrᵢ로 mass center(질량중심) G를 정의합니다. 원본은 r̄라는 막대 표기를 쓰며, 본문 rG와 같은 의미입니다. 성분별로 xG=Σmᵢxᵢ/m, yG=Σmᵢyᵢ/m, zG=Σmᵢzᵢ/m입니다.',
    'Relative position(상대위치) r′ᵢ=rᵢ−rG를 질량으로 가중하여 합하면 Σmᵢr′ᵢ=0입니다. 이후 여러 미분·에너지 식에서 항을 없애는 핵심 정체성입니다. 시험용 보강: center of gravity(무게중심)와 질량중심은 uniform gravitational field(균일 중력장)에서 일치하며 항상 같은 개념인 것은 아닙니다.',eq='rG = (Σmᵢrᵢ)/m; Σmᵢr′ᵢ = 0')
add(19,'정의를 두 번 미분하면 질량중심의 운동방정식이 됩니다.','Contents 2 01:50–03:11',
    '고정된 입자 집합과 constant masses(일정한 질량들)에서 mrG=Σmᵢrᵢ를 미분하면 mvG=Σmᵢvᵢ=L입니다. 다시 미분하면 maG=dL/dt=ΣFext입니다.',
    '질량중심은 단순히 그림의 한 점이 아니라 total momentum(총운동량)을 하나의 속도로 표현하는 위치입니다. Σmᵢv′ᵢ=0도 앞의 Σmᵢr′ᵢ=0을 시간미분한 결과입니다. 질량이 변화하거나 분석 대상 입자가 바뀌는 경우에는 이 미분에 추가 항이 필요합니다.',eq='L = mvG; ΣFext = maG; Σmᵢv′ᵢ = 0')
add(20,'질량중심의 병진운동과 계 내부 운동은 다릅니다.','Contents 2 03:14–03:22',
    'Mass center(질량중심)는 entire mass(전체 질량)와 all external forces(모든 외력)가 그 점에 집중된 것처럼 이동합니다. 따라서 전체 병진 운동을 구할 때 각 internal force(내력)를 일일이 구하지 않아도 됩니다.',
    '시험용 보강: 같은 질량 두 입자가 스프링에 밀려 반대 방향으로 멀어지면 각 속도는 변해도 외력 합력이 0인 G의 속도는 일정합니다. “G의 운동이 같다”는 말은 각 입자 위치·계의 모양·내부 에너지까지 같다는 말이 아닙니다.')

add(21,'질량중심 좌표계는 회전하지 않고 함께 이동합니다.','Contents 2 03:24–06:00',
    'Centroidal frame(질량중심 기준계) Gx′y′z′는 원점만 G를 따라 이동하고 축은 Newtonian frame(뉴턴 기준계) Oxyz와 평행하게 유지됩니다. Translation(병진)만 하므로 rᵢ=rG+r′ᵢ, vᵢ=vG+v′ᵢ, aᵢ=aG+a′ᵢ입니다.',
    'G가 acceleration(가속도)을 가지면 이 기준계는 generally non-Newtonian(일반적으로 비뉴턴·비관성)입니다. 상대속도·상대가속도를 쓸 수 있다는 사실과 관성 기준계라는 판정은 다릅니다. 여기서 prime(프라임) ′은 G에 대한 relative quantity(상대량)이며, 앞 렉처의 “충돌 후” 표시와 다릅니다.',
    extra=card('시험용 보강 · 회전 좌표계로 확장하지 않습니다.','축까지 rotating(회전)하면 vᵢ=vG+v′ᵢ에 회전 운동 항이 필요합니다. 이번 유도는 축 방향이 고정된 translating frame(병진 기준계)이므로 그 항이 없습니다. 그림의 x′,y′,z′ 방향이 x,y,z와 나란한 이유입니다.'))
add(22,'상대속도로 계산한 G 기준 각운동량을 먼저 정의합니다.','Contents 2 06:05–07:55',
    'H′G=Σ(r′ᵢ×mᵢv′ᵢ)로 정의합니다. Position vector(위치벡터)와 velocity vector(속도벡터) 모두 G 기준의 relative quantities(상대량들)입니다. 원본은 나중에 절대속도로 계산한 HG와 비교하기 위해 H′G를 따로 표기합니다.',
    'Absolute velocity(절대속도)로 계산한 HG=Σ(r′ᵢ×mᵢvᵢ)에서도 위치는 여전히 G에서 입자로 향하는 r′ᵢ입니다. 기준점과 속도를 측정하는 기준계를 서로 다른 선택으로 구분해야 합니다.',
    correction='Contents 2 06:39–06:45 자막은 v′ᵢ도 relative position vector라고 부릅니다. 수식상 v′ᵢ는 relative velocity(상대속도)이며 단위는 m/s입니다.',eq='H′G = Σ(r′ᵢ×mᵢv′ᵢ); HG = Σ(r′ᵢ×mᵢvᵢ)')
add(23,'질량중심의 가속 항은 가중 상대위치 합 때문에 사라집니다.','Contents 2 07:57–12:51',
    'H′G를 미분하면 Σ[v′ᵢ×mᵢv′ᵢ+r′ᵢ×mᵢa′ᵢ]입니다. 첫 벡터곱은 0이고 a′ᵢ=aᵢ−aG를 대입하면 dH′G/dt=Σ(r′ᵢ×mᵢaᵢ)−[Σmᵢr′ᵢ]×aG가 됩니다.',
    'aG는 모든 입자에게 공통이므로 합 밖으로 꺼낼 수 있습니다. 이는 index i(입자 번호)에 무관하다는 뜻이지 time(시간)에 대해 constant(일정)이라는 뜻이 아닙니다. 대괄호는 질량중심 정의로 0입니다.',
    '마지막으로 각 입자의 mᵢaᵢ=Fᵢ+Σⱼfᵢⱼ를 넣고 전체 내부 모멘트를 쌍별 상쇄하면 dH′G/dt=ΣMext,G입니다. 원본의 짧은 등호 사이에는 이 상쇄 과정이 생략되어 있습니다. 각 입자에서 mᵢaᵢ=Fᵢ라고 외력만 남기는 것은 일반적으로 틀립니다.',
    correction='원본 유도 중 상대위치의 프라임과 입자 첨자가 일관되지 않은 항은 r′ᵢ로 통일합니다. 자막 10:59의 “a bar is constant”는 뒤의 11:23–11:38처럼 i에 무관하다는 뜻으로 해석합니다.',eq='dH′G/dt = Σ(r′ᵢ×mᵢaᵢ)−(Σmᵢr′ᵢ)×aG = ΣMext,G')
add(24,'G가 가속해도 G 기준 전체 모멘트 식은 성립합니다.','Contents 2 12:55–13:05',
    'Moment resultant(합모멘트) ΣMext,G는 mass center(질량중심)에 대한 angular momentum(각운동량)의 시간 변화율입니다. 앞 장에서 G의 병진 가속이 만든 항이 0이 되는 것을 보였으므로 G가 inertial(관성)일 필요는 없습니다.',
    '시험용 보강: 이것은 임의의 accelerating point(가속하는 점)에 자동으로 성립하는 식이 아닙니다. G에는 Σmᵢr′ᵢ=0이라는 특별한 성질이 있습니다. 기준점을 정한 뒤 그 점이 fixed point(고정점)인지 mass center(질량중심)인지 먼저 확인합니다.',eq='ΣMext,G = dH′G/dt')
add(25,'절대속도는 기준계 이동 속도와 상대속도의 합입니다.','Contents 2 13:22–14:16',
    '입자 Pᵢ의 absolute velocity(절대속도) vᵢ는 mass-center velocity(질량중심 속도) vG와 relative velocity(상대속도) v′ᵢ의 vector sum(벡터합)입니다. 원본의 v̄는 vG와 같은 표기입니다.',
    'vG는 모든 입자에 공통인 병진 성분이고 v′ᵢ는 입자마다 다릅니다. 두 벡터가 꼭 나란하지 않으므로 speed(속력) 크기를 단순히 더하지 않습니다. 그림의 벡터 삼각형은 크기와 방향을 함께 더하는 관계를 보여 줍니다.',eq='vᵢ = vG+v′ᵢ')
add(26,'상대운동만으로 계산한 각운동량을 다시 확인합니다.','Contents 2 14:23–14:42',
    'H′G=Σ(r′ᵢ×mᵢv′ᵢ)는 입자들의 motion relative to G(질량중심에 대한 상대운동)를 사용합니다. 이 양에는 계 전체가 공간을 이동하는 공통 속도 vG를 직접 넣지 않습니다.',
    '상대속도가 모두 0인 pure translation(순수 병진)에서는 H′G=0입니다. 반면 G가 정지한 상태에서도 입자들이 주변을 움직이면 H′G가 0이 아닐 수 있습니다. 다음 장은 절대속도로 계산해도 같은 결과인지 증명합니다.')
add(27,'HG와 H′G는 같지만 모멘트는 그 시간미분입니다.','Contents 2 14:45–16:19',
    'HG=Σ[r′ᵢ×mᵢ(vG+v′ᵢ)]를 전개하면 [Σmᵢr′ᵢ]×vG+Σ(r′ᵢ×mᵢv′ᵢ)입니다. 앞 항이 0이므로 HG=H′G입니다. 두 정의의 차이가 질량중심 성질 때문에 사라집니다.',
    '그러므로 앞서 얻은 ΣMext,G=dH′G/dt를 ΣMext,G=dHG/dt로도 쓸 수 있습니다. Momentum(운동량)과 its rate of change(그 변화율)를 분리해서 적어야 단위도 일치합니다.',
    correction='원본 마지막의 HG=H′G=ΣMG는 각운동량과 모멘트를 직접 같다고 놓아 차원이 맞지 않습니다. 올바른 관계는 HG=H′G, dHG/dt=dH′G/dt=ΣMG입니다. 전개 마지막 합의 속도도 상대속도 v′ᵢ로 써야 앞뒤 유도가 이어집니다.',eq='HG = H′G<br>dHG/dt = dH′G/dt = ΣMext,G')
add(28,'같은 G 기준에서 계산이 편한 속도를 선택할 수 있습니다.','Contents 2 16:22–16:36',
    '입자의 momentum(운동량)을 absolute velocity(절대속도)로 계산하거나 centroidal relative velocity(질량중심 상대속도)로 계산해도 G에 대한 전체 angular momentum(각운동량)은 같습니다. 두 경우 모두 lever arm(모멘트팔)의 기준은 G입니다.',
    '시험용 보강: rᵢ=rG+r′ᵢ, vᵢ=vG+v′ᵢ를 HO에 대입하면 HO=rG×mvG+HG입니다. Σmᵢr′ᵢ와 Σmᵢv′ᵢ가 0이라 교차항이 사라집니다. 이 분해는 “기준점 O에 대한 계 전체 이동”과 “G 주변 상대운동”을 연결해 줍니다.',eq='시험용 보강: HO = rG×mvG+HG')
add(29,'외력과 외력 모멘트가 없으면 두 운동량이 보존됩니다.','Contents 2 16:43–17:02',
    'No external forces(외력이 없음)는 ΣFext=0과 ΣMext,O=0을 함께 보장하는 충분한 조건입니다. 이때 dL/dt=0, dHO/dt=0이므로 L과 HO가 각각 constant(일정)입니다.',
    '더 일반적으로는 개별 외력이 모두 0일 필요 없이 해당 합력·합모멘트가 0이면 됩니다. 단, 합력 0만으로 합모멘트 0이 따라오지는 않습니다. 각각의 conservation condition(보존 조건)을 별도로 확인합니다.')
add(30,'중심력은 선운동량을 바꾸어도 각운동량을 보존할 수 있습니다.','Contents 2 17:10–17:46',
    'Central force(중심력)의 작용선이 고정점 O를 지나면 r×F=0입니다. 외력 합력이 0이 아니어서 linear momentum(선운동량)이 바뀌더라도 O에 대한 angular momentum(각운동량)은 보존될 수 있습니다.',
    '자막의 “external forces exist → linear momentum is not conserved”는 너무 넓게 읽으면 안 됩니다. 필요한 조건은 resultant external force(외력 합력)가 0이 아닌가입니다. 서로 상쇄되는 여러 외력이 존재할 수도 있습니다.',eq='ΣFext ≠ 0 → dL/dt ≠ 0<br>ΣMext,O = 0 → HO = constant(일정)')
add(31,'질량중심 속도와 G 기준 각운동량도 조건별로 보존됩니다.','Contents 2 17:57–18:02',
    'ΣFext=0이면 L=mvG가 일정하므로 constant mass(일정 질량) 계의 vG가 일정합니다. ΣMext,G=0이면 HG가 일정합니다. 이 두 문장은 서로 다른 조건에서 각각 성립합니다.',
    '시험용 보강: initial total momentum(초기 총운동량)이 0일 때에만 외력 합력 0인 G가 계속 정지합니다. 당구공 하나가 이미 움직이는 예제에서는 총운동량이 0이 아니므로 충돌 뒤에도 G는 일정한 속도로 이동합니다.')
add(32,'입자계의 운동에너지는 각 입자의 에너지를 더합니다.','Contents 2 18:05–18:19',
    'Kinetic energy(운동에너지)는 scalar(스칼라)이며 T=½Σmᵢ(vᵢ·vᵢ)=½Σmᵢvᵢ²입니다. 반대 방향으로 움직이는 두 입자도 양의 에너지를 각각 더합니다. Vector momentum(벡터 운동량)의 상쇄와 다릅니다.',
    '원본의 vᵢ=vG+v′ᵢ를 이용하면 동일한 에너지를 centroidal frame(질량중심 기준계)의 상대운동으로 다시 표현할 수 있습니다. 단순히 vᵢ를 vG로 바꾸는 것이 아니라 제곱을 전개해야 합니다.')
add(33,'교차항이 0이 되어 에너지가 두 부분으로 분해됩니다.','Contents 2 18:21–20:24',
    'T=½Σmᵢ(vG+v′ᵢ)·(vG+v′ᵢ)를 전개하면 ½mvG²+vG·Σmᵢv′ᵢ+½Σmᵢ(v′ᵢ)²입니다. 질량중심 상대위치 합을 미분하여 얻은 Σmᵢv′ᵢ=0 때문에 middle term(가운데 항)이 없어집니다.',
    '남은 두 항은 translation of G(질량중심 병진)와 motion relative to G(질량중심에 대한 상대운동)의 kinetic energy(운동에너지)입니다. 상대운동 항은 항상 0 이상이므로 T≥½mvG²이며 모든 상대속도가 0일 때만 등호입니다.',
    extra=card('시험용 보강 · 총운동량 0인데 운동에너지는 양수인 예',
        '같은 질량 q의 두 입자가 속도 +u와 −u로 움직이면 L=q u−q u=0, vG=0입니다. 하지만 T=½qu²+½qu²=qu²입니다. 질량중심만 정지했을 뿐 입자들은 움직이므로 전체 운동에너지는 0이 아닙니다.'),eq='T = ½mvG² + ½Σmᵢ(v′ᵢ)²')
add(34,'입자 하나의 일에는 내력과 외력이 모두 포함됩니다.','Contents 2 20:27–21:03',
    '각 particle(입자) Pᵢ에 대해 (T₁)ᵢ+(U₁→₂)ᵢ=(T₂)ᵢ입니다. 여기서 work(일)는 그 입자에 작용하는 external resultant(외력 합력)와 internal forces(내력들)가 실제 작용점 변위에 대해 한 일을 모두 포함합니다.',
    'Momentum equation(운동량 식)에서 내력 합이 없어졌다는 사실을 work equation(일의 식)에 바로 적용하면 안 됩니다. 힘은 벡터합으로 더하지만 일은 각 작용점의 다른 displacement(변위)와 dot product(내적)를 취하기 때문입니다.')
add(35,'내력의 일은 상대변위 때문에 상쇄되지 않을 수 있습니다.','Contents 2 21:05–21:35',
    '계 전체에는 T₁+Uext+Uint=T₂를 씁니다. fⱼᵢ=−fᵢⱼ인 한 쌍의 미소 일은 fᵢⱼ·drᵢ+fⱼᵢ·drⱼ=fᵢⱼ·(drᵢ−drⱼ)입니다. 작용점의 relative displacement(상대변위)가 남으므로 일반적으로 0이 아닙니다.',
    '시험용 보강: 내부 spring(스프링)이 팽창하며 두 입자를 밀면 같은 크기·반대 방향의 힘이 각 입자의 이동 방향으로 일을 할 수 있습니다. 전체 운동량은 그대로여도 kinetic energy(운동에너지)는 증가하며 스프링의 potential energy(위치에너지)가 감소합니다.',eq='dUint = fᵢⱼ·(drᵢ−drⱼ)')
add(36,'보존력의 일은 위치에너지 감소량으로 바꿉니다.','Contents 2 21:38–21:48',
    'Conservative force(보존력)의 work(일)는 U₁→₂=V₁−V₂입니다. 계에 한 일을 모두 보존력의 일로 표현할 수 있거나 남은 힘들의 순일이 0이면 T₁+V₁=T₂+V₂이며 mechanical energy(역학적 에너지)가 보존됩니다. 보존력이 하나 존재한다는 이유만으로 이 보존식이 성립하지는 않습니다.',
    'Internal conservative interaction(내부 보존 상호작용)의 위치에너지도 V에 포함할 수 있습니다. 이미 V로 옮긴 스프링의 일을 U에 다시 더하지 않습니다. 시험용 보강: nonconservative work(비보존 일)가 남으면 T₁+V₁+Unc=T₂+V₂로 확장하며, 질량중심의 운동에너지만이 아니라 전체 T를 사용합니다.',
    correction='원본의 “change in potential energy”는 일을 +ΔV로 대체하라는 뜻이 아닙니다. 보존력이 한 일은 위치에너지 감소량 −ΔV입니다.',eq='Uconservative = −ΔV = V₁−V₂<br>T₁+V₁ = T₂+V₂ (Unc=0)')
add(37,'힘과 모멘트를 시간 적분하면 두 충격량 관계가 됩니다.','Contents 2 21:50–22:03',
    'ΣFext=dL/dt를 t₁에서 t₂까지 적분하면 L₁+∫ΣFext dt=L₂입니다. Fixed point(고정점) O에 대해 ΣMext,O=dHO/dt를 적분하면 HO,₁+∫ΣMext,O dt=HO,₂입니다.',
    'Linear impulse(선충격량)의 단위는 N·s, angular impulse(각충격량)는 N·m·s입니다. 외부 충격량이 negligible(무시 가능)이면 앞뒤 운동량이 같습니다. 순간의 force(힘)가 작다는 말과 전체 시간 적분이 작다는 말을 구별합니다.',eq='L₁+∫ΣFext dt = L₂<br>HO,₁+∫ΣMext,O dt = HO,₂')
add(38,'벡터계 그림은 운동량 합과 그 모멘트 합을 함께 표현합니다.','Contents 2 22:03–22:45',
    '원본은 initial particle momenta(초기 입자 운동량들)에 external impulses(외부 충격량들)를 더한 벡터계와 final particle momenta(최종 입자 운동량들)의 벡터계가 equipollent(합과 합모멘트가 같은)라고 설명합니다.',
    '그림의 O에 놓인 resultant impulse(합충격량)뿐 아니라 angular impulse(각충격량)도 필요합니다. 하나의 합벡터만 맞추면 각운동량 정보가 빠질 수 있습니다. 입자별 최종 속도를 결정하려면 주어진 방향·구속·에너지 조건을 추가해야 합니다.')
add(39,'Lecture 8-4 · 입자계 예제 풀이','Problem Solving',
    '폭발 파편, 세 당구공의 충돌, 움직이는 카트의 진자, 연속 탄성충돌을 다룹니다. 각 문제에서 system(계), component(성분), reference point(기준점), conservation condition(보존 조건)을 먼저 정합니다.',role='Divider')

add(40,'예제 1 · 폭발 뒤 두 파편의 속도','Problem Solving 00:18–01:24',
    '10 kg projectile(발사체)이 오른쪽 30 m/s로 이동하다가 A 2.5 kg, B 7.5 kg의 fragments(파편들)로 나뉩니다. Immediately after the explosion(폭발 직후) A는 위쪽 45°, B는 아래쪽 30°로 이동합니다. 방향은 주어졌으므로 미지수는 speed(속력) vA,vB 두 개입니다.',
    '오른쪽 +x, 위쪽 +y를 정하면 vA=(vAcos45°,vAsin45°), vB=(vBcos30°,−vBsin30°)입니다. B가 아래로 움직인다는 사실은 angle magnitude(각도의 크기)가 양수여도 y성분의 부호가 음수라는 뜻입니다.')
add(41,'예제 1 · 짧은 폭발 동안 외부 충격량을 무시합니다.','Problem Solving 01:26–02:03',
    'System(계)은 폭발 전 발사체를 구성하던 모든 물질, 폭발 후 두 파편 전체입니다. Explosion forces(폭발력)는 이 계 내부의 상호작용이고, 매우 짧은 폭발 구간에서는 weight impulse(중량 충격량)를 무시합니다. 따라서 전체 linear momentum(선운동량)이 거의 보존됩니다.',
    '원본과 자막의 “no external forces”는 실제 중력이 사라진다는 뜻으로 읽지 않습니다. 엄밀히는 해당 짧은 시간의 external impulse(외부 충격량)가 negligible(무시 가능)하다는 근사입니다. 폭발 뒤 긴 비행 구간에는 중력을 다시 고려해야 합니다.')
add(42,'예제 1 · 폭발 전 한 벡터와 폭발 후 두 벡터를 비교합니다.','Problem Solving 02:05–02:48',
    'Initial total momentum(초기 총운동량)은 (10)(30)i=300i kg·m/s입니다. 폭발 후에는 mAvA+mBvB이며 각각의 momentum vector(운동량벡터)를 더하면 같은 300i가 되어야 합니다.',
    '수평 성분은 두 파편 모두 오른쪽이어서 더해집니다. 수직 성분은 위·아래가 상쇄되어 0입니다. 이 두 관찰만으로도 원본 수직 식의 두 양의 항을 그대로 더하면 잘못된다는 점을 확인할 수 있습니다.')
add(43,'예제 1 · 질량을 포함한 벡터 보존식을 세웁니다.','Problem Solving 02:51–03:18',
    'mAvA+mBvB=mv₀에서 질량이 서로 다르므로 약분해 없애지 않습니다. 대입하면 2.5vA+7.5vB=10v₀이며 여기서 각 v는 vector(벡터)입니다.',
    '다음 장에서 두 Cartesian components(직교좌표 성분들)로 나누면 scalar equations(스칼라 방정식들) 두 개가 됩니다. Direction(방향)이 이미 주어졌기에 추가 restitution relation(반발 관계)이나 에너지식 없이 두 미지 속력을 구할 수 있습니다.',eq='2.5<b>v</b>A+7.5<b>v</b>B = 300<b>i</b>')
add(44,'예제 1 · 아래쪽 파편의 수직 성분에는 음수를 붙입니다.','Problem Solving 03:22–04:01',
    'x방향: 2.5vAcos45°+7.5vBcos30°=300입니다. y방향: 2.5vAsin45°−7.5vBsin30°=0입니다. 두 속력은 그림의 화살표 방향을 따르는 nonnegative magnitudes(0 이상 크기)로 정의했습니다.',
    'y식으로 vA=[7.5sin30°/(2.5sin45°)]vB=2.121320vB를 얻어 x식에 대입합니다. “각도에 sin을 붙였으니 부호도 정해졌다”는 식으로 계산하지 말고 화살표 방향으로 부호를 따로 결정합니다.',
    correction='원본 y식의 +7.5vBsin30°는 그림의 아래쪽 운동과 맞지 않습니다. 올바른 항은 −7.5vBsin30°입니다. 음수를 쓰면 원본이 의도한 양의 두 속력이 나옵니다.',eq='2.5vAcos45°+7.5vBcos30° = 300<br>2.5vAsin45°−7.5vBsin30° = 0')
add(45,'예제 1 · 두 속력을 연립하여 구하고 검산합니다.','Problem Solving 04:05–04:21',
    '앞 장의 비례식을 x식에 넣으면 vB=29.282032 m/s, vA=62.116571 m/s입니다. 반올림 답은 vA≈62.1 m/s, vB≈29.3 m/s입니다. 원본 표시는 A 62.2 m/s, B 29.3 m/s로 A에 작은 수치 차이가 있어 계산값과 구별합니다.',
    '시험용 보강: 검산은 수직 momentum(운동량) 두 크기의 일치와 수평 합 300 kg·m/s를 확인하는 것입니다. Initial kinetic energy(초기 운동에너지)는 4500 J, 계산된 final kinetic energy(최종 운동에너지)는 약 8038.48 J입니다. 늘어난 운동에너지는 폭발의 내부 저장에너지 방출과 연결되며 운동량 보존과 모순이 아닙니다.',
    correction='원본 vA=62.2 m/s와 재계산 62.116571… m/s를 구분합니다. 후자의 소수 첫째 자리 반올림은 62.1 m/s이므로 단순히 동일한 반올림값이라고 적지 않습니다.',eq='vA ≈ 62.117 m/s; vB ≈ 29.282 m/s')
add(46,'예제 1 · 가벼운 파편이 빠른 이유를 식으로 읽습니다.','Problem Solving 04:24–04:39',
    '이 문제에서 수직 운동량이 상쇄되려면 2.5vAsin45°=7.5vBsin30°입니다. 주어진 질량과 두 각도로부터 A가 더 빠른 결과가 나옵니다. 적은 질량이 큰 속력을 갖는다는 설명을 실제 성분 식과 연결해야 합니다.',
    '편집자 보강: “가벼운 물체는 어떤 충돌에서도 반드시 더 빠르다”는 일반 법칙은 아닙니다. 여기서는 초기 총운동량, 두 질량, 지정된 방출 방향이 함께 결과를 정합니다. G의 속도는 폭발 전후 오른쪽 30 m/s로 유지됩니다.')

add(47,'예제 2 · 같은 질량의 당구공 세 개','Problem Solving 04:41–06:29',
    'Ball(공) A만 v₀=4 m/s로 수평 위 30° 방향에서 들어오고 B,C는 initially at rest(처음 정지)입니다. 충돌 후 A는 위쪽 수직에서 오른쪽으로 7.4°, B는 아래쪽 수직에서 오른쪽으로 49.3°, C는 수평 위 45°로 나갑니다. vC=2 m/s이며 vA,vB를 구합니다.',
    '강의는 equal masses(같은 질량들)를 가정합니다. A,B의 최종 각도는 vertical reference(수직 기준)이고 C와 초기 속도의 각도는 horizontal reference(수평 기준)입니다. 이 때문에 A,B의 x성분에는 sin, y성분에는 cos이 붙습니다.')
add(48,'예제 2 · 두 미지수에 두 성분 식을 사용합니다.','Problem Solving 06:31–07:09',
    'A+B+C를 한 system(계)으로 잡으면 공 사이 contact impulses(접촉 충격량)는 internal(내부)입니다. 테이블 위 평면의 마찰 충격량을 무시하면 평면 내 total linear momentum(총 선운동량)이 보존됩니다.',
    'Weight(중량)와 normal reaction(수직항력)이 실제로 존재하지만 평면 내 충격량은 만들지 않는 모델입니다. 주어진 방향과 vC 덕분에 미지수는 두 개뿐입니다. 이 예제는 perfectly elastic(완전탄성)이라는 별도 조건을 주지 않았으므로 운동에너지 보존을 추가하지 않습니다.')
add(49,'예제 2 · B의 y성분은 아래 방향입니다.','Problem Solving 07:13–08:30',
    '동일 질량 m을 모든 항에서 약분합니다. x식은 4cos30°=vAsin7.4°+vBsin49.3°+2cos45°입니다. y식은 4sin30°=vAcos7.4°−vBcos49.3°+2sin45°입니다.',
    '수치로 정리하면 0.128796vA+0.758134vB=2.049888, 0.991671vA−0.652098vB=0.585786입니다. B는 downward(아래 방향)이므로 두 번째 식의 vB 계수는 반드시 음수입니다.',
    correction='원본 49–50장의 y성분 관계에 표시된 +vBcos49.3°와 +0.65210vB는 그림과 맞지 않습니다. 두 항을 음수로 교정해야 원본의 최종 속력 2.13, 2.34 m/s와 일치합니다.',eq='0.128796vA+0.758134vB = 2.049888<br>0.991671vA−0.652098vB = 0.585786')
add(50,'예제 2 · 소거법으로 속력을 구합니다.','Problem Solving 08:24–08:35',
    '첫 식에 cos49.3°≈0.652098, 둘째 식에 sin49.3°≈0.758134를 곱해 더하면 vB항이 상쇄됩니다. 약 0.8358vA=1.7808이므로 vA=2.130675 m/s입니다. 첫 식에 다시 넣으면 vB=2.341889 m/s입니다.',
    '원본 최종 답 vA≈2.13 m/s, vB≈2.34 m/s는 교정한 부호와 일치합니다. 시험용 보강: T₂/T₁=(vA²+vB²+2²)/4²≈0.876514로 운동에너지의 약 12.35%가 줄어듭니다. 이 수치는 보존할 수 없는 에너지식을 억지로 추가하지 않았는지 확인하는 계산입니다.',eq='vA ≈ 2.131 m/s; vB ≈ 2.342 m/s')
add(51,'예제 2 · 충돌 뒤에도 전체 계는 같은 입자들로 구성됩니다.','Problem Solving 08:39–08:55',
    '이 페이지는 같은 당구공 문제를 다시 제시하며 전체 mass center(질량중심)의 운동으로 관점을 바꿉니다. 처음에는 A만 움직이지만, 충돌 후에는 A,B,C가 서로 다른 방향으로 움직입니다.',
    '개별 운동이 달라져도 세 공을 모두 포함한 system(계)은 동일합니다. 내부 충격량은 전체 L을 바꾸지 못하므로 처음의 총운동량으로 vG를 결정할 수 있습니다.')
add(52,'예제 2 · 질량중심은 초기 진행 방향으로 계속 이동합니다.','Problem Solving 08:58–09:23',
    '원본에 포함된 질문의 결론은 G가 v₀와 같은 direction(방향)으로 이동한다는 것입니다. 이 원본 페이지를 보존하되 별도의 추가 점검 문제로 확장하지 않습니다.',
    '시험용 보강: 전체 질량은 3m, 초기 momentum(운동량)은 mv₀이므로 vG=v₀/3입니다. 성분은 (4cos30°/3,4sin30°/3)≈(1.154701,0.666667) m/s, 속력은 1.333333 m/s입니다. 정지하지도 않고 초기 공 A의 속력 4 m/s와 같지도 않습니다. 마찰·쿠션 충격량이 없는 모델 구간에 대한 결과입니다.')

add(53,'예제 3 · 움직일 수 있는 카트에 매달린 진자','Problem Solving 09:26–11:58',
    'Ball(공) B의 mass(질량)는 mB, cart(카트) A의 질량은 mA입니다. B는 길이 ℓ의 inextensible cord(비신축성 줄)로 A에 매달려 있습니다. A는 frictionless horizontal track(마찰 없는 수평 궤도)을 움직이며 처음 정지해 있고, B는 최저점에서 오른쪽 v₀=√(2gℓ)를 받습니다.',
    '구할 것은 B가 maximum elevation(최대 높이)에 도달했을 때의 absolute velocity(절대속도)와 추가 상승 높이 h입니다. 최고점에서도 카트가 움직이므로 공의 절대속도를 0으로 놓지 않습니다.',
    correction='문제 53장과 자막 10:11·14:27은 v₀=√(2gℓ), 회고 62장은 v₀²&lt;2gℓ를 사용합니다. 본문은 먼저 일반 v₀의 결과를 유도한 뒤 문제의 등호 조건을 대입합니다. 부등호 조건으로 조용히 바꾸지 않습니다.')
add(54,'예제 3 · 수평 운동량과 전체 에너지를 결합합니다.','Problem Solving 12:01–12:54',
    'Cart+ball(카트+공)을 한 system(계)으로 잡습니다. 수평 외력이 없으므로 horizontal momentum(수평 운동량)이 보존됩니다. 최고점에서 두 물체의 속도가 같다는 relative-motion condition(상대운동 조건)을 결합하면 그 공통 속도를 구할 수 있습니다.',
    '그다음 energy conservation(에너지 보존)을 사용합니다. Gravity(중력)는 보존력이고, 이상적 줄은 계 전체에 순일을 하지 않으며 수직 지지 반력도 수평으로 움직이는 카트에 일을 하지 않습니다. 마찰·줄 질량 등 손실을 무시하는 모델입니다.')
add(55,'예제 3 · 수직 외력이 있어도 수평 운동량은 보존됩니다.','Problem Solving 12:57–13:59',
    '외력에는 두 weight(중량)와 track reaction(궤도 반력)이 있습니다. 모두 vertical(수직)이므로 ∫ΣFx dt=0입니다. 따라서 Lx,₁=Lx,₂를 쓸 수 있습니다.',
    '줄이 공과 카트를 당기는 force(힘)는 각각의 운동량을 바꾸지만 전체 계에서는 internal(내부)입니다. 수직 운동량의 보존까지 주장하면 안 됩니다. 카트에 대한 궤도의 수직 반력이 존재하기 때문입니다.',eq='Lx,₁+∫ΣFx dt = Lx,₂; ∫ΣFx dt = 0')
add(56,'예제 3 · 최고점 조건을 넣기 전 수평 식을 씁니다.','Problem Solving 14:03–14:47',
    '상태 1은 공의 최저점 출발, 상태 2는 공이 처음으로 가장 높이 올라간 순간입니다. 수평 속도들에 대해 mAvA,₁+mBvB,₁=mAvA,₂+mBvB,₂입니다. 처음에는 vA,₁=0, vB,₁=v₀입니다.',
    '이 식만으로 최종 속도 두 개를 따로 정할 수는 없습니다. 다음 장에서 maximum elevation(최대 높이)의 turning-point condition(방향 전환점 조건)을 적용해 두 속도를 연결합니다.',eq='mBv₀ = mAvA,₂+mBvB,₂')
add(57,'예제 3 · 최고점에서는 상대속도가 0입니다.','Problem Solving 14:49–16:18',
    'B가 지지점보다 낮은 범위에서 첫 turning point(방향 전환점)에 이르면 줄의 각도 변화율이 0이고 vB/A,₂=0입니다. Relative velocity relation(상대속도 관계) vB,₂=vA,₂+vB/A,₂로부터 vB,₂=vA,₂=V입니다.',
    '따라서 mBv₀=(mA+mB)V, V=mBv₀/(mA+mB)입니다. 이 최고점 조건은 공의 velocity relative to A(카트에 대한 상대속도)가 0이라는 뜻이지, 지면 기준 absolute velocity(절대속도)가 0이라는 뜻이 아닙니다.',eq='vA,₂ = vB,₂ = V = mBv₀/(mA+mB)')
add(58,'예제 3 · 내부 장력은 전체에 순일을 하지 않습니다.','Problem Solving 16:22–16:45',
    '카트가 움직이므로 tension(장력)이 공 하나에 하는 일은 일반적으로 0이라고 할 수 없습니다. 그러나 ideal inextensible cord(이상적 비신축성 줄)의 양 끝에 대한 일은 합하면 상쇄됩니다. 양 끝 상대속도의 줄 방향 성분이 0이기 때문입니다.',
    '이는 일반 내력의 일이 항상 0이라는 주장이 아니라 이 구속조건에서의 결과입니다. 전체 계의 mechanical energy(역학적 에너지)는 보존되어 T₁+V₁=T₂+V₂를 쓸 수 있습니다.',eq='T₁+V₁ = T₂+V₂')
add(59,'예제 3 · 초기에는 공만 운동에너지를 갖습니다.','Problem Solving 16:48–17:24',
    'Position 1(상태 1)에서 cart(카트)는 stationary(정지)이므로 T₁=½mBv₀²입니다. 공의 초기 높이를 datum(기준 높이)으로 잡으면 공의 초기 potential energy(위치에너지)는 0입니다.',
    '원본은 카트의 일정한 위치에너지를 mAgℓ로 적어 V₁=mAgℓ로 표현합니다. 중요한 것은 이 카트 높이가 이후에도 변하지 않는다는 점입니다. 카트의 정확한 질량중심 높이를 다른 일정값으로 잡아도 앞뒤 같은 상수가 약분되어 답은 같습니다.',eq='T₁ = ½mBv₀²; V₁ = constant cart potential(일정한 카트 위치에너지)')
add(60,'예제 3 · 최고점에도 두 물체의 병진 에너지가 남습니다.','Problem Solving 17:27–17:54',
    'Position 2(상태 2)에서 두 물체는 모두 V로 이동하므로 T₂=½(mA+mB)V²입니다. 공은 h만큼 올라갔으므로 V₂−V₁=mBgh입니다.',
    '“최고점이므로 T₂=0”은 카트의 이동을 빠뜨린 식입니다. Relative kinetic energy(상대 운동에너지)가 사라져도 center-of-mass translation(질량중심 병진)의 에너지는 남는다는 앞의 분해와 일치합니다.',eq='T₂ = ½(mA+mB)V²; V₂−V₁ = mBgh')
add(61,'예제 3 · 공통 속도를 제거하여 상승 높이를 구합니다.','Problem Solving 17:58–18:04',
    '½mBv₀²=½(mA+mB)V²+mBgh에 V=mBv₀/(mA+mB)를 대입합니다. 양변을 mBg로 나누면 h=v₀²/(2g)−[(mA+mB)/mB]V²/(2g)입니다.',
    '이를 정리하면 h=[mA/(mA+mB)]v₀²/(2g)입니다. 문제에 적힌 v₀=√(2gℓ)를 최종적으로 대입하면 h=mAℓ/(mA+mB), V=[mB/(mA+mB)]√(2gℓ)입니다. 특정 질량값이 없으므로 일반식이 최종 답입니다.',
    extra=card('시험용 보강 · 질량이 같을 때의 간단한 검산','mA=mB라면 V=v₀/2, h=v₀²/(4g)입니다. 이 문제의 초기 속도를 쓰면 h=ℓ/2입니다. 초기 에너지의 일부는 최고점의 공통 병진 에너지로 남으며 나머지가 중력 위치에너지로 바뀝니다.'),eq='h = [mA/(mA+mB)]v₀²/(2g)<br>v₀=√(2gℓ)일 때 h = mAℓ/(mA+mB)')
add(62,'예제 3 · 높이 조건과 질량비 극한을 확인합니다.','Problem Solving 18:07–20:07',
    '양의 유한 질량이면 mA/(mA+mB)&lt;1입니다. 따라서 문제의 v₀²=2gℓ에서도 h&lt;ℓ로, B는 지지점 아래에 머뭅니다. 원본 회고의 더 강한 조건 v₀²&lt;2gℓ도 이 결론을 보장하지만 문제 진술과 같은 조건은 아닙니다.',
    'mA≫mB인 heavy cart(무거운 카트) 극한에서는 V→0, h→v₀²/(2g)로 fixed-pivot pendulum(고정 지지점 진자)에 가까워집니다. mA≪mB인 light cart(가벼운 카트) 극한에서는 V→v₀, h→0으로 공의 이동을 카트가 거의 그대로 따라갑니다. 유한 질량에서 정확히 0이라는 뜻이 아니라 극한입니다.',
    correction='원본의 h&lt;1은 길이 ℓ과 비교하는 h&lt;ℓ로 읽어야 하며, h=0g는 높이의 단위가 아니므로 h→0으로 정리합니다. 부등호 조건과 등호 조건의 차이는 위에서 별도로 유지했습니다.')

add(63,'예제 4 · 두 번의 충돌 뒤 쿠션에 닿기 직전의 속도','Problem Solving 20:10–21:59',
    'Ball(공) A는 오른쪽 v₀=3 m/s로 출발하여 정지한 B, 이어서 C와 충돌합니다. 이후 A는 윗변 A′에 squarely(수직으로), C는 오른쪽 변 C′에 squarely(수직으로), B는 아랫변 B′에 obliquely(비스듬히) 도달합니다. 공들은 equal mass(같은 질량)인 입자 모델입니다.',
    '두 공 사이 collisions(충돌들)는 perfectly elastic(완전탄성)이고 평면 마찰·공의 자전은 무시합니다. 구할 속도는 테이블 쿠션에 부딪히기 직전이며 쿠션과의 반발은 포함하지 않습니다. 외부 쿠션 충격량까지 포함하면 아래의 전체 운동량 보존을 그대로 사용할 수 없습니다.')
add(64,'예제 4 · 네 미지수에 네 보존식을 사용합니다.','Problem Solving 22:02–23:05',
    'A는 위쪽 속력 하나, C는 오른쪽 속력 하나가 미지수입니다. B는 방향을 모르므로 x,y성분 두 개가 미지수입니다. 총 four unknowns(네 미지수)에 대해 linear momentum(선운동량) x,y 두 식, angular momentum(각운동량) 한 식, energy(에너지) 한 식을 사용합니다.',
    '각 보존의 근거도 다릅니다. 평면 외력·외력 모멘트를 무시하여 두 운동량을 보존하고, perfectly elastic(완전탄성) 조건 때문에 운동에너지를 보존합니다. 미지수 수가 맞는다는 이유만으로 성립하지 않는 식을 추가해서는 안 됩니다.')
add(65,'예제 4 · 부호 있는 성분과 양의 방향 크기를 분리합니다.','Problem Solving 23:08–24:05',
    '오른쪽 +x, 위쪽 +y를 정합니다. A의 위쪽 속력을 a, C의 오른쪽 속력을 c, B의 오른쪽 크기를 bx, 아래쪽 크기를 by라 두면 vA=a j, vB=bx i−by j, vC=c i입니다. 여기서 a,c,bx,by는 그림의 방향을 따르는 nonnegative magnitudes(0 이상 크기)입니다.',
    '원본 65장은 vB=vB,x i+vB,y j로 signed y-component(부호 있는 y성분)를 정의하지만 이후 식에서는 vB,y를 아래 방향 크기처럼 씁니다. 본문은 by라는 별도 양의 크기로 통일하고 실제 y성분은 −by라고 표시합니다.',
    correction='원본의 vB,y가 어떤 줄에서는 부호 있는 성분, 어떤 줄에서는 아래 방향 크기로 쓰입니다. 본문 bx,by는 오른쪽·아래쪽 크기이고 최종 속도벡터에 −by j를 사용합니다.',eq='vA = a j; vB = bx i−by j; vC = c i')
add(66,'예제 4 · 모멘트팔이 세 번째 식을 제공합니다.','Problem Solving 24:10–25:14',
    '동일한 mass(질량) m을 약분하면 x식 bx+c=3, y식 a−by=0입니다. Fixed point(고정점) O는 테이블 좌하단이고 positive angular momentum(양의 각운동량)은 반시계 방향입니다.',
    '초기 A의 수평 경로는 O 위 0.6 m이므로 HO,₁/m=−0.6(3)입니다. 최종 A의 수직 경로는 O 오른쪽 2.4 m로 +2.4a, B는 아랫변 x=2.1 m에서 아래 방향이므로 −2.1by, C의 수평 경로는 O 위 0.9 m이므로 −0.9c입니다. 따라서 −1.8=2.4a−2.1by−0.9c입니다.',
    correction='원본 첫 줄 L₁=Σ∫Fdt=L₂는 충격량 원리의 덧셈 관계를 잘못 표시한 것입니다. L₁+∫ΣFext dt=L₂이고 이 문제에서 평면 외부 충격량을 0으로 놓아 L₁=L₂가 됩니다.',
    extra=card('시험용 보강 · 쿠션 도착점의 위치를 써도 되는 이유',
        '충돌이 끝난 뒤 각 공은 속도가 일정한 straight path(직선 경로)를 따릅니다. 그 경로 위에서 위치를 Δr=vΔt만큼 옮겨도 Δr×mv=0이므로 각운동량은 같습니다. 따라서 쿠션 충돌 직전의 경로 끝점을 모멘트팔 계산에 사용할 수 있습니다. 세 공이 실제로 동시에 쿠션에 닿는다고 가정하는 것이 아닙니다.'),eq='bx+c = 3; a−by = 0<br>−0.6(3) = 2.4a−2.1by−0.9c')
add(67,'예제 4 · 완전탄성 조건은 운동에너지의 네 항을 연결합니다.','Problem Solving 25:17–25:50',
    '테이블 위 높이는 일정하므로 gravitational potential energy(중력 위치에너지)의 변화가 0입니다. 각 공 사이 충돌을 perfectly elastic(완전탄성)으로 모델링했으므로 초기 ½m(3²)은 최종 ½m[a²+(bx²+by²)+c²]와 같습니다.',
    'B의 speed squared(속력 제곱)는 bx²+by²입니다. 방향 성분 중 하나만 넣거나 bx+by를 먼저 더해 제곱하면 안 됩니다. 질량과 ½를 약분하면 a²+bx²+by²+c²=9입니다.',eq='a²+bx²+by²+c² = 9')
add(68,'예제 4 · 두 근 중 주어진 진행 방향과 맞는 근을 택합니다.','Problem Solving 25:58–26:03',
    'a=by를 각운동량 식에 넣으면 −1.8=0.3a−0.9c이므로 a=by=3c−6입니다. 또한 bx=3−c입니다. 에너지식은 2(3c−6)²+(3−c)²+c²=9, 즉 20c²−78c+72=0이 됩니다.',
    '시험용 보강: 이차방정식의 두 근은 c=2.4 m/s와 c=1.5 m/s입니다. 후자는 a=−1.5 m/s로 A가 윗변을 향한다는 주어진 방향과 모순이므로 제외합니다. c=2.4이면 a=by=1.2, bx=0.6 m/s입니다.',
    '최종 답은 vA=1.2j m/s, vB=(0.6i−1.2j) m/s, vC=2.4i m/s입니다. B의 speed(속력)는 √(0.6²+1.2²)=1.341641 m/s≈1.342 m/s입니다. 음의 y성분은 아래 방향이라는 뜻이지 음의 속력이 아닙니다.',eq='vA = 1.2j m/s<br>vB = (0.6i−1.2j) m/s; |vB| ≈ 1.342 m/s<br>vC = 2.4i m/s')
add(69,'예제 4 · 실제 당구와 입자 모델의 차이를 확인합니다.','Problem Solving 26:06–26:56',
    '실제 공은 friction(마찰), rotation/spin(회전/스핀), restitution(반발) 손실의 영향을 받습니다. 이 문제는 입자 모델로 자전 에너지와 접선 접촉 효과를 생략하여 간단한 보존식만 사용했습니다.',
    '원본의 “energy would not be conserved”는 전체 물리적 에너지가 사라진다는 뜻이 아니라 여기서 합산한 translational kinetic energy(병진 운동에너지)가 유지되지 않을 수 있다는 뜻입니다. 더 현실적인 분석에는 충돌 조건에 맞는 반발계수와 강체·마찰 모델이 필요합니다. 원본의 Chapter 17 안내는 교재 단원이지 현재 주차 일정으로 바꾸지 않습니다.')
add(70,'참고문헌','원본 Reference 페이지',
    '원본의 Beer, Johnston, Cornwell, Self, Sanghi, <i>Vector Mechanics for Engineers: Dynamics</i>, 12th edition(제12판), Chapter 14(제14장) 참고문헌을 보존합니다. 별도로 교재 본문을 열람하거나 인용한 것은 아닙니다.',role='Reference')

exam_items = [
    ('Define(정의하라) effective force(유효력), and distinguish(구별하라) it from external force(외력).',
     'The effective force of particle i is mi ai. It equals the resultant of all external and internal forces acting on that particle; it is not an additional applied force.',
     'Effective force(유효력)는 mᵢaᵢ입니다. 입자 하나에는 internal force(내력)도 포함해야 하며, 전체 계를 합한 뒤에야 내력이 상쇄됩니다.'),
    ('Why do internal forces(내력들) cancel in the total force and moment equations(전체 힘·모멘트 식)?',
     'Each internal-force pair is equal, opposite, and collinear. The pair has zero resultant force and zero resultant moment. This cancellation does not imply zero internal work.',
     'Equal, opposite, and collinear(크기가 같고 반대이며 동일 작용선상)라는 세 조건을 구분합니다. 떨어진 작용점에 있는 반대 방향 힘만으로는 moment(모멘트)가 반드시 0은 아닙니다.'),
    ('Express(나타내라) total linear momentum(총 선운동량) using the mass center(질량중심).',
     'For a fixed collection of constant-mass particles, L = sum(mi vi) = m vG. Hence the resultant external force equals m aG. If it vanishes, the mass-center velocity is constant, not necessarily zero.',
     'Constant(일정한)과 zero(0인)를 구별합니다. Resultant external force(외력 합력)가 0이면 질량중심은 정지할 수도 있고 일정한 속도로 이동할 수도 있습니다.'),
    ('State(서술하라) the angular momentum equation(각운동량 식) about a fixed point(고정점) O.',
     'For O fixed in an inertial frame, HO = sum(ri cross mi vi), and the resultant external moment about O equals dHO/dt. The same reference point must be used for momentum and moment.',
     'Fixed in an inertial frame(관성 기준계에 고정된) 조건과 동일한 reference point(기준점)를 명시합니다. HG 자체와 torque(토크)를 같다고 쓰지 않습니다.'),
    ('Why is HG = H\u2032G valid for a nonrotating centroidal frame(회전하지 않는 질량중심 기준계)?',
     'Substituting vᵢ = vG + v′ᵢ gives HG = H′G + [Σmᵢr′ᵢ] × vG. The bracket is zero by the definition of the mass center, so HG = H′G even when G accelerates.',
     'Prime(프라임)은 이번 강의에서 relative quantity(상대량)입니다. G가 accelerating(가속하는) 경우도 가능하지만 축은 nonrotating(회전하지 않는) 조건입니다.'),
    ('Decompose(분해하라) kinetic energy(운동에너지) into translational and relative parts(병진·상대운동 항).',
     'T = ½mvG² + ½Σmᵢ(v′ᵢ)². The mixed term vanishes because Σmᵢv′ᵢ = 0. A stationary mass center does not imply zero kinetic energy.',
     'Stationary mass center(정지한 질량중심)에서도 입자들은 서로 상대운동을 할 수 있습니다. 내부 운동을 회전 한 가지로만 제한하지 않습니다.'),
    ('Does zero resultant internal force(내력 합력 0) imply zero internal work(내부 일 0)?',
     'No. The work of a pair is fij dot (dri - drj), which is generally nonzero because the application points may undergo different displacements. For conservative interactions, this work equals minus the change in potential energy.',
     'Displacement(변위)는 두 작용점마다 다릅니다. Conservative interaction(보존적 상호작용)이면 U = −ΔV라는 부호까지 명시합니다.'),
    ('When are linear momentum(선운동량), angular momentum(각운동량), and kinetic energy(운동에너지) conserved(보존되는가)?',
     'Linear momentum requires zero resultant external force, and angular momentum requires zero resultant external moment about the selected point. Zero net impulse gives equality between endpoint momenta. Kinetic energy needs a separate energy condition, such as perfectly elastic collisions at constant potential energy.',
     '세 conservation conditions(보존 조건)은 서로 다릅니다. Perfectly elastic(완전탄성)이라는 말이 없는 폭발·일반 충돌에 kinetic-energy conservation(운동에너지 보존)을 자동으로 붙이지 않습니다.'),
    ('At maximum elevation(최대 높이), is the ball on the movable cart(이동 가능한 카트) at rest(정지한 상태인가)?',
     'At the first turning point below the pivot, the ball is instantaneously at rest relative to the cart, not relative to the ground. Both have V = mB v0/(mA + mB). Energy conservation then gives h = [mA/(mA + mB)]v0 squared/(2g).',
     'At rest relative to the cart(카트에 대하여 정지한)라고 기준을 적습니다. Absolute velocity(절대속도)는 남으며 최고점의 운동에너지를 0으로 두면 안 됩니다.'),
    ('How do you choose the admissible root(허용되는 근) in the final pool problem(마지막 당구 문제)?',
     'The energy equation gives c = 2.4 or 1.5 m/s. Since a = 3c - 6 is the upward speed of A, the second root contradicts the specified direction. Thus c = 2.4, a = 1.2, bx = 0.6, and by = 1.2 m/s.',
     'Admissible(허용되는)은 단순히 이차방정식을 만족한다는 뜻이 아닙니다. Specified direction(주어진 방향)까지 만족해야 하며, B의 실제 y성분은 −by입니다.'),
    ('Explain(설명하라) squarely(수직으로) and obliquely(비스듬히) in the pool problem(당구 문제).',
     'Squarely means that the velocity is perpendicular to the cushion just before impact. Obliquely means that both normal and tangential velocity components may be present. The stated velocities are evaluated before cushion impulses act.',
     'Cushion(쿠션)에 대한 방향 조건입니다. 쿠션의 external impulse(외부 충격량)가 작용하기 전 속도를 구하므로 쿠션 반발까지 포함한 운동량 보존으로 확장하지 않습니다.'),
]

terms = [
    ('system of particles','입자계','함께 분석하도록 선택한 여러 입자의 집합'),
    ('fixed collection / constant mass','고정된 집합 / 일정 질량','분석 중 입자 구성과 각 질량이 바뀌지 않는 전제'),
    ('internal / external force','내력 / 외력','계 안의 입자 사이 작용 / 계 밖에서 들어오는 작용'),
    ('effective force / inertia force','유효력 / 관성력','mᵢaᵢ / 부호가 반대인 −mᵢaᵢ; 서로 혼동하지 않음'),
    ('resultant / moment','합력 / 모멘트','힘의 벡터합 / 기준점에 대한 r×F'),
    ('equal, opposite, and collinear','같은 크기, 반대 방향, 동일 작용선상','입자 사이 내력의 합력·합모멘트 상쇄 조건'),
    ('equipollent / equivalent','합력·합모멘트가 같은 / 동등한','전체 합의 일치 / 여기서는 개별 운동 효과까지의 동등성 구별'),
    ('deformable / rigidly connected','변형 가능한 / 상대거리가 고정되게 연결된','입자 사이 거리 변화 가능 / 강체로 이어지는 구속'),
    ('mass center / center of gravity','질량중심 / 무게중심','질량 가중 평균 위치 / 중량의 합력 작용점; 균일 중력장에서 일치'),
    ('entire mass / concentrated','전체 질량 / 집중된','계 전체 질량의 합 / 한 점에 모인 것처럼 취급'),
    ('linear momentum / angular momentum','선운동량 / 각운동량','L=Σmᵢvᵢ / H=Σ(rᵢ×mᵢvᵢ)'),
    ('absolute / relative velocity','절대 / 상대속도','관성 기준계 기준 속도 / 다른 물체나 기준계에 대한 속도'),
    ('inertial / Newtonian frame','관성 / 뉴턴 기준계','뉴턴 운동법칙을 가속 기준계 보정 없이 적용하는 기준계'),
    ('noninertial / non-Newtonian','비관성 / 비뉴턴','이번 강의에서는 가속하는 기준계를 나타내는 표현'),
    ('centroidal / nonrotating frame','질량중심 / 회전하지 않는 기준계','원점이 G / 축 방향이 고정됨'),
    ('translation / relative motion','병진 / 상대운동','좌표계 축 방향을 유지하며 이동 / 기준 물체에 대한 운동'),
    ('prime / time derivative','프라임 / 시간미분','이번 강의의 상대량 표시 ′ / 시간에 대한 변화율'),
    ('fixed point / reference point','고정점 / 기준점','관성 기준계에 고정된 점 / 모멘트·각운동량을 계산하는 점'),
    ('cross product / dot product','벡터곱 / 내적','모멘트에 쓰는 벡터 연산 / 일과 에너지에 쓰는 스칼라 연산'),
    ('central force / couple','중심력 / 우력','고정된 중심을 향하는 힘 / 합력 0이나 모멘트를 만드는 힘 쌍'),
    ('conserved / constant / stationary','보존되는 / 일정한 / 정지한','시간 변화 없음 / 값 일정 / 해당 기준계에서 속도 0'),
    ('kinetic / potential energy','운동 / 위치에너지','운동에 의한 에너지 / 보존적 상호작용의 위치·배치에 따른 에너지'),
    ('internal work / conservative force','내부 일 / 보존력','내력이 한 일 / 일을 −ΔV로 표현하는 힘'),
    ('impulse / angular impulse','충격량 / 각충격량','힘의 시간적분 / 모멘트의 시간적분'),
    ('net external impulse / negligible','순외부 충격량 / 무시할 만큼 작은','모든 외력 충격량의 합 / 선택한 비교에서 효과가 충분히 작은'),
    ('explosion / fragment','폭발 / 파편','내부 에너지가 운동으로 전환될 수 있는 사건 / 나뉜 물체'),
    ('equal mass / identical','같은 질량 / 동일한','질량 조건이 같음 / 문제에서 지정한 물성이 같음'),
    ('horizontal / vertical / upward / downward','수평 / 수직 / 위쪽 / 아래쪽','축과 방향을 정할 때 쓰는 조건 표현'),
    ('signed component / magnitude / speed','부호 있는 성분 / 크기 / 속력','축 방향 부호 포함 / 벡터의 비음수 길이 / 속도의 크기'),
    ('cart / ball / cord / pivot','카트 / 공 / 줄 / 지지점','카트–진자 예제의 물체와 연결점'),
    ('frictionless / inextensible / taut','마찰 없는 / 비신축성 / 팽팽한','마찰 효과 무시 / 길이 일정 / 장력 전달 가능한 상태'),
    ('maximum elevation / turning point','최대 높이 / 방향 전환점','가장 높은 위치 / 해당 상대운동이 멈췄다가 반대로 전환되는 점'),
    ('initially at rest / common velocity','처음 정지한 / 공통 속도','초기 속도 0 / 여러 물체가 같은 순간에 함께 갖는 속도'),
    ('datum / reaction / tension','기준 높이 / 반력 / 장력','위치에너지의 영점 / 구속면의 힘 / 줄의 당기는 힘'),
    ('limiting case / finite','극한 경우 / 유한한','비율 등을 한계로 보낸 분석 / 무한대가 아닌 값'),
    ('perfectly elastic / dissipated','완전탄성 / 소산된','충돌의 운동에너지 보존 모델 / 열·변형 등으로 전환된'),
    ('squarely / obliquely / cushion','수직으로 / 비스듬히 / 쿠션','테이블 경계에 직각 방향 / 법선과 다른 경사 방향 / 당구대 경계'),
    ('before impact / moment arm','충돌 전 / 모멘트팔','접촉 충격량 작용 직전 / 기준점에서 운동량 작용선까지 거리'),
    ('admissible root / specified direction','허용되는 근 / 주어진 방향','물리 조건까지 만족하는 해 / 문제에서 지정한 진행 방향'),
    ('determine / express / distinguish / neglect','구하라 / 나타내라 / 구별하라 / 무시하라','계산해 결정 / 식으로 표현 / 차이 설명 / 모델에서 작은 효과 제외'),
]

audit = [
    ('Overview 00:34–00:51','cards','carts(차량들)','롤러코스터 입자계 설명 문맥'),
    ('Contents 1 00:17–00:29','fully dynamic / rigid parties','fluid dynamics(유체역학) / rigid bodies(강체들)','원본 5의 응용 대상'),
    ('Contents 1 01:05–01:23','mess/math center / in-person momentum','mass center(질량중심) / impulse–momentum(충격량·운동량)','원본 7의 용어와 관계식'),
    ('원본 8','mᵢaᵢ = external force','effective force(유효력)','입자 하나의 Fᵢ+Σⱼfᵢⱼ=mᵢaᵢ'),
    ('Contents 1 03:52 / 원본 11','cos / 반대 방향이면 모멘트도 0으로 오해','cross product(벡터곱) / 동일 작용선 조건 명시','(rᵢ−rⱼ)×fᵢⱼ=0의 기하학 조건'),
    ('원본 12 · Contents 1 06:08–06:30','equipollent by not equivalent / equivalent 반복','equipollent but not equivalent(합력·합모멘트 같지만 개별 효과 동등하지 않음)','원본의 두 용어와 변형 가능한 입자계 문맥'),
    ('Contents 1 07:36–07:51','a six / a 6.0','fixed point O(고정점 O)','원본 15의 각운동량 기준점'),
    ('Contents 2 전반','messenger / math center','mass center(질량중심)','G의 정의와 질량 가중 위치 관계'),
    ('Contents 2 06:39–06:45','v′ᵢ를 relative position vector로 지칭','relative velocity(상대속도)','기호 및 m/s 차원'),
    ('원본 23 · Contents 2 10:59–11:23','aG를 constant라고 표현','입자 번호 i와 무관, 시간에 대해 일정하다는 뜻 아님','뒤의 independent of i 설명과 이중 합 분리'),
    ('원본 23','입자별 mᵢaᵢ를 외력만으로 바꾸기 쉬움','개별 입자에는 내력 포함; 전체 모멘트 합에서 상쇄','원본 8–11의 전체 계 유도'),
    ('원본 27','HG=H′G=ΣMG / 전개식 상대속도 프라임 누락','HG=H′G, dHG/dt=dH′G/dt=ΣMext,G','각운동량과 모멘트의 차원, vᵢ=vG+v′ᵢ'),
    ('Contents 2 17:10–17:46','외력이 하나라도 있으면 L 비보존으로 읽힘','외력 합력 또는 해당 방향 순충격량으로 판단','ΣFext=dL/dt; 중심력 예시는 합력 비영·모멘트 0'),
    ('원본 36','일을 potential energy change로만 설명','Uconservative=V₁−V₂=−ΔV','T₁+U=T₂와 T₁+V₁=T₂+V₂ 비교'),
    ('Problem Solving 00:33','30 millimeters per second','30 m/s','원본 40의 수치·단위'),
    ('원본 44','y식의 두 파편 항이 모두 +','2.5vAsin45°−7.5vBsin30°=0','그림에서 B는 아래 방향'),
    ('원본 45','vA=62.2 m/s','vA=62.116571… m/s, 소수 첫째 자리 62.1','주어진 질량·각도로 연립 재계산; 원본값과 구별'),
    ('원본 49–50','y식의 B 항이 +','vAcos7.4°−vBcos49.3°=4sin30°−2sin45°','B는 아래 방향; 원본의 최종 숫자는 음수 항과 부합'),
    ('원본 53·62 · Problem Solving 10:11·14:27','문제 v₀=√(2gℓ), 회고 v₀²&lt;2gℓ','일반식 유도 후 문제의 등호 조건 대입, 불일치 별도 표시','문제·영상과 회고를 임의 통일하지 않음'),
    ('Problem Solving 예제 3','card / chord / pole','cart(카트) / cord(줄) / ball(공)','원본 그림의 물체·구속조건'),
    ('원본 62 · Problem Solving 18:18','h&lt;1 / h=0g','h&lt;ℓ / 가벼운 카트 극한 h→0','길이 차원과 h=[mA/(mA+mB)]v₀²/(2g)'),
    ('원본 65–66','vB,y를 부호 있는 성분과 아래 방향 크기로 혼용','본문 by는 아래 방향 양의 크기; 실제 성분은 −by','원본 방향 그림과 y운동량 식'),
    ('원본 66','L₁=Σ∫Fdt=L₂','L₁+∫ΣFext dt=L₂','충격량·운동량 원리의 덧셈 관계'),
    ('원본 68','결과만 제시','이차방정식의 두 근 및 방향 조건에 따른 선택을 보강','20c²−78c+72=0; 두 번째 근은 A의 방향과 모순'),
    ('원본 69 · Problem Solving 26:06–26:56','energy would not be conserved','분석에 포함한 병진 운동에너지의 비보존으로 한정','회전·마찰·변형을 생략한 입자 모델과 전체 에너지 구별'),
    ('Summary 00:47–01:00','next week rigid bodies','다음 단원 안내로 분리; 중간고사 날짜 추정 안 함','보존된 강의 인덱스: Week 08 날짜 미기재, Lecture 9는 Week 09'),
]

roadmap = '''<section class="editorial-section section-divider" id="course-roadmap" aria-labelledby="roadmap-title">
<p class="section-kicker">Summary video · Course roadmap</p>
<h2 class="section-title" id="roadmap-title">Summary 영상 후반: 다음 단원은 강체 운동입니다.</h2>
<p class="section-lead">Summary 00:17–00:44의 Newton’s second law(뉴턴 제2법칙), mass center(질량중심), momentum(운동량), energy(에너지), conservation(보존) 복습은 위 핵심 개념 요약에 반영했습니다. 이후의 강좌 진행 안내만 아래에 분리했습니다.</p>
</section>
<section class="editorial-section" id="roadmap-detail" aria-labelledby="roadmap-detail-title">
<p class="section-kicker">What comes next</p>
<h2 class="section-title" id="roadmap-detail-title">입자계의 전체 운동에서 강체의 위치와 방향으로 확장합니다.</h2>
<div class="card"><h3>Rigid bodies(강체들)와 reference frames(기준계들)</h3><p>영상 후반은 rigid-body motion(강체 운동)으로 넘어가며 3D(3차원)에서 위치뿐 아니라 orientation(방향 자세)을 기술하는 기준계를 소개할 것이라고 예고합니다. 이는 이번 입자계 개념 요약을 대신하는 내용이 아니라 다음 단원 안내입니다.</p><p>보존된 강의 인덱스의 Week 08은 Midterm – No class(중간고사·수업 없음), 날짜 미기재입니다. 다음 Lecture 9 · Kinematics of Rigid Bodies I(강체 운동학 I)는 Week 09 · 2026-10-28로 기재되어 있습니다. 영상의 “next week(다음 주)”를 실제 중간고사 날짜나 다음 강의 날짜로 환산하지 않습니다.</p></div>
<div class="evidence"><span>Summary 00:47–01:00</span><span>강의 인덱스 대조</span></div>
</section>'''

template = (SITE/'templates/lecture-page.template.html').read_text(encoding='utf-8')
source_pattern = r'<section class="source-section"[\s\S]*?</section>'
source_template = re.search(source_pattern,template).group()
sections = []
assert len(records)==70
for n,(title,evidence,blocks,role) in enumerate(records,1):
    section = source_template
    replacements = {'NN':f'{n:02d}', 'SLIDE_ROLE':role, 'SLIDE_HEADING':title,
        'LECTURE_SLUG':'lecture08','DESCRIPTIVE_ALT_TEXT':f'Lecture 8 원본 슬라이드 {n:02d}: {escape(title)}',
        'CURRENT_PAGE':str(n),'PAGE_COUNT':'70','TRANSCRIPT_TIME_OR_SLIDE_ROLE':evidence,
        'SLIDE_EXPLANATION_BLOCKS':blocks}
    for key,value in replacements.items():
        section = section.replace('{{'+key+'}}',value)
    sections.append(section)
template = re.sub(source_pattern,lambda _: '\n\n'.join(sections),template,count=1)
exam_html = ''.join('<div class="exam-card"><h3>'+q+'</h3><div class="answer"><span class="answer__label">Model answer</span>'+escape(a)+'</div><p style="margin-top: 12px">'+ko+'</p></div>' for q,a,ko in exam_items)
template = re.sub(r'<div class="exam-card">\s*<h3>\{\{EXAM_QUESTION\}\}</h3>[\s\S]*?</div>\s*</div>',lambda _:exam_html+'\n          </div>',template,count=1)
videos = [('Overview','E4n4KXxWxLc'),('Contents 1','g07zOf2lvBo'),('Contents 2','w52fBxRGP6s'),('Problem Solving','gXdeWNdR2CE'),('Summary','4jGpna7ysWQ')]
toc = [('overview','전체 개요'),('concept-map','개념 지도'),('concept-summary','핵심 개념 요약')] + [(f'slide-{i:02d}',f'{i:02d} · {r[0]}') for i,r in enumerate(records,1)] + [('course-roadmap','Summary · 다음 단원 안내'),('exam-english','시험 영어'),('glossary','용어집'),('asr-log','원본·스크립트 교정'),('sources','출처')]
values = {
    'LECTURE_NUMBER':'Lecture 8','LECTURE_TITLE':'Systems of Particles',
    'ONE_SENTENCE_DESCRIPTION':'7주차 입자계: 원본 70장과 영어 영상 5편을 대조한 한국어 수업 대체 학습 노트',
    'WEEK':'Week 07','DATE_OR_날짜_미기재':'2026-10-14','PAGE_COUNT':'70',
    'LECTURE_PROMISE':'System of particles(입자계)의 전체 운동과 내부 상대운동을 구분하고, mass center(질량중심)·momentum(운동량)·energy(에너지) 관계를 폭발·당구·카트 진자 예제까지 연결합니다.',
    'VIDEO_SET':'Overview · Contents 1·2 · Problem Solving · Summary',
    'ALL_CONTENTS_AND_PROBLEM_SOLVING_BUTTONS':'\n'.join(f'<a class="button button--primary" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상 열기</a>' for label,vid in videos[1:4]),
    'ORIGINAL_PDF_URL':'https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/lecture08_note.pdf',
    'LECTURE_NOTE_FILENAME':'lecture08_note.pdf',
    'CORE_RELATIONSHIP_HEADLINE':'여러 입자의 운동을, 질량중심 이동과 내부 상대운동으로 나눕니다.',
    'CORE_RELATIONSHIP_EXPLANATION':'Internal forces(내력들)는 전체 힘·모멘트 합에서 상쇄되지만 입자들의 상대운동과 에너지 변화에는 남을 수 있습니다. External forces(외력들)로 mass center(질량중심)의 운동을 구하고, 각운동량·에너지·구속 조건을 결합하여 개별 속도를 결정합니다.',
    'CONCEPT_MAP_HEADLINE':'입자별 운동방정식에서 전체 보존식과 네 예제로.',
    'CONCEPT_MAP_BLOCKS':'<div class="grid-3">'+card('System(계)과 resultant(합력)','내력·외력을 분류하고 전체 합에서 쌍별 상쇄를 확인합니다. L=mvG로 질량중심 이동을 구합니다.')+card('Centroidal motion(질량중심 기준 운동)','회전하지 않는 G 기준계에서 HG=H′G와 운동에너지 분해를 유도합니다.')+card('Conservation(보존)의 적용','선운동량·각운동량·에너지의 조건을 따로 확인하고 방향·상대속도 조건으로 미지수를 연결합니다.')+'</div>',
    'STANDALONE_CONCEPT_SUMMARY':summary,'DISTINCT_SUMMARY_VIDEO_SECTION_IF_NEEDED':roadmap,
    'EXAM_SECTION_TITLE':'입자계의 원리와 풀이 조건을 설명하는 영어 답안',
    'BILINGUAL_GLOSSARY_TABLE':table(['영어(한국어)','의미와 사용'],[(f'{en}({ko})',escape(meaning)) for en,ko,meaning in terms]),
    'AUDIT_SECTION_TITLE':'원본 슬라이드·자동생성 스크립트 교정 기록',
    'ASR_CORRECTION_TABLE':p('원본 PDF와 영어 자동생성 자막은 수정하지 않았습니다. 아래는 본문에 채택한 해석 및 원본 자료와의 불일치입니다. 오표기가 실제 발화인지 자동인식 오류인지는 별도의 음성 판독 없이 단정하지 않습니다. 중요한 수식·조건 불일치는 해당 원본 슬라이드 바로 아래에서도 설명했습니다.')+table(['위치','원문 또는 문제','본문 처리','근거'],audit),
    'SOURCE_LIST_AND_PROVENANCE_NOTE':'<ul class="plain-list"><li>원본 PDF: Lecture 8, MC2103, Fall 2026, 70장.</li>'+''.join(f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상</a> · 영어 자동생성 원문, 2026-10-08 확보.</li>' for label,vid in videos)+'<li>주차·날짜: 보존된 강의 인덱스, Week 07 · 2026-10-14.</li></ul>'+p('원본 70장의 이미지와 영어 자막 5편, 총 1,211개 시간 구간을 대조했습니다. 시간 표시는 관련 설명 구간이며 정확한 슬라이드 전환 시각은 아닙니다. 원본 3장의 보조 링크는 보존하되 그 영상은 설명 근거로 사용하지 않았습니다. 원본 70장의 교재 목록은 보존했으나 교재 본문을 별도로 열람한 것은 아닙니다.')+p('영어 자동자막 원문은 별도 텍스트로 보존했습니다. Summary의 실제 개념 복습은 핵심 개념 요약에 반영하고 다음 단원 안내는 분리했습니다. 생략된 대수 전개, 개념 비교, 수치 검산, 에너지 비율, 이차방정식 근 선택은 시험용 보강 또는 편집자 보강입니다. 원본의 부호·표기·초기 조건 불일치를 원본 이미지 수정 없이 인접 설명에서 구분했습니다.'),
    'TABLE_OF_CONTENTS_LINKS':''.join(f'<li><a href="#{id}">{label}</a></li>' for id,label in toc),
}
for key,value in values.items():
    template = template.replace('{{'+key+'}}',value)
template = template.replace('이 부분만 읽어도 렉처의 핵심 정의, 개념 관계, 가정과 풀이 흐름을 이해할 수 있도록 작성합니다.','입자계의 정의, 질량중심 운동, 두 운동량과 에너지의 보존 조건, 네 예제를 연결한 독립형 요약입니다. 상세한 원본 슬라이드별 해설은 아래에서 별도로 이어집니다.')
template = re.sub(r'\s*<!--[\s\S]*?-->','',template)
template = '\n'.join(line.rstrip() for line in template.splitlines())+'\n'
assert not re.search(r'\{\{[^}]+\}\}',template)
(SITE/'lecture08.html').write_text(template,encoding='utf-8')
print(f'BUILT lecture08.html: {len(records)} source sections, {len(exam_items)} exam cards, {len(terms)} terms')
