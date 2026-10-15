"""Minecraft 1.8 player flight after a velocity is set: per tick move, then vy=(vy-0.08)*0.98, vh*=0.91 (air)."""
import math, sys
def fly(p, v, land_y=None, ticks=200, inp=0.0):
    x, y, z = p; vx, vy, vz = v
    path=[(0,x,y,z)]; apex=y
    for t in range(1, ticks):
        x += vx; y += vy; z += vz
        apex=max(apex,y)
        path.append((t,x,y,z))
        vy = (vy - 0.08) * 0.98
        vx *= 0.91; vz *= 0.91
        if land_y is not None and vy < 0 and y <= land_y:
            return t, x, y, z, apex, path
    return None, x, y, z, apex, path
if __name__ == "__main__":
    for name, p, v, land in [("mush a-left-to-mid", (-441.5,13,-325.5),(2.4,0.9,-2.4),14),
                             ("mush mid-to-a-right",(-390.5,15,-304.5),(-3.2,0.8,3.2),12),
                             ("mush a-bottom",(-436.5,3,-291.5),(-0.2,1.7,0.2),12)]:
        r=fly(p,v,land)
        t,x,y,z,apex,_=r
        print(f"{name}: lands after {t} ticks at ({x:.1f},{y:.1f},{z:.1f}), {math.hypot(x-p[0],z-p[2]):.1f} blocks out, apex {apex:.1f}")
