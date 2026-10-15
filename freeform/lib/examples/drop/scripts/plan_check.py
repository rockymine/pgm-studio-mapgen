"""Check Drop's course: every link's gap and drop, the gentlest way across, and the fall damage."""
from plan import HEALTH, build

C = build()
rows = C.audit(HEALTH)
print(f"{'from':<24}{'to':<26}{'gap':>5}{'drop':>6}  {'how':<12}{'spare':>6}{'damage':>8}")
for r in rows:
    print(f"{r['a']:<24}{r['b']:<26}{r['gap']:>5.1f}{r['drop']:>6}  {str(r['how']):<12}{r['spare']:>6}"
          f"{r['damage']:>6}  lands {r['lands']}{' in water' if r['water'] else ''}"
          f"{'' if r['on_piece'] else '  OFF THE PIECE'}{'  LETHAL' if r['lethal'] else ''}")
print(f"links that nothing clears: {sum(r['how'] is None for r in rows)}")
print(f"lethal links: {sum(r['lethal'] for r in rows)}")
print(f"landings off the piece: {sum(not r['on_piece'] for r in rows if r['how'])}")
