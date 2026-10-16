"""Check Thawline's plan: every measurement checks.py makes, its value beside its target."""
import checks

rows, _ = checks.measure()
for value, what, target, ok in rows:
    print(f"{'ok  ' if ok else 'MISS'} {value!s:>12}  {what}  (target {target})")
