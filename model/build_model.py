from pathlib import Path
import json,hashlib,math,sys
from vegetation import Planting
import numpy as np
import trimesh as t
from PIL import Image,ImageOps,ImageDraw,ImageColor
out=Path(__file__).resolve().parent; scene=t.Scene(); records=[]
def box(name,pos,size,color):
 m=t.creation.box(extents=size);m.apply_translation(pos);m.visual.vertex_colors=ImageColor.getrgb(color)+ (255,);scene.add_geometry(m,node_name=name,geom_name=name);records.append({'name':name,'position':pos,'size':size});return m
def cyl(name,pos,r,h,color):
 m=t.creation.cylinder(radius=r,height=h,sections=12);m.apply_transform(t.transformations.rotation_matrix(math.pi/2,[1,0,0]));m.apply_translation(pos);m.visual.vertex_colors=ImageColor.getrgb(color)+ (255,);scene.add_geometry(m,node_name=name,geom_name=name);return m
cream='#ddd5b5';green='#56856c';dark='#333d39';concrete='#a9aaa0';wood='#a47c45'

# Denah supplies topology; map gives overall approximate 31 x 23 m envelope.
# Road/gate +Z. Left when entering is negative X. No internal sketch dimension is surveyed.
box('owner-marked-property',[2,-.12,-11.65],[31.4,.2,23.3],'#92987d')
box('worn-courtyard',[-1,.005,-4.8],[19,.08,9.6],'#b4b0a0')
box('expansion-ground',[13.1,-.005,-11.65],[6.8,.08,23.3],'#7c8b65')
box('backyard-parking-area',[-5.5,.01,-19.3],[14,.08,6.4],'#77775a')
# Side path geometry is built from photo-informed segments below.
box('access-to-backyard',[-5.5,.04,-22.5],[14,.08,1.4],'#b9ae92')
box('road',[2,-.2,5],[42,.12,6],'#636c68');box('brick-sidewalk',[2,-.05,1.1],[34,.12,1.8],'#ac8271');box('tactile-strip',[2,.02,1.4],[34,.025,.3],'#c8ad5b')
# Green sketch boundaries remain tracing strips; front wall is visible in photos.
for x,w in [(-8,11.5),(10,15.4)]:box('front-wall-'+str(x),[x,.62,0],[w,1.25,.16],'#b0b5a9')
for x in [-13.7,17.7]:box('boundary-trace-'+str(x),[x,.09,-11.65],[.12,.15,23.3],'#388b69')
box('boundary-trace-rear',[2,.09,-23.3],[31.4,.15,.12],'#388b69')
box('green-main-gate',[-.3,.75,0],[3.8,1.5,.09],green)
for i in range(10):box('gate-panel-'+str(i),[-2.05+i*.37,.75,.065],[.025,1.45,.02],'#355c4a')
box('pedestrian-gate',[2.1,.72,-.4],[.08,1.45,1.2],green)
# Two attached wings match the owner's L-shaped main-house outline.
def roof(name,x,z,w,d,y=3.2,color='#77634d'):
 rise=.8;half=w/2
 for side in [-1,1]:
  center=[x+side*w/4,y+rise/2,z];m=box(name+'-roof-'+str(side),center,[math.hypot(half,rise),.13,d],color);m.apply_transform(t.transformations.rotation_matrix(-side*math.atan2(rise,half),[0,0,1],point=center))
 # Tile rows: stylized seams, not captured texture.
 for j in range(int(d/.35)):
  zz=z-d/2+j*.35
  for side in [-1,1]:
   center=[x+side*w/4,y+rise/2+.08,zz];m=box(name+'-roof-tile-'+str((j,side)),center,[math.hypot(half,rise),.018,.018],'#5c5141');m.apply_transform(t.transformations.rotation_matrix(-side*math.atan2(rise,half),[0,0,1],point=center))
# Front wall stops at the recessed left bay; do not place a solid wall across its mouth.
box('house-main-front',[1.65,1.5,-10.08],[13.1,3,.16],cream)
box('house-main-back',[0,1.5,-16.45],[16.4,3,.16],cream)
box('house-alcove-left-rear',[-8.2,1.5,-14.025],[.16,3,4.85],cream)
box('house-main-right',[8.2,1.5,-13.05],[.16,3,6.9],cream)
box('house-main-floor',[0,.08,-13.05],[16.4,.16,6.9],'#b5ad95')
roof('house-main',0,-13.05,17,7.6)
# Back wing only on the right side of the house when entering.
box('house-wing-back',[4.2,1.5,-22.5],[8.2,3,.16],cream)
box('house-wing-side',[.1,1.5,-19.5],[.16,3,6.1],cream)
box('house-wing-side-right',[8.3,1.5,-19.5],[.16,3,6.1],cream)
box('house-wing-floor',[4.2,.08,-19.5],[8.2,.16,6.1],'#b5ad95');roof('house-wing',4.2,-19.5,8.8,6.5)
# Visible house front has two dark, unglazed-looking openings, not a row of glazed windows.
for i,x in enumerate([-3.8,-1.4]):
 box('house-window-reveal-'+str(i),[x,1.64,-9.972],[1.6,1.15,.08],'#a5a797')
 box('house-window-opening-'+str(i),[x,1.64,-9.92],[1.4,.95,.025],'#17251e')
# First-day IMG20261027174445 and IMG20261027180232 show a roofed recess, not a flush door.
# Opening width 3.3 m and depth 1.6 m are provisional; depth is adjustable in the viewer.
box('house-alcove-back-wall',[-6.55,1.55,-11.68],[3.3,3.1,.16],'#a9b0aa')
box('house-alcove-stretch-return',[-4.98,1.55,-10.8],[.16,3.1,1.6],'#b7bbb0')
box('house-alcove-stretch-floor',[-6.55,.17,-10.8],[3.3,.12,1.6],'#93988d')
box('house-alcove-step',[-6.55,.1,-9.88],[3.3,.2,.25],'#9b9d8e')
box('house-alcove-stretch-roof',[-6.55,3.12,-10.8],[3.55,.08,1.6],'#87908b')
box('house-alcove-roof-front-overhang',[-6.55,3.07,-9.85],[3.55,.1,.3],'#87908b')
for i,x in enumerate(np.linspace(-8.15,-4.95,13)):
 box('house-alcove-stretch-roof-rib-'+str(i),[float(x),3.18,-10.8],[.025,.035,1.6],'#697775')
for x in [-8.15,-4.95]:box('house-alcove-front-post-'+str(x),[x,1.52,-9.95],[.055,3.04,.055],'#7d8982')
# White-framed window in the right-hand return faces into the recess.
box('house-alcove-stretch-window-dark',[-5.075,1.65,-10.8],[.025,1.55,1.28],'#34453e')
for y in [.85,1.65,2.45]:box('house-alcove-stretch-window-horizontal-'+str(y),[-5.1,y,-10.8],[.05,.055,1.38],'#d2d5c7')
for i,z in enumerate([-10.12,-10.8,-11.48]):box('house-alcove-stretch-window-upright-'+str(i),[-5.1,1.65,z],[.05,1.65,.045],'#d2d5c7')
# Boarded back opening and stored frames from day one; no proposed decoration yet.
box('house-alcove-back-opening',[-6.35,1.1,-11.575],[1.05,1.85,.025],'#525e56')
for i in range(7):box('house-alcove-back-board-'+str(i),[-6.35,.28+i*.25,-11.55],[1.05,.025,.035],'#8d9181')
for x in [-7.7,-6.65]:box('house-alcove-back-stored-frame-side-'+str(x),[x,1.03,-11.25],[.045,1.9,.045],'#a99973')
for y in [.08,1.98]:box('house-alcove-back-stored-frame-cross-'+str(y),[-7.175,y,-11.25],[1.1,.045,.045],'#a99973')
box('house-alcove-back-stored-panel',[-6.05,.46,-11.07],[.65,.9,.06],'#a18551')
# Daylight photo shows low pale slats across stored items near the front.
for y in [.35,.61]:box('house-alcove-stored-low-slat-'+str(y),[-6.35,y,-10.45],[1.45,.2,.075],'#d0c9a4')
for x in [-6.97,-5.73]:box('house-alcove-slat-support-'+str(x),[x,.42,-10.5],[.07,.65,.08],'#78785c')
cyl('house-alcove-aqua-container',[-5.45,.4,-10.65],.19,.55,'#548a81')
# Low eave and a small pale front gable; roof depths remain provisional.
verts=[[-6.6,2.95,-9.94],[-.4,2.95,-9.94],[-3.5,4.65,-9.94]]
m=t.Trimesh(vertices=verts,faces=[[0,1,2]],process=False);m.visual.vertex_colors=ImageColor.getrgb('#c3c5b6')+(255,);scene.add_geometry(m,node_name='house-front-gable',geom_name='house-front-gable')
box('house-front-eave',[-1.95,2.94,-9.7],[5.9,.18,.55],'#737866')
# Narrow side corridor from the first-day photos: pale tiles, cream glazed door.
box('house-corridor-floor',[7.6,.12,-11.4],[1.1,.1,3.6],'#bdb49a')
for z in np.arange(-13.0,-9.6,.4):box('house-corridor-tile-'+str(z),[7.6,.176,float(z)],[1.05,.01,.012],'#918b77')
box('house-corridor-glazed-door',[7.6,1.15,-12.95],[.85,2.2,.06],'#d0cbb0')
for dx in [-.21,.21]:
 for y in [1.3,1.85]:box('house-corridor-glass-'+str((dx,y)),[7.6+dx,y,-12.9],[.36,.45,.025],'#344a43')
# Compact corrugated kiosk reconstructed from 5-6 Nov close-ups.
bx,bz=-7.7,-4.2
box('bar-slab',[bx,.12,bz],[3.5,.2,4.3],'#a7a591')
box('bar-back-wall',[bx-1.4,1.3,bz],[.1,2.6,3.5],cream)
box('bar-side-half-wall',[bx+1.4,.69,bz],[.1,1.14,3.5],cream)
for z in [bz-1.75,bz+1.75]:
 box('bar-end-half-wall-'+str(z),[bx,.69,z],[2.8,1.14,.1],cream)
 for x in [bx-1.4,bx+1.4]:box('bar-green-post-'+str((x,z)),[x,1.35,z],[.065,2.7,.065],'#32815b')
 box('bar-end-top-rail-'+str(z),[bx,2.62,z],[2.85,.06,.065],'#32815b')
for side in [-1,1]:
 box('bar-green-horizontal-rail-'+str(side),[bx+side*1.45,1.25,bz],[.07,.065,3.6],'#32815b')
 box('bar-green-bottom-rail-'+str(side),[bx+side*1.45,.16,bz],[.07,.12,3.6],'#32815b')
for z in np.arange(bz-1.7,bz+1.75,.18):box('bar-panel-seam-'+str(z),[bx+1.46,.7,float(z)],[.018,1.05,.035],'#bbb590')
for x in np.arange(bx-1.35,bx+1.4,.18):box('bar-road-panel-seam-'+str(x),[float(x),.7,bz+1.81],[.035,1.05,.018],'#bbb590')
box('bar-roof',[bx,2.65,bz],[3,.1,3.8],'#bdbea5')
for z in np.arange(bz-1.8,bz+1.9,.2):box('bar-roof-rib-'+str(z),[bx,2.72,float(z)],[2.95,.025,.025],'#a6ad93')
# Quarter-arc turquoise fabric canopy, with scalloped hanging edge.
verts=[];faces=[]
for j in range(17):
 a=j/16*math.pi/2;x=bx+1.4+math.sin(a)*.85;y=2.15+math.cos(a)*.65
 verts.extend([[x,y,bz-1.95],[x,y,bz+1.95]])
for j in range(16):
 k=j*2;faces.extend([[k,k+1,k+2],[k+1,k+3,k+2],[k+2,k+1,k],[k+2,k+3,k+1]])
m=t.Trimesh(vertices=verts,faces=faces,process=False);m.visual.vertex_colors=ImageColor.getrgb('#69b4a3')+(255,);scene.add_geometry(m,node_name='bar-awning-curved',geom_name='bar-awning-curved')
for i in range(13):
 z=bz-1.95+(i+.5)*.3;vs=[[bx+2.255,2.17,z-.15],[bx+2.255,2.17,z+.15]]
 for j in range(9):
  a=j/8*math.pi;vs.append([bx+2.255,2.1-.13*math.sin(a),z+.15*math.cos(a)])
 fs=[[0,k,k+1] for k in range(1,len(vs)-1)];fs+= [[c,b,a] for a,b,c in fs];m=t.Trimesh(vertices=vs,faces=fs,process=False);m.visual.vertex_colors=ImageColor.getrgb('#69b4a3')+(255,);scene.add_geometry(m,node_name='bar-awning-scallop-'+str(i),geom_name='bar-awning-scallop-'+str(i))
box('bar-service-counter',[bx+1.65,1.24,bz],[.6,.075,2.95],'#aa8856')
box('bar-counter-green-edge',[bx+1.98,1.24,bz],[.045,.06,3],'#32815b')
box('bar-counter-inner-step',[bx+1.35,1.45,bz],[.13,.32,2.95],'#c6a36d')
# Menu boards inside the serving opening: simple framed panels, no invented menu text.
for i,z in enumerate([bz-1.15,bz,bz+1.15]):
 box('bar-menu-frame-'+str(i),[bx-1.31,1.85,z],[.05,1.1,.78],'#4c4835');box('bar-menu-paper-'+str(i),[bx-1.27,1.85,z],[.025,1,.7],'#e4dcc0')
box('bar-roadside-counter',[bx,1.02,-1.45],[3.6,.1,.5],wood)
# Furniture helpers retain separate legs, backrests and seat surfaces.
def chair(name,x,z,rotation=0,color='#65503b'):
 before=set(scene.geometry)
 box(name+'-seat',[x,.45,z],[.46,.08,.46],color);box(name+'-back',[x,.78,z-.2],[.46,.55,.06],color)
 for dx in [-.17,.17]:
  for dz in [-.17,.17]:box(name+'-leg-'+str((dx,dz)),[x+dx,.22,z+dz],[.045,.44,.045],dark)
 if rotation:
  for key in set(scene.geometry)-before:scene.geometry[key].apply_transform(t.transformations.rotation_matrix(rotation,[0,1,0],point=[x,0,z]))
def table(name,x,z,w=1.4,d=.7,color='#537567'):
 box(name+'-top',[x,.76,z],[w,.08,d],color)
 for dx in [-w*.4,w*.4]:
  for dz in [-d*.35,d*.35]:box(name+'-leg-'+str((dx,dz)),[x+dx,.37,z+dz],[.055,.74,.055],dark)
def bench(name,x,z,w=1.6):
 box(name+'-seat',[x,.45,z],[w,.09,.42],'#605240');box(name+'-back',[x,.75,z-.2],[w,.5,.06],'#615844')
 for dx in [-w*.4,w*.4]:box(name+'-leg-'+str(dx),[x+dx,.23,z],[.08,.46,.36],dark)
# Current seating: each group matches a black mark; furniture detail follows photos.
table('current-seat-courtyard',-1.6,-8,1.2,.7,'#45483e');bench('current-seat-courtyard-left',-2.7,-8,1.1);bench('current-seat-courtyard-right',-.5,-8,1.1)
for i,x in enumerate([-8.8,-7.7,-6.6]):
 box('current-seat-roadside-stool-'+str(i),[x,.52,-.85],[.45,.08,.4],wood)
 for dx in [-.16,.16]:box('stool-leg-'+str((i,dx)),[x+dx,.26,-.85],[.04,.5,.3],dark)
# Closed area footprint from denah, detailed from 27 Oct photos.
cx,cz=5.1,-5.9
box('closed-area-floor',[cx,.07,cz],[8.2,.14,5],'#9d9d8b')
box('closed-screen-back',[cx,1.4,-8.4],[8.2,2.8,.07],'#2e3530')
box('closed-screen-side',[9.2,1.4,cz],[.07,2.8,5],'#3a3d33')
# The courtyard side (+Z and -X) remains open as in the entrance photographs.
for x in [1,9.2]:
 for z in [-8.4,-3.4]:box('closed-post-'+str((x,z)),[x,1.5,z],[.1,3,.1],dark)
box('closed-roof',[cx,3.05,cz],[8.6,.1,5.4],'#839083')
for x in np.arange(.9,9.4,.22):box('closed-roof-corrugation-'+str(x),[float(x),3.12,cz],[.025,.025,5.3],'#a1aaa0')
for z in [-8.2,-6,-3.6]:box('closed-roof-beam-'+str(z),[cx,2.93,z],[8.5,.1,.08],dark)
bench('closed-back-bench',5.5,-7.7,3.3)
table('closed-green-table',5.2,-5.5,2,.85)
for i,(x,z,r) in enumerate([(3.9,-5.5,-math.pi/2),(6.5,-5.5,math.pi/2),(4.8,-6.4,0),(5.7,-4.6,math.pi)]):chair('closed-wood-chair-'+str(i),x,z,r)
# Cream open display cabinet visible at the back of the seating room.
box('closed-cabinet-back',[2,1.25,-7.95],[1.7,2.5,.06],'#d8d0b2')
for x in [1.15,2.85]:box('closed-cabinet-side-'+str(x),[x,1.25,-7.7],[.08,2.5,.55],'#d8d0b2')
for y in [.12,.8,1.35,1.9,2.5]:box('closed-cabinet-shelf-'+str(y),[2,y,-7.7],[1.7,.06,.55],'#d8d0b2')
for i in range(9):
 x=1.4+(i%3)*.5;y=.93+(i//3)*.55;cyl('closed-cabinet-ceramic-'+str(i),[x,y,-7.55],.09,.2,'#b8b89d')
box('closed-display-case',[7.9,1.2,-7.7],[1.8,.9,.45],'#9c8050');box('closed-display-glass',[7.9,1.2,-7.45],[1.6,.65,.025],'#536453')
for i,y in enumerate([2.2,1.75]):cyl('closed-wall-plate-'+str(i),[7,y,-8.28],.18,.04,'#c7c7ac')
table('current-seat-closed-front',6.7,-2,1.4,.7);chair('current-seat-closed-chair',6.7,-1.2,math.pi)
# Fine, exportable foliage keeps the existing planting layout; no sphere/disc proxies.
plants=Planting(scene);rng=np.random.default_rng(1106)
for i,(x,z,r,h) in enumerate([(2.3,-2,1.9,5.7),(-4,-1.6,1.6,5.2),(-4.4,-8.4,1.5,5),(10.3,-8.5,1.8,5.8)]):
 if i==2:continue
 plants.tree('tree-crown-'+str(i),x,z,h,r,mature=True)
box('tree-brick-base',[2.3,.13,-2],[1.25,.25,1.25],'#a4836b')
for i,(x,z) in enumerate([(-3,-9),(3,-9),(7,-9),(-4.5,-6.8),(1.2,-3.3),(9,-3.3)]):
 cyl('plant-pot-'+str(i),[x,.2,z],.23,.4,'#9c7751')
 plants.shrub('plant-foliage-'+str(i),x,.6,z,.28)
# Mixed low growth over soil, leaving the existing worn route through the yard.
for i in range(220):
 x=float(rng.uniform(-12.3,1));z=float(rng.uniform(-21.6,-16.9))
 if -5.3<x<-4.3:continue
 plants.grass('garden-grass',x,z,.5,.45,90)
for i,(x,z,h) in enumerate([(-10.5,-18,3.8),(-8.6,-20.4,4.2),(-3.2,-18.7,4.3),(-.5,-20.5,3.5),(-11.8,-21,3.8)]):
 plants.tree('garden-sapling-'+str(i),x,z,h,.95,red=True)
for i in range(20):
 x=float(rng.uniform(-12.1,1));z=float(rng.uniform(-21.5,-16.9))
 plants.shrub('garden-shrub-'+str(i),x,.3,z,.38)
# Preserve the approved frontage bed outline and edge stones.
edge=[(-8.1,-7.9),(-6.7,-7.75),(-5.4,-8.1),(-4.4,-8.55),(-3.1,-8.8),(-2.1,-9.05),(-.3,-9.03),(.5,-9.15)]
for i,((x,z),(xx,zz)) in enumerate(zip(edge,edge[1:])):
 m=t.Trimesh(vertices=[[x,.065,-9.95],[x,.065,z],[xx,.065,zz],[xx,.065,-9.95]],faces=[[0,1,2],[0,2,3]],process=False)
 m.visual.vertex_colors=ImageColor.getrgb('#777762')+(255,);scene.add_geometry(m,node_name='house-front-soil-'+str(i),geom_name='house-front-soil-'+str(i))
 for j in range(5):
  f=(j+.5)/5;box('house-front-edge-stone-'+str((i,j)),[x+(xx-x)*f,.09,z+(zz-z)*f],[float(rng.uniform(.1,.28)),.07,float(rng.uniform(.08,.17))],['#8e9181','#a6a28a'][j%2])
for i in range(650):
 x=float(rng.uniform(-8,.4));z=float(rng.uniform(-9.75,-7.9))
 boundary=float(np.interp(x,[v[0] for v in edge],[v[1] for v in edge]))
 if z>boundary-.1:continue
 plants.grass('house-front-grass',x,z,.09,.08,12,y=.07)
for i,(x,z,h,w) in enumerate([(-5.1,-9.05,3.05,.9),(-3.95,-9.25,3.5,1.0),(-1.05,-9.3,3.4,.95)]):
 plants.tree('house-front-tree-'+str(i),x,z,h,w,red=True)
for i,(x,z) in enumerate([(-7.3,-9.5),(-5.4,-9.6),(-4.8,-9.25),(-3,-9.55),(-2.5,-9.65),(-.1,-9.6)]):
 plants.shrub('house-front-underplant-'+str(i),x,.26,z,.3)
box('garden-weathered-ladder',[-2.2,.15,-17],[3,.1,.45],'#6e644a')
for x in np.arange(-3.5,-.7,.35):box('garden-ladder-rung-'+str(x),[float(x),.23,-17],[.08,.06,.65],'#6e644a')
cyl('garden-blue-barrel',[.5,.5,-20],.36,1,'#427f8a')
# Side-strip correction: bar moves out toward the boundary instead of leaving a broad empty lane.
for name,m in list(scene.geometry.items()):
 if name.startswith(('bar-','current-seat-roadside','stool-leg')):m.apply_translation([-2.9,0,0])
# Narrow concrete seating strip between corrugated kiosk and existing low wall.
box('side-access-path',[-12.72,.045,-3.25],[1.65,.1,6.5],'#a4a69a')
box('side-low-grey-wall',[-13.6,.45,-4.6],[.18,.9,9.2],'#858f86')
box('neighbor-white-wall',[-14.05,1.65,-4.6],[.2,3.3,9.2],'#d0d0be')
# Behind the kiosk the strip bends inward, then continues toward the planted yard.
def path_segment(name,a,b,width):
 delta=np.array(b)-np.array(a);mid=(np.array(a)+np.array(b))/2
 m=box(name,[mid[0],.045,mid[1]],[width,.1,float(np.linalg.norm(delta))],'#a4a69a');angle=math.atan2(delta[0],delta[1]);m.apply_transform(t.transformations.rotation_matrix(angle,[0,1,0],point=[mid[0],.045,mid[1]]))
path_segment('side-path-bend',[-12.72,-6.5],[-11.1,-8.2],1.05)
path_segment('side-path-to-yard',[-11.1,-8.2],[-11.1,-16.1],1.05)
# Photo shows a table between opposing dark slab-like benches, rather than two picnic sets.
table('side-strip-current-table',-12.7,-3.7,1.28,.68,'#555a50')
bench('side-strip-bench-front',-12.7,-2.8,1.35)
bench('side-strip-bench-back',-12.7,-4.65,1.35)
# Reverse the nearer bench so the two backrests face away from the table.
for name,m in scene.geometry.items():
 if name.startswith('side-strip-bench-front'):m.apply_transform(t.transformations.rotation_matrix(math.pi,[0,1,0],point=[-12.7,0,-2.8]))
# Dark worn wood and greying concrete edges shown in the originals.
for name,m in scene.geometry.items():
 if name.startswith('side-strip-bench'):m.visual.vertex_colors=ImageColor.getrgb('#444c42')+(255,)
for i in range(32):
 z=-.2-i*.19;x=-13.45 if i%2 else -12.02
 box('side-path-edge-chip-'+str(i),[x,.102,z],[.08,.015,.08],'#7c8176')
for i in range(6):
 z=-.7-i*.93;m=box('side-path-crack-'+str(i),[-12.7,.101,z],[.95,.008,.012],'#767d70');m.apply_transform(t.transformations.rotation_matrix(.2*(i%3-1),[0,1,0],point=[-12.7,.101,z]))
# Tree/plant obstruction at the back of the seating strip, seen on both visits.
plants.tree('side-strip-tree',-12.68,-6.25,3.05,.78)
for i in range(10):plants.shrub('side-strip-underplant-'+str(i),-13.2+(i%3)*.35,.25,-6.4-(i//3)*.4,.26)
plants.flush()
# Thin fence wires along low wall are architectural context from the photographs.
for y in [1.12,1.4]:
 for i in range(5):box('side-fence-wire-'+str((y,i)),[-13.6,y,-.9-i*1.8],[.014,.014,1.8],'#686b55')
for z in [-.2,-3.4,-6.8,-9]:box('side-fence-post-'+str(z),[-13.6,1.12,z],[.035,.75,.035],'#526c56')
# Register source limits with the portable model.
scene.metadata={'title':'JoyBromo current site - owner denah revision','units':'meters','source':'Owner illustrated denah, annotated satellite scale, 27 Oct and 5-6 Nov photos','gate_to_house_default_m':10,'alcove_depth_estimate_m':1.6,'alcove_future_use':'Owner intends an Instagram photo spot; current recess shown without proposed decoration','layout':'L-shaped house; parking behind bar; expansion beyond house/closed area; road at front','limits':'Sketch topology authoritative; sketch proportions not surveyed. Interior detail photo-informed, hidden rooms not reconstructed. 60 cm tape is a local reference, not global calibration.'}
scene.export(out.parent/'dist/model.glb')
(out/'geometry-register.json').write_text(json.dumps({'metadata':scene.metadata,'elements':[{'name':name,'bounds':m.bounds.tolist()} for name,m in scene.geometry.items()]},indent=2))
# Draw an actual orthographic projection of the exported model geometry.
# Orthographic painter projection from the actual mesh triangles.
if '--skip-preview' not in sys.argv:
 canvas=Image.new('RGB',(1600,1200),'#eeeee5');draw=ImageDraw.Draw(canvas)
 right=np.array([.8,0,-.6]);up=np.array([-.3,.866,-.4]);depth=np.cross(right,up)
 pixels=np.array(canvas);zbuf=np.full((1200,1600),-np.inf)
 for name,m in scene.geometry.items():
  for face,col in zip(m.faces,m.visual.face_colors):
   pts=m.vertices[face];normal=np.cross(pts[1]-pts[0],pts[2]-pts[0]);norm=np.linalg.norm(normal)
   if norm:normal=normal/norm
   shade=.68+.32*abs(np.dot(normal,np.array([.3,.85,.43])))
   color=np.minimum(255,col[:3]*shade).astype(np.uint8)
   xy=np.array([(800+float(v@right)*30,650-float(v@up)*30) for v in pts]);zz=pts@depth
   xmin=max(0,int(np.floor(xy[:,0].min())));xmax=min(1599,int(np.ceil(xy[:,0].max())));ymin=max(0,int(np.floor(xy[:,1].min())));ymax=min(1199,int(np.ceil(xy[:,1].max())))
   if xmax<xmin or ymax<ymin:continue
   x0,y0=xy[0];x1,y1=xy[1];x2,y2=xy[2];den=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
   if abs(den)<1e-8:continue
   yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];a=((y1-y2)*(xx-x2)+(x2-x1)*(yy-y2))/den;b=((y2-y0)*(xx-x2)+(x0-x2)*(yy-y2))/den;c=1-a-b
   z=a*zz[0]+b*zz[1]+c*zz[2];patch=zbuf[ymin:ymax+1,xmin:xmax+1];mask=(a>=-1e-8)&(b>=-1e-8)&(c>=-1e-8)&(z>patch);patch[mask]=z[mask];pixels[ymin:ymax+1,xmin:xmax+1][mask]=color
 canvas=Image.fromarray(pixels);draw=ImageDraw.Draw(canvas)
 draw.text((45,35),'JOYBROMO / EXISTING SITE / 06 NOV 2026',fill='#314d3b',font_size=28)
 draw.text((45,80),'Owner denah layout + photo-informed interior. Gate to house default 10 m; other dimensions approximate.',fill='#536451',font_size=20)
 canvas.save(out/'existing-overview.png')
print('Exported',len(scene.geometry),'mesh parts to dist/model.glb.')
