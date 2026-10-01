"""The words a board is stated in: `GET /api/kit.py`, which the studio writes from its own schema — a constructor per
shape a route takes, `library()` and `use()` for a name, and `Studio` for every route
(`pgm-studio/docs/architecture.md`). A build-spec takes it from here:

    sys.path.insert(0, os.path.join(ROOT, "tools"))
    from studio_kit import kit

    kit.SolidMaterial(id=1, data=5)
    kit.library("brick-roofed-stone-and-dark-oak-house")

**A kit is one studio's words, so it is asked of the studio the board is driven against** — the one `drive.py`
resolves — and kept under `out/kit/<hash>.py`, the hash being the `ETag` that studio answers it with. A studio whose
schema has moved on answers another hash, and a board is stated in its words from then on.
"""
import importlib.util, os, re, urllib.request
import drive

KEPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", "kit")


def _load():
    request = urllib.request.Request(drive.endpoint() + "/kit.py", headers=drive.signed({}))
    with urllib.request.urlopen(request, timeout=120) as answer:
        source = answer.read()
        hashed = re.sub(r"[^0-9a-f]", "", (answer.headers.get("ETag") or "").lower()) or "unhashed"
    os.makedirs(KEPT, exist_ok=True)
    path = os.path.join(KEPT, f"{hashed}.py")
    written = f"{path}.{os.getpid()}"
    with open(written, "wb") as handle:
        handle.write(source)
    os.replace(written, path)
    spec = importlib.util.spec_from_file_location("kit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


kit = _load()
