from .calendar_reader import Reader
from . import __project__, __version__


def list_events():
    """List events"""
    reader = Reader()
    reader.listing_events()


def version_check():
    """Print version info"""
    print(f"{__project__} version {__version__}")
