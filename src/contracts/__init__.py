"""Alias package that exposes `feature_interfaces` under the `contracts` name.

This module aliases all immediate submodules of `feature_interfaces` into
`contracts.*` via entries in `sys.modules`. This makes the migration safe and
idempotent: existing imports that were rewritten from
`feature_interfaces.xxx` -> `contracts.xxx` will continue to resolve.
"""

from __future__ import annotations

import importlib
import pkgutil
import sys

BASE_NAME = "feature_interfaces"

# Import base package
base_pkg = importlib.import_module(BASE_NAME)

# Alias the base package
sys.modules[__name__] = base_pkg

# Walk immediate submodules in feature_interfaces and alias them under
# contracts.<submodule>
for finder, fullname, ispkg in pkgutil.iter_modules(
    base_pkg.__path__, prefix=BASE_NAME + "."
):
    try:
        mod = importlib.import_module(fullname)
    except Exception:
        # Skip modules that fail to import at package-initialization time
        continue
    # Map feature_interfaces.foo.bar -> contracts.foo.bar
    contract_name = __name__ + fullname[len(BASE_NAME) :]
    sys.modules[contract_name] = mod
