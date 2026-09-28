"""The token a caller without a browser signs in to an invited studio with -- the deployed one takes a write
only from someone signed in (pgm-studio/docs/access.md). `PGM_STUDIO_TOKEN` holds it, and it is sent only over
https or to this machine: over plain http anywhere else it would cross the network readable."""
import os
import sys
import urllib.parse

LOCAL = {"localhost", "127.0.0.1", "::1"}


def authorization(api):
    """`{"Authorization": "Bearer ..."}` for requests to `api`, or `{}` where no token is set. Stops the run
    where one is set and `api` would carry it in the clear."""
    token = os.environ.get("PGM_STUDIO_TOKEN", "").strip()
    if not token:
        return {}
    address = urllib.parse.urlparse(api)
    if address.scheme != "https" and address.hostname not in LOCAL:
        sys.exit(f"PGM_STUDIO_TOKEN is sent only over https or to this machine, and PGM_STUDIO_API is {api}")
    return {"Authorization": f"Bearer {token}"}
