"""PyDataScouteR - Python client for DataScouteR API"""
__version__ = "0.2.0"

from .client import (
    DataScouteRClient,
    get_goalkeepers,
    get_forwards
)

__all__ = [
    "DataScouteRClient",
    "get_goalkeepers", 
    "get_forwards"
]