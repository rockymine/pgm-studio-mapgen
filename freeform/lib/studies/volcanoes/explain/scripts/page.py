"""Writes ../caldera-lake-layers.html from template.html and the two data files gen.py and overlay.py write.

    python3 gen.py && python3 overlay.py && python3 page.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
page = open(os.path.join(HERE, "template.html")).read()
page = page.replace("%DATA%", open(os.path.join(HERE, "data.json")).read())
page = page.replace("%OVERLAY%", open(os.path.join(HERE, "overlay.json")).read())
open(os.path.join(HERE, "..", "caldera-lake-layers.html"), "w").write(page)
