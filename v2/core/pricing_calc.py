"""
Pricing Calculation Engine - Total Health Conferencing
Handles all pricing calculations, discounts, and rounding
"""
from typing import List, Optional
from core.models import PricingCalculation
from config.pricing import (
    get_booth_prices,
    get_add_ons_pricing,
    get_discount_multiplier,
    round_nearest_50,
    currency,
)


class PricingEngine:
    """
    Centralized pricing calculation engine

    Handles booth pricing, add-ons, discounts, and rounding logic
    """

    @staticmethod
    def calculate_pricing(
        booth_tier: str,
        add_on_keys: List[str],
        event_year: int,
        discount_key: str = "none",
        custom_total: Optional[float] = None,
    ) -> PricingCalculation:
        """
        Calculate complete pricing for an event sponsorship

        Args:
            booth_tier: Booth tier key (e.g., "standard_2d", "platinum")
            add_on_keys: List of selected add-on keys
            event_year: Event year (2025 or 2026) for add-ons pricing
            discount_key: Discount option key (e.g., "minus_10", "custom")
            custom_total: Custom total override (only used if discount_key="custom")

        Returns:
            PricingCalculation object with all pricing details
        """
        # Get pricing data
        booth_prices = get_booth_prices()
        add_ons_pricing = get_add_ons_pricing(event_year)

        # Calculate booth price
        if booth_tier == "(no booth)":
            booth_price = 0.0
        else:
            booth_price = booth_prices.get(booth_tier, 0.0)

        # Calculate add-ons total
        add_ons_total = sum(
            add_ons_pricing[key]["price"]
            for key in add_on_keys
            if key in add_ons_pricing
        )

        # Calculate subtotal
        subtotal = booth_price + add_ons_total

        # Apply discount
        if discount_key == "custom" and custom_total is not None:
            # Custom total override
            final_total = custom_total
            discount_multiplier = 0.0
            discount_amount = subtotal - custom_total
        else:
            # Standard discount
            discount_multiplier = get_discount_multiplier(discount_key) or 1.0
            discounted = subtotal * discount_multiplier
            discount_amount = subtotal - discounted
            final_total = discounted

        # Round to nearest $50
        rounded_total = round_nearest_50(final_total)

        return PricingCalculation(
            booth_tier=booth_tier,
            booth_price=booth_price,
            add_on_keys=add_on_keys,
            add_ons_total=add_ons_total,
            subtotal=subtotal,
            discount_key=discount_key,
            discount_multiplier=discount_multiplier,
            discount_amount=discount_amount,
            final_total=final_total,
            rounded_total=rounded_total,
        )

    @staticmethod
    def calculate_multi_meeting_pricing(
        events_configs: List[dict],
    ) -> dict:
        """
        Calculate pricing for multi-meeting package

        Args:
            events_configs: List of event configurations, each containing:
                - event: Event object
                - booth_tier: Selected booth tier
                - add_on_keys: Selected add-ons

        Returns:
            Dictionary with pricing breakdown:
                - total_booth_cost
                - total_addon_cost
                - final_total
                - events_breakdown (list of per-event costs)
        """
        total_booth_cost = 0.0
        total_addon_cost = 0.0
        events_breakdown = []

        booth_prices = get_booth_prices()

        for config in events_configs:
            event = config["event"]
            booth_tier = config.get("booth_tier", "(no booth)")
            add_on_keys = config.get("add_on_keys", [])

            # Get event year for add-ons pricing
            event_year = event.get_year()
            add_ons_pricing = get_add_ons_pricing(event_year)

            # Calculate booth cost
            if booth_tier != "(no booth)":
                booth_cost = booth_prices.get(booth_tier, 0.0)
            else:
                booth_cost = 0.0

            # Calculate add-ons cost
            addon_cost = sum(
                add_ons_pricing[key]["price"]
                for key in add_on_keys
                if key in add_ons_pricing
            )

            # Add to totals
            total_booth_cost += booth_cost
            total_addon_cost += addon_cost

            # Track breakdown
            events_breakdown.append({
                "event_name": event.meeting_name,
                "booth_tier": booth_tier,
                "booth_cost": booth_cost,
                "add_ons": add_on_keys,
                "addon_cost": addon_cost,
                "event_total": booth_cost + addon_cost,
            })

        final_total = total_booth_cost + total_addon_cost

        return {
            "total_booth_cost": total_booth_cost,
            "total_addon_cost": total_addon_cost,
            "final_total": final_total,
            "events_breakdown": events_breakdown,
        }

    @staticmethod
    def format_pricing_display(calculation: PricingCalculation) -> dict:
        """
        Format pricing calculation for display

        Args:
            calculation: PricingCalculation object

        Returns:
            Dictionary with formatted strings for UI display
        """
        return {
            "Booth": currency(calculation.booth_price),
            "Add-ons": currency(calculation.add_ons_total),
            "Subtotal": currency(calculation.subtotal),
            "Discount": f"-{currency(calculation.discount_amount)}" if calculation.discount_amount > 0 else "None",
            "Total (before rounding)": currency(calculation.final_total),
            "Final Total (rounded)": currency(calculation.rounded_total),
        }

    @staticmethod
    def get_add_ons_breakdown(
        add_on_keys: List[str],
        event_year: int
    ) -> List[dict]:
        """
        Get detailed breakdown of selected add-ons

        Args:
            add_on_keys: List of selected add-on keys
            event_year: Event year for pricing

        Returns:
            List of dictionaries with add-on details
        """
        add_ons_pricing = get_add_ons_pricing(event_year)
        breakdown = []

        for key in add_on_keys:
            if key in add_ons_pricing:
                addon = add_ons_pricing[key]
                breakdown.append({
                    "key": key,
                    "label": addon["label"],
                    "price": addon["price"],
                    "price_formatted": currency(addon["price"]),
                })

        return breakdown
