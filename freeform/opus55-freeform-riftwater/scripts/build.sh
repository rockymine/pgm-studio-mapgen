#!/usr/bin/env bash
# Regenerate Riftwater from nothing: generate the volume, write the region files, draw the renders.
#   scripts/build.sh [build-dir]        (needs python3 with numpy, scipy, pillow; dotnet 10; the studio at
#                                        /home/user/pgm-studio with tools/PgmStudio.RoundTrip built)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(dirname "$here")"
build="${1:-/tmp/riftwater-build}"
RT="dotnet /home/user/pgm-studio/tools/PgmStudio.RoundTrip/bin/Debug/net10.0/PgmStudio.RoundTrip.dll"

cd "$here"
python3 gen.py "$build"
dotnet run write_world.cs -- "$build" "$root/world"
cp "$here/map.xml" "$root/world/map.xml"
python3 renders.py "$build" "$root" "$RT"
python3 annotate.py "$build" "$root/renders/05-topdown-annotated.png"
python3 walk.py "$build" > "$root/renders/walks.txt"
