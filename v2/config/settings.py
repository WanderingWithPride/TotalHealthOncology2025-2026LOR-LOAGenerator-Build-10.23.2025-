"""
Application Settings - Total Health Conferencing
Company information, branding, and configuration constants
"""
from typing import Dict
from pathlib import Path


# ============================================================================
# COMPANY INFORMATION
# ============================================================================

COMPANY_INFO = {
    "name": "Total Health Information Services, LLC.",
    "short_name": "Total Health Conferencing",
    "address": "20423 State Road 7, F6-496, Boca Raton FL 33498",
}


# ============================================================================
# SARAH'S INFORMATION (CEO)
# ============================================================================

SARAH_INFO = {
    "name": "Sarah Louden",
    "title": "Founder and Executive Director, Total Health Conferencing",
    "email": "sarah@totalhealthconferencing.com",
    "phone": "C: (561) 331-9615  O: (561) 237-2845  F: (561) 771-1748",
}


# ============================================================================
# MICHAEL'S INFORMATION (Alternative Signatory)
# ============================================================================

MICHAEL_INFO = {
    "name": "Michael Eisinger",
    "title": "Chief Executive Officer, Total Health Conferencing",
}


# ============================================================================
# BRANDING & COLORS
# ============================================================================

BRAND_COLORS = {
    "primary": "#013955",           # Deep teal
    "secondary": "#6d5065",         # Plum
    "accent": "#bb9cb2",            # Lavender
    "blue_gray": "#4a8499",
    "light_blue": "#c9deff",
    "light_gray": "#eeedeb",
    "white": "#ffffff",
    "black": "#000000",
    "dark_gray": "#1a1a1a"
}


# ============================================================================
# ASSET PATHS
# ============================================================================

# Base directory for assets
ASSETS_DIR = Path(__file__).parent.parent / "assets"

# Logo file paths (in priority order)
LOGO_PATHS = [
    ASSETS_DIR / "TH Logo.png",
    ASSETS_DIR / "TH Logo.jpg",
    ASSETS_DIR / "th_logo.png",
    ASSETS_DIR / "th_logo.jpg",
]

# Signature file paths (in priority order)
SIGNATURE_PATHS = [
    ASSETS_DIR / "sarah_signature.jpg",
    ASSETS_DIR / "sarah_signature.png",
    ASSETS_DIR / "sarah signature.jpg",
    ASSETS_DIR / "sarah signature.png",
    ASSETS_DIR / "Sarah signature.png",
    ASSETS_DIR / "Sarah signature.jpg",
]


# ============================================================================
# DOCUMENT GENERATION SETTINGS
# ============================================================================

DOCUMENT_SETTINGS = {
    "logo_width_inches": 2.5,
    "signature_width_inches": 2.0,
    "default_font": "Times New Roman",
    "default_font_size": 12,
    "pdf_margins_inches": 0.9,
}


# ============================================================================
# AUDIENCE DESCRIPTION (Default)
# ============================================================================

DEFAULT_AUDIENCE = "physicians, nurses, pharmacists, advanced practitioners and patient advocates"


# ============================================================================
# ASCO NAMING TOGGLE
# ============================================================================

# Global setting for ASCO event naming
# Set to True when approved to use "Best of ASCO" instead of "ASCO Direct"
USE_BEST_OF_ASCO_NAMING = False


def get_asco_event_name(base_name: str, use_best_of: bool = None) -> str:
    """
    Get ASCO event name based on naming toggle

    Args:
        base_name: Original event name
        use_best_of: Override for naming preference (None = use global setting)

    Returns:
        Event name with correct ASCO branding
    """
    if use_best_of is None:
        use_best_of = USE_BEST_OF_ASCO_NAMING

    if use_best_of:
        return base_name.replace("ASCO Direct", "Best of ASCO")
    return base_name


# ============================================================================
# COMPLIANCE TEMPLATES
# ============================================================================

COMPLIANCE_TEMPLATES = {
    "novartis": {
        "name": "Novartis Standard",
        "text": """Novartis requires that you acknowledge that the support described in this letter is being provided at fair market value for the services/benefits described. Novartis requires that no HCPs be remunerated by you in connection with this CME activity, and that you certify that the meeting will comply with the Sunshine Act reporting requirements. In addition, Novartis Pharmaceuticals Corporation must approve the meeting agenda at least 60 days in advance of the meeting and the grant does not represent a charitable contribution."""
    },
    "generic": {
        "name": "Generic Pharma Compliance",
        "text": """Company Name requires confirmation that all financial support is provided at fair market value and that this activity complies with all applicable Sunshine Act reporting requirements. The support does not constitute a charitable contribution."""
    },
    "educational": {
        "name": "Educational Focus",
        "text": """This educational activity is developed in accordance with ACCME Standards for Integrity and Independence in Accredited Continuing Education. The content is developed free from commercial influence and bias, and will present evidence-based clinical information."""
    }
}


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    "log_file": "letter_generation_log.json",
    "max_file_size_mb": 10,
    "max_entries": 500,
    "dangerous_chars": ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}', '[', ']'],
    "max_input_length": 500,
}


# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

SECURITY_CONFIG = {
    "password_expiry_hours": 48,
    "session_timeout_minutes": 120,
}


# ============================================================================
# UI CONFIGURATION
# ============================================================================

UI_CONFIG = {
    "events_per_page": 100,
    "log_entries_to_show": 50,
    "search_min_chars": 2,
}
