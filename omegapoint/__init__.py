"""
Omegapoint library for accessing the Omega Point API from Python.

This library consists of three main components:
    
    schema.py - Python classes for the Omega Point GraphQL API, auto-generated with sgqlc
    
    omegapoint.py - Convenience functions for common operations
    
    utils.py - Utility functions for working with dates and API requests
    
    validation.py - Input validation utilities

Environment variables:
    OMEGA_POINT_DEFAULT_MODEL_ID - Default model ID (e.g., 'AXWW4-SH')
    OMEGA_POINT_API_KEY - API key from Omega Point platform
    OMEGA_POINT_URL - API URL (default: 'https://api.ompnt.com/graphql')
"""
__version__ = '0.0.4'

from . import schema
from . import omegapoint
from . import utils
from . import validation