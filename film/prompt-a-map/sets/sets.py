import json, math, random
def fill(x0,y0,z0,x1,y1,z1,i,d=0): return [x0,y0,z0,x1,y1,z1,i,d]
def blk(x,y,z,i,d=0): return [x,y,z,i,d]
W=35
# ---------------- studio ----------------
s=[]
s.append(fill(-34,0,-14,34,0,22,155,0))                      # quartz floor
for x in range(-34,35):
    for z in range(-14,23):
        if (x//3+z//3)%2==0 and abs(x)>7: s.append(blk(x,0,z,W,0))   # white wool checker (subtle)
# sunburst backdrop at z=22
for x in range(-34,35):
    for y in range(1,30):
        a=math.atan2(y-7, x)
        ray=int(math.floor(a/(math.pi/14)))
        r=math.hypot(x,y-7)
        if r<6.2: i,d=W,14           # red sun disc
        elif r<7.4: i,d=W,0
        else: i,d=(W,4) if ray%2==0 else (W,1)
        s.append(blk(x,y,22,i,d))
s.append(fill(-34,1,22,34,1,22,W,11)); s.append(fill(-34,29,22,34,30,22,W,11))
# side wings
for sx in (-1,1):
    s.append(fill(sx*34,1,-14,sx*34,30,22,W,11))
    for y in range(1,30,4): s.append(fill(sx*34,y,-14,sx*34,y,22,W,4))
# podium: gold disc
for x in range(-6,7):
    for z in range(2,15):
        r=math.hypot(x,z-8)
        if r<=5.3: s.append(blk(x,1,z,41,0))
        elif r<=6.3: s.append(blk(x,1,z,W,14))
# footlights
for x in range(-30,31,3): s.append(blk(x,1,-3,89,0))
# the machine (stage left of camera = +x? put at x 13..19)
s.append(fill(12,1,8,20,1,16,42,0))
s.append(fill(13,2,9,19,8,15,42,0))
for y in range(2,9):
    for x in range(13,20):
        if (x+y)%2==0: s.append(blk(x,y,9,124,0))
        else: s.append(blk(x,y,9,123,0))
s.append(fill(15,4,9,17,6,9,152,0)); s.append(blk(16,5,9,57,0))
s.append(fill(14,9,10,18,9,14,152,0)); s.append(fill(16,10,12,16,13,12,42,0)); s.append(blk(16,14,12,124,0))
# product stacks (stage right)
for (x,z,h,i,d) in [(-14,10,3,47,0),(-16,11,5,47,0),(-18,10,2,46,0),(-15,13,4,133,0),(-19,13,6,47,0),(-12,13,1,46,0)]:
    s.append(fill(x,1,z,x+1,h,z+1,i,d))
json.dump(s,open('studio.json','w'))
# ---------------- machine room ----------------
random.seed(7); m=[]
L=46
m.append(fill(-8,0,-4,8,0,L,42,0)); m.append(fill(-8,11,-4,8,11,L,98,0))
for z in range(-4,L+1):
    for y in range(1,11):
        for sx in (-8,8):
            r=random.random()
            if y in (1,10): i,d=98,0
            elif z%6==0: i,d=42,0
            elif r<.33: i,d=124,0
            elif r<.6: i,d=123,0
            elif r<.8: i,d=47,0
            elif r<.9: i,d=152,0
            else: i,d=22,0
            m.append(blk(sx,y,z,i,d))
for z in range(0,L,6):
    m.append(fill(-2,11,z,2,11,z,89,0)); m.append(fill(-8,0,z,8,0,z,152,0))
# end wall: the Machine's face
m.append(fill(-8,1,L,8,10,L,42,0))
for x in range(-6,7):
    for y in range(2,10):
        m.append(blk(x,y,L-1,124 if (x*y)%3 else 123,0))
m.append(fill(-4,6,L-2,-2,8,L-2,57,0)); m.append(fill(2,6,L-2,4,8,L-2,57,0))   # eyes
m.append(fill(-3,3,L-2,3,4,L-2,49,0))                                           # mouth slot
m.append(fill(-8,1,-4,8,10,-4,98,0))
json.dump(m,open('machine.json','w'))
# ---------------- awards stage ----------------
a=[]
a.append(fill(-30,0,-12,30,0,20,W,15)); a.append(fill(-3,0,-12,3,0,20,W,14))    # black floor, red carpet
for x in range(-30,31):
    for y in range(1,26):
        i,d=W,15
        if (x*7+y*13)%23==0: i,d=89,0                 # stars
        if abs(x) in (29,30) or y in (25,): i,d=41,0
        a.append(blk(x,y,20,i,d))
for sx in (-1,1): a.append(fill(sx*30,1,-12,sx*30,25,20,W,15))
a.append(fill(-8,1,10,8,1,19,W,14)); a.append(fill(-7,2,12,7,2,19,41,0))           # steps
# trophy: gold cup behind the host
cx,cz=0,16
a.append(fill(cx-2,3,cz-2,cx+2,3,cz+2,42,0)); a.append(fill(cx-1,4,cz-1,cx+1,5,cz+1,41,0)); a.append(fill(cx,6,cz,cx,8,cz,41,0))
for y in range(9,15):
    r=2+ (y-9)//2
    for x in range(-r,r+1):
        for z in range(-r,r+1):
            if max(abs(x),abs(z))==r or y==9: a.append(blk(cx+x,y,cz+z,41,0))
for sx in (-1,1):
    for y in range(11,14): a.append(blk(cx+sx*6,y,cz,41,0))
    a.append(blk(cx+sx*5,11,cz,41,0)); a.append(blk(cx+sx*5,13,cz,41,0))
for x in range(-24,25,6): a.append(blk(x,1,-2,169,0))
json.dump(a,open('awards.json','w'))
json.dump([{"name":"studio-a","w":1280,"h":720,"from":{"x":0,"y":5,"z":-8,"yaw":0,"pitch":4,"fov":62}},
           {"name":"studio-b","w":1280,"h":720,"from":{"x":-4,"y":4.2,"z":-1,"yaw":-18,"pitch":2,"fov":60}}],open('studio.jobs.json','w'))
json.dump([{"name":"machine-a","w":1280,"h":720,"from":{"x":0,"y":4,"z":0,"yaw":0,"pitch":2,"fov":75}},
           {"name":"machine-b","w":1280,"h":720,"from":{"x":0,"y":5,"z":30,"yaw":0,"pitch":0,"fov":70}}],open('machine.jobs.json','w'))
json.dump([{"name":"awards-a","w":1280,"h":720,"from":{"x":0,"y":5.5,"z":-6,"yaw":0,"pitch":2,"fov":60}}],open('awards.jobs.json','w'))
