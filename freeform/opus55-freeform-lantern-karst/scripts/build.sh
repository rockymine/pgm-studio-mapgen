#!/usr/bin/env bash
# Regenerate Lantern Karst from nothing: measure the plan, generate the volume, write the region files, draw
# the renders, walk the routes.
#   scripts/build.sh [build-dir]        (python3 with numpy, scipy, pillow; dotnet 10; the studio at
#                                        /home/user/pgm-studio with tools/PgmStudio.RoundTrip built)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(dirname "$here")"
world="$(python3 "$root/../../tools/worlds.py" of "$root")"
build="${1:-/tmp/lantern-karst-build}"
RT="dotnet /home/user/pgm-studio/tools/PgmStudio.RoundTrip/bin/Debug/net10.0/PgmStudio.RoundTrip.dll"

cd "$here"
mkdir -p "$root/renders"
python3 plan_check.py > "$root/renders/plan-check.txt"; cat "$root/renders/plan-check.txt"
python3 sketch.py "$root/renders/00-plan-sketch.png"
python3 gen.py "$build"
rm -rf "$world/region"
(cd /tmp && dotnet run "$here/write_world.cs" -- "$build" "$world")
cp "$here/map.xml" "$world/map.xml"
python3 renders.py "$build" "$root" "$RT"
python3 walk.py "$build" > "$root/renders/walks.txt"; cat "$root/renders/walks.txt"
