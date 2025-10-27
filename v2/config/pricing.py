"""
Pricing Configuration - Total Health Conferencing
Booth tiers, add-ons, and pricing rules for 2025-2026
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import streamlit as st


# ============================================================================
# BOOTH TIERS
# ============================================================================

BOOTH_TIER_LABELS = {
    "standard_1d": "Standard Booth (1-Day Event)",
    "standard_2d": "Standard Booth (2-Day Event)",
    "platinum": "Platinum Booth",
    "best_of": "Best of Booth",
    "premier": "Premier Booth",
    "(no booth)": "(No Booth - Add-ons Only)"
}


def get_booth_prices() -> Dict[str, float]:
    """
    Get booth pricing from secure secrets

    Returns:
        Dictionary mapping booth tier keys to prices
    """
    try:
        prices = dict(st.secrets.get("booth_prices", {}))
        # Convert to dict if it's a special streamlit object
        return {
            "standard_1d": float(prices.get("standard_1d", 5000)),
            "standard_2d": float(prices.get("standard_2d", 7500)),
            "platinum": float(prices.get("platinum", 10000)),
            "best_of": float(prices.get("best_of", 10000)),
            "premier": float(prices.get("premier", 15000)),
        }
    except Exception:
        # Fallback pricing if secrets unavailable
        return {
            "standard_1d": 5000,
            "standard_2d": 7500,
            "platinum": 10000,
            "best_of": 10000,
            "premier": 15000,
        }


# ============================================================================
# ADD-ONS CONFIGURATION
# ============================================================================

@dataclass
class AddOn:
    """
    Represents an add-on sponsorship opportunity

    Attributes:
        key: Unique identifier
        label: Display name
        price: Cost in USD
        category: Category for UI grouping
        bullets: List of benefits/features
    """
    key: str
    label: str
    price: float
    category: str
    bullets: List[str]


def get_add_ons_2025() -> Dict[str, Dict]:
    """Get 2025 add-ons pricing from secure secrets"""
    try:
        addons = dict(st.secrets.get("add_ons_2025", {}))
        # Convert to standard dict format
        result = {}
        for key, value in addons.items():
            if isinstance(value, dict):
                result[key] = {
                    "label": value.get("label", ""),
                    "price": float(value.get("price", 0))
                }
        return result if result else _get_fallback_add_ons_2025()
    except Exception:
        return _get_fallback_add_ons_2025()


def get_add_ons_2026() -> Dict[str, Dict]:
    """Get 2026 add-ons pricing from secure secrets"""
    try:
        addons = dict(st.secrets.get("add_ons_2026", {}))
        # Convert to standard dict format
        result = {}
        for key, value in addons.items():
            if isinstance(value, dict):
                result[key] = {
                    "label": value.get("label", ""),
                    "price": float(value.get("price", 0))
                }
        return result if result else _get_fallback_add_ons_2026()
    except Exception:
        return _get_fallback_add_ons_2026()


def _get_fallback_add_ons_2025() -> Dict[str, Dict]:
    """Fallback add-ons for 2025 if secrets unavailable"""
    return {
        "program_ad_full": {"label": "Program Guide Full Page Ad", "price": 2000},
        "charging_stations": {"label": "In-Person Charging Station", "price": 2000},
        "wifi_sponsorship": {"label": "Wi-Fi Network Sponsorship", "price": 3000},
        "platform_banner": {"label": "Platform Banner Ad", "price": 2000},
        "email_banner": {"label": "Email Banner Ad", "price": 2500},
        "registration_banner": {"label": "Registration Banner Ad", "price": 2000},
        "networking_reception": {"label": "In-Person Networking Reception", "price": 3500},
        "networking_activity": {"label": "Networking Activity / Excursion", "price": 3500},
        "advisory_board": {"label": "Advisory Board (3-hour)", "price": 30000},
        "non_cme_session": {"label": "Non-CME/CE Session (45 min)", "price": 50000},
    }


def _get_fallback_add_ons_2026() -> Dict[str, Dict]:
    """Fallback add-ons for 2026 if secrets unavailable"""
    return {
        "program_ad_full": {"label": "Program Guide Full Page Ad", "price": 2000},
        "charging_stations": {"label": "In-Person Charging Station", "price": 3000},  # Price increase
        "wifi_sponsorship": {"label": "Wi-Fi Network Sponsorship", "price": 3000},
        "platform_banner": {"label": "Platform Banner Ad", "price": 2000},
        "email_banner": {"label": "Email Banner Ad", "price": 2500},
        "registration_banner": {"label": "Registration Banner Ad", "price": 2000},
        "networking_reception": {"label": "In-Person Networking Reception", "price": 3500},
        "networking_activity": {"label": "Networking Activity / Excursion", "price": 3500},
        "advisory_board": {"label": "Advisory Board (3-hour)", "price": 30000},
        "non_cme_session": {"label": "Non-CME/CE Session (45 min)", "price": 50000},
    }


def get_add_ons_pricing(year: int) -> Dict[str, Dict]:
    """
    Get add-ons pricing for specific year

    Args:
        year: Event year (2025 or 2026)

    Returns:
        Dictionary of add-ons with labels and prices
    """
    if year == 2026:
        return get_add_ons_2026()
    else:
        return get_add_ons_2025()


# ============================================================================
# ADD-ON BENEFITS/DESCRIPTIONS
# ============================================================================

ADD_ON_BULLETS = {
    "program_ad_full": [
        "Full-page advertisement in the printed/digital program guide."
    ],
    "charging_stations": [
        "One branded charging station with company artwork.",
        "Includes (1) in-person company representative badge."
    ],
    "wifi_sponsorship": [
        "Exclusive Wi-Fi sponsorship with company logo/name on the Wi-Fi page.",
        "Includes (1) in-person company representative badge."
    ],
    "platform_banner": [
        "Banner advertisement on the event's digital platform/lobby page."
    ],
    "email_banner": [
        "Banner placement in a national call-to-action email."
    ],
    "registration_banner": [
        "Banner on the event registration page (typically live ~6 months)."
    ],
    "networking_reception": [
        "On-site networking reception with food & beverage.",
        "Company logo on in-person conference signage.",
        "Literature may be available on high-top tables during the reception.",
        "Includes (2) in-person company representative badges for the whole conference."
    ],
    "networking_activity": [
        "Networking activity/excursion.",
        "High-top table at the activity site.",
        "Insert in branded grab-and-go snack bags plus post-conference activity.",
        "Includes (1) in-person company representative badge."
    ],
    "advisory_board": [
        "3-hour advisory board with room, AV, and food & beverage.",
        "Post-event summary and guaranteed attendance."
    ],
    "non_cme_session": [
        "45-minute non-CME/CE symposium in a non-competitive slot.",
        "Full logistics, room and AV support."
    ],
}


# ============================================================================
# ADD-ON CATEGORIES (for UI grouping)
# ============================================================================

ADD_ON_CATEGORIES = {
    "📱 Digital Marketing": ["platform_banner", "email_banner", "registration_banner"],
    "📄 Print Materials": ["program_ad_full"],
    "🔌 On-Site Services": ["charging_stations", "wifi_sponsorship"],
    "🤝 Networking": ["networking_reception", "networking_activity"],
    "🎓 Educational Programs": ["advisory_board", "non_cme_session"]
}


# ============================================================================
# STANDARD BOOTH BENEFITS
# ============================================================================

def get_booth_benefits() -> List[str]:
    """Get standard booth benefits (same for all booth tiers)"""
    return [
        "In-person exhibit booth — (1) 6' draped table and 2 chairs.",
        "(2) Full registration admissions for company representatives; additional badges available for purchase.",
        "Company logo on in-person and virtual signage.",
        "Company logo on the conference app.",
        "(1) Conference bag insert.",
        "Pre- and post-conference registration list.",
    ]


# ============================================================================
# DISCOUNT OPTIONS
# ============================================================================

DISCOUNT_OPTIONS = {
    "none": {"label": "No Discount (0%)", "multiplier": 1.00},
    "minus_10": {"label": "10% Discount", "multiplier": 0.90},
    "minus_15": {"label": "15% Discount", "multiplier": 0.85},
    "minus_20": {"label": "20% Discount", "multiplier": 0.80},
    "custom": {"label": "Custom Total Override", "multiplier": None},
}


def get_discount_multiplier(discount_key: str) -> Optional[float]:
    """
    Get discount multiplier for a discount key

    Args:
        discount_key: Discount option key

    Returns:
        Multiplier (0.80 for 20% off, etc.) or None for custom
    """
    return DISCOUNT_OPTIONS.get(discount_key, {}).get("multiplier")


# ============================================================================
# PRICING UTILITIES
# ============================================================================

def currency(amount: float) -> str:
    """Format number as USD currency"""
    return f"${amount:,.2f}"


def round_nearest_50(amount: float) -> float:
    """Round amount to nearest $50"""
    return round(amount / 50.0) * 50.0
