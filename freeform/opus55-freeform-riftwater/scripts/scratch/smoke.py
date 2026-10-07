# Scratch: the first test of the writer bridge — stairs of every data value, a chest and a sign on a slab.
# python3 scratch/smoke.py; then dotnet run write_world.cs -- /tmp/claude-0/rw/smoke <out-world>
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from mc import World, B
w = World(-16, -16, 32, 32, sy=32)
w.fill(-16,0,-16,15,9,15,B.STONE); w.fill(-16,10,-16,15,10,15,B.GRASS)
for d in range(8):
    w.set(-8+2*d, 11, 0, B.OAK_STAIRS, d)
w.chest(0,11,4,[(0,'minecraft:iron_ingot',5,0)])
w.sign(2,11,4,["hello","world"],rot=8)
w.save('/tmp/claude-0/rw/smoke', 'smoke', (0,12,0))
