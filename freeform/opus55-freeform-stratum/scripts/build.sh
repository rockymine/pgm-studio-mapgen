#!/usr/bin/env bash
# Regenerate Stratum from nothing: audit the placements, generate the volume, write the region files,
# draw the renders, walk the routes.
#   scripts/build.sh [build-dir]        (python3 with numpy, scipy, pillow; dotnet 10; the studio at
#                                        /home/user/pgm-studio with tools/PgmStudio.RoundTrip built)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(dirname "$here")"
world="$(python3 "$root/../../tools/worlds.py" of "$root")"
build="${1:-/tmp/stratum-build}"
RT="dotnet /home/user/pgm-studio/tools/PgmStudio.RoundTrip/bin/Debug/net10.0/PgmStudio.RoundTrip.dll"

cd "$here"
mkdir -p "$root/renders"
if [ -f audit.py ]; then python3 audit.py > "$root/renders/audit.txt"; cat "$root/renders/audit.txt"; fi
python3 gen.py "$build"
(cd /tmp && dotnet run "$here/write_world.cs" -- "$build" "$world")
cp "$here/map.xml" "$world/map.xml"
python3 renders.py "$build" "$root" "$RT"
if [ -f annotate.py ]; then python3 annotate.py "$build" "$root/renders/05-topdown-annotated.png"; fi
if [ -f walk.py ]; then python3 walk.py "$build" > "$root/renders/walks.txt"; cat "$root/renders/walks.txt"; fi
