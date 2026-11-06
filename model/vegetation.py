"""Deterministic, exportable foliage: fine leaves and grass, batched by plant and shade."""
import math
import numpy as np
import trimesh as t
from PIL import ImageColor

class Planting:
 def __init__(self,scene):
  self.scene=scene;self.rng=np.random.default_rng(61108);self.batches={}
 def mesh(self,name,vertices,faces,color):
  key=(name,color);v,f=self.batches.setdefault(key,([],[]));offset=len(v);v.extend(vertices);f.extend([[offset+i for i in face] for face in faces])
 def leaf(self,name,base,direction,length,width,color):
  direction=np.array(direction,dtype=float);direction/=np.linalg.norm(direction)
  normal=np.cross(direction,[1,0,.3]);normal/=np.linalg.norm(normal);side=np.cross(direction,normal)
  base=np.array(base);mid=base+direction*length*.48
  verts=np.array([base,mid+side*width,mid+normal*length*.06,mid-side*width,base+direction*length-normal*length*.1])
  faces=[[0,1,2],[0,2,3],[1,4,2],[2,4,3]]
  # Two thin surfaces retain both sides in standalone GLB as well as the web viewer.
  self.mesh(name,np.concatenate([verts,verts-normal*.0015]),faces+[[c+5,b+5,a+5] for a,b,c in faces],color)
 def stem(self,name,a,b,r1,r2):
  a=np.array(a);b=np.array(b);d=b-a;length=np.linalg.norm(d)
  m=t.creation.conical_frustum(radius_base=r1,radius_top=r2,height=length,sections=8) if hasattr(t.creation,'conical_frustum') else t.creation.cylinder(radius=r1,height=length,sections=8)
  # Taper cylinder vertices explicitly; trimesh versions differ on frustum availability.
  if not hasattr(t.creation,'conical_frustum'):
   top=m.vertices[:,2]>0;m.vertices[top,:2]*=r2/r1
  m.apply_transform(t.geometry.align_vectors([0,0,1],d));m.apply_translation((a+b)/2)
  self.mesh(name,m.vertices,m.faces,'#756c57')
 def cluster(self,name,center,radii,count,red=False):
  palette=['#354d2e','#425e35','#52703f','#637e48','#728953']
  for j in range(count):
   d=self.rng.normal(size=3);d/=np.linalg.norm(d);q=self.rng.random()**.4
   point=np.array(center)+d*np.array(radii)*q
   angle=self.rng.uniform(0,math.tau);pitch=self.rng.uniform(-.45,.6)
   size=self.rng.uniform(.09,.18)
   color=palette[j%5]
   if red and d[1]>.45 and j%6==0:color=['#96714e','#9b8357'][j%2]
   self.leaf(name,point,[math.cos(angle),pitch,math.sin(angle)],size,size*.22,color)
 def tree(self,name,x,z,h,r,mature=False,red=False):
  trunk=name+'-wood';crown=name+'-leaves'
  # Bent, tapering leader and irregular secondary branches; roots keep previous positions.
  points=[[x,.08,z],[x-.07,h*.28,z+.04],[x+.09,h*.52,z-.08],[x-.06,h*.8,z+.02]]
  radius=.19 if mature else .047
  for i in range(3):self.stem(trunk,points[i],points[i+1],radius*(1-i*.27),radius*(.72-i*.22))
  for j in range(9 if mature else 7):
   a=j*2.399+self.rng.uniform(-.2,.2);reach=r*self.rng.uniform(.45,.85)
   end=[x+math.cos(a)*reach,h*(.7+self.rng.uniform(0,.23)),z+math.sin(a)*reach]
   origin=points[1 if j<3 else 2]
   mid=(np.array(origin)+end)/2;mid[1]+=.15
   self.stem(trunk,origin,mid,radius*.45,radius*.2);self.stem(trunk,mid,end,radius*.2,.008)
   self.cluster(crown,end,[r*.58,h*.15,r*.48],460 if mature else 330,red)
   for k in range(2):
    tip=np.array(end)+self.rng.uniform(-.24,.24,3);self.stem(crown,end,tip,.009,.003)
 def shrub(self,name,x,y,z,r=.35):
  for j in range(7):
   a=j*2.4;tip=[x+math.cos(a)*r*.55,y+r*.65,z+math.sin(a)*r*.55]
   self.stem(name,[x,y-r*.5,z],tip,.009,.002)
   self.cluster(name,tip,[r*.55,r*.45,r*.5],45)
 def grass(self,name,x,z,rx,rz,count,y=.06):
  palette=['#596746','#66734d','#78805a','#4c603e','#87886a']
  for j in range(count):
   a=self.rng.uniform(0,math.tau);radius=self.rng.random()**.5
   base=np.array([x+math.cos(a)*radius*rx,y,z+math.sin(a)*radius*rz]);h=self.rng.uniform(.025,.14)
   angle=self.rng.uniform(0,math.tau);side=np.array([math.cos(angle),0,math.sin(angle)])*self.rng.uniform(.003,.008)
   bend=np.array([math.sin(angle),0,-math.cos(angle)])*h*self.rng.uniform(.1,.6)
   verts=np.array([base-side,base+side,base+np.array([0,h*.55,0])+bend*.3-side*.55,base+np.array([0,h*.55,0])+bend*.3+side*.55,base+[0,h,0]+bend])
   fs=[[0,1,2],[1,3,2],[2,3,4]]
   self.mesh(name,np.concatenate([verts,verts+[0,0,.0007]]),fs+[[c+5,b+5,a+5] for a,b,c in fs],palette[j%5])
 def flush(self):
  for (name,color),(verts,faces) in self.batches.items():
   m=t.Trimesh(vertices=verts,faces=faces,process=False);m.visual.vertex_colors=ImageColor.getrgb(color)+(255,)
   label=name+'-'+color[1:];self.scene.add_geometry(m,node_name=label,geom_name=label)
