"""
Utility package for Travel Agency Billing Software

NOTE: Imports have been removed from here to prevent circular dependency loops.
The chain (utils -> styles -> config -> settings -> utils.config_manager) 
causes a crash if styles are imported here.

Please import functions directly from their modules:
Ex: from travel_billing_software.utils.styles import get_frame_style
"""

# __all__ is left empty to prevent implicit exports causing loops
__all__ = []