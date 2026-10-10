#!/usr/bin/env bash
# Regenerate Hollow Mesa from nothing: audit the placements, generate the volume, write the region files,
# draw the renders, walk the routes.
#   scripts/build.sh [build-dir]        (python3 with numpy, scipy, pillow; dotnet 10; the studio at
#                                        /home/user/pgm-studio with tools/PgmStudio.RoundTrip built)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(dirname "$here")"
world="$(python3 "$root/../../tools/worlds.py" of "$root")"
build="${1:-/tmp/hollow-mesa-build}"
RT="dotnet /home/user/pgm-studio/tools/PgmStudio.RoundTrip/bin/Debug/net10.0/PgmStudio.RoundTrip.dll"

cd "$here"
python3 audit.py > "$root/renders/audit.txt"
cat "$root/renders/audit.txt"
python3 gen.py "$build"
dotnet run write_world.cs -- "$build" "$world"
cp "$here/map.xml" "$world/map.xml"
python3 renders.py "$build" "$root" "$RT"
python3 annotate.py "$build" "$root/renders/05-topdown-annotated.png"
python3 walk.py "$build" > "$root/renders/walks.txt"
