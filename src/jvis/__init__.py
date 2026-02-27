"""JVIS - Journey Virtual Intelligent System."""

# Version SSOT: delegated to utils.config.read_version() which reads .jvis/version
# then falls back to importlib.metadata. Import is deferred to avoid circular imports
# during early package initialization.

try:
    from jvis.utils.config import read_version

    __version__ = read_version()
except Exception:
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version("jvis")
    except PackageNotFoundError:
        __version__ = "0.0.0"
