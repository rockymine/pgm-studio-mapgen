#!/usr/bin/env bash
# Regenerate Penstock from nothing: generate the volume, write the region files, draw the renders, walk it.
#   scripts/build.sh [build-dir]        (python3 with numpy, scipy, pillow; dotnet 10; the studio at
#                                        /home/user/pgm-studio with tools/PgmStudio.RoundTrip built)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(dirname "$here")"
build="${1:-/tmp/penstock-build}"
RT="dotnet /home/user/pgm-studio/tools/PgmStudio.RoundTrip/bin/Debug/net10.0/PgmStudio.RoundTrip.dll"

cd "$here"
mkdir -p "$root/renders"
python3 gen.py "$build"
rm -rf "$root/world/region"
(cd /tmp && dotnet run "$here/write_world.cs" -- "$build" "$root/world")
cp "$here/map.xml" "$root/world/map.xml"
python3 levels.py "$build" "$root/renders/00-plan-levels.png"
python3 renders.py "$build" "$root" "$RT"
python3 walk.py "$build" > "$root/renders/walks.txt"; cat "$root/renders/walks.txt"
