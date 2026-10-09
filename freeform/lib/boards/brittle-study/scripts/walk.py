"""Read the study back: nothing falls or hangs on nothing, no water stands against air.

    python3 walk.py <build-dir>
"""
import sys

from pgmvox import World, audit

w = World.load(sys.argv[1])
foot = audit.footing(w)
print(f"footing problems (audit.footing): {len(foot)}")
for f in foot[:10]:
    print("  ", f)
print(f"water standing against air (audit.loose_water): {len(audit.loose_water(w))}")
