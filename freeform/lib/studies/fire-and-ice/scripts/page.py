"""Writes ../composer.html: the composer page with the stamps and the default layout in it.

    python3 stamps.py && python3 page.py
"""
import base64
import json
import os
import zlib

import numpy as np

from compose import DEFAULT, STAMPS

HERE = os.path.dirname(os.path.abspath(__file__))
stamps = {k: base64.b64encode(zlib.compress(np.ascontiguousarray(v, "<i2").tobytes(), 9)).decode()
          for k, v in np.load(STAMPS).items()}
page = open(os.path.join(HERE, "composer.template.html")).read()
page = page.replace("%STAMPS%", json.dumps(stamps)).replace("%DEFAULT%", json.dumps(DEFAULT))
open(os.path.join(HERE, "..", "composer.html"), "w").write(page)
print(f"composer.html {len(page) // 1024} KB")
