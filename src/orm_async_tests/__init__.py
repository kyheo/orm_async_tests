from importlib.metadata import PackageNotFoundError  # type: ignore
from importlib.metadata import version

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
