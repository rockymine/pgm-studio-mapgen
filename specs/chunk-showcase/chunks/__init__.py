"""Every chunk on the showcase, in the order the board lays them out (four to a row). A chunk whose module does
not build is reported and left out, so one unfinished chunk never stops the others."""
import importlib
import os
import sys

ORDER = ["crypt", "camp", "wizard-tower", "fishing-hut", "mine", "windmill", "forge", "oasis",
         "lighthouse", "graveyard", "outpost", "jungle-shrine"]

ALL = []
for _name in ORDER:
    _module = _name.replace("-", "_")
    if not os.path.exists(os.path.join(os.path.dirname(__file__), f"{_module}.py")):
        continue
    try:
        ALL.append(importlib.import_module(f"chunks.{_module}").build())
    except Exception as fault:                       # noqa: BLE001 -- report and carry on
        print(f"  ! chunk {_name} left out: {type(fault).__name__}: {fault}", file=sys.stderr)
