from importlib.metadata import version

"""
Python convention:
- project name is the human-readable name using dashes: "vetlog-buddy"
- package name is the importable name using underscores: "vetlog_buddy"
"""
# Get project info from pyproject.toml
__project__ = "vetlog-calendar"
__version__ = version(__project__)