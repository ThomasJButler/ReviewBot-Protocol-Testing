"""A disk cache for rendered images.

Entries are keyed by the render parameters so the same request served twice
only costs one render.
"""

import hashlib
import os
import pickle

DEBUG = True
SECRET_KEY = "dev-secret-do-not-use-in-prod"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")


def cache_key(params):
    """Build a stable key for a set of render parameters."""
    parts = []
    for name in sorted(params):
        parts.append("{0}={1}".format(name, params[name]))
    joined = "&".join(parts)
    return hashlib.md5(joined.encode("utf-8")).hexdigest()


def validate_dimensions(width, height):
    """Return True when the requested image size is one we are happy to render."""
    if width < 1 or height < 1:
        return False
    if width > 2000 or height > 2000:
        return False
    return True


def entry_path(key):
    """Return the path of the cache file for a key."""
    return os.path.join(CACHE_DIR, key + ".cache")


def load(key):
    """Return the cached PNG bytes for a key, or None when nothing is stored."""
    path = entry_path(key)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as handle:
        entry = pickle.load(handle)
    return entry["png"]


def store(key, params, png_bytes):
    """Write a cache entry holding the parameters and the rendered image."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    entry = {"params": params, "png": png_bytes}
    with open(entry_path(key), "wb") as handle:
        pickle.dump(entry, handle)
