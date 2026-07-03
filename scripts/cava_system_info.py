"""Print installed versions of all CAVA/OMOP stack packages and key dependencies.

Run with:
    python <(curl -s https://raw.githubusercontent.com/AustralianCancerDataNetwork/cava-devops/main/scripts/cava_system_info.py)

Only prints packages that are actually installed; skips the rest silently.
"""
import platform
import sys
from importlib.metadata import PackageNotFoundError, version


def get_version(package_name: str) -> str | None:
    """Return the installed version string, or None if not installed.

    Parameters
    ----------
    package_name : str
        PyPI distribution name (e.g. 'omop-alchemy', not the import name).

    Returns
    -------
    str or None
        Version string if installed, None otherwise.
    """
    try:
        return version(package_name)
    except PackageNotFoundError:
        return None


PACKAGES = [
    # CAVA/OMOP stack
    ("oa-configurator", "OA Configurator"),
    ("orm-loader", "ORM Loader"),
    ("omop-alchemy", "OMOP Alchemy"),
    ("omop-emb", "OMOP Emb"),
    ("omop-graph", "OMOP Graph"),
    ("omop-spires", "OMOP Spires"),
    # Key shared dependencies
    ("sqlalchemy", "SQLAlchemy"),
    ("pgvector", "pgvector"),
    ("faiss-cpu", "FAISS CPU"),
    ("faiss-gpu", "FAISS GPU"),
    ("numpy", "NumPy"),
]

print("--- CAVA Stack ---")
print(f"Platform : {platform.platform()}")
print(f"Python   : {sys.version.split()[0]}")
print()

any_found = False
for pkg, label in PACKAGES:
    v = get_version(pkg)
    if v is not None:
        print(f"{label:<20} {v}")
        any_found = True

if not any_found:
    print("No CAVA/OMOP packages found.")

print("------------------")
