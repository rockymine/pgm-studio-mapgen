#!/usr/bin/env bash
# Rebuilds ../index.html from the Riftwater port: the ground and the world step by step, the pictures, the page.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out/img
python3 heights.py "$PWD/out/stack.pkl"
python3 worldsteps.py "$PWD/out/world.pkl"
python3 frames.py
python3 overlay.py
python3 forms.py
python3 soft.py
python3 melt.py
python3 paint.py
python3 page.py
