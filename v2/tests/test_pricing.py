"""
Unit Tests - Pricing Engine
Tests for pricing calculations, discounts, and rounding
"""
import pytest
from core.pricing_calc import PricingEngine
from config.pricing import round_nearest_50


class TestPricingCalculations:
    """Test pricing calculation logic"""

    def test_basic_booth_pricing(self):
        """Test basic booth pricing without add-ons"""
        result = PricingEngine.calculate_pricing(
            booth_tier="standard_1d",
            add_on_keys=[],
            event_year=2025,
            discount_key="none"
        )

        assert result.booth_price == 5000
        assert result.add_ons_total == 0
        assert result.subtotal == 5000
        assert result.final_total == 5000

    def test_booth_with_addons(self):
        """Test booth + add-ons pricing"""
        result = PricingEngine.calculate_pricing(
            booth_tier="standard_2d",
            add_on_keys=["program_ad_full", "charging_stations"],
            event_year=2025,
            discount_key="none"
        )

        assert result.booth_price == 7500
        assert result.add_ons_total == 4000  # 2000 + 2000
        assert result.subtotal == 11500

    def test_10_percent_discount(self):
        """Test 10% discount calculation"""
        result = PricingEngine.calculate_pricing(
            booth_tier="platinum",
            add_on_keys=[],
            event_year=2025,
            discount_key="minus_10"
        )

        assert result.booth_price == 10000
        assert result.discount_multiplier == 0.90
        assert result.final_total == 9000  # 10000 * 0.90

    def test_custom_total_override(self):
        """Test custom total override"""
        result = PricingEngine.calculate_pricing(
            booth_tier="premier",
            add_on_keys=["non_cme_session"],
            event_year=2025,
            discount_key="custom",
            custom_total=50000.0
        )

        assert result.subtotal == 65000  # 15000 + 50000
        assert result.final_total == 50000  # Custom override

    def test_rounding_to_nearest_50(self):
        """Test rounding to nearest $50"""
        assert round_nearest_50(7537.50) == 7550
        assert round_nearest_50(7524.99) == 7500
        assert round_nearest_50(7525.00) == 7500  # Python rounds to even (banker's rounding)
        assert round_nearest_50(7575.00) == 7600  # Rounds up
        assert round_nearest_50(10000.00) == 10000

    def test_2026_pricing_difference(self):
        """Test 2026 add-ons pricing (charging stations increased)"""
        result_2025 = PricingEngine.calculate_pricing(
            booth_tier="(no booth)",
            add_on_keys=["charging_stations"],
            event_year=2025,
            discount_key="none"
        )

        result_2026 = PricingEngine.calculate_pricing(
            booth_tier="(no booth)",
            add_on_keys=["charging_stations"],
            event_year=2026,
            discount_key="none"
        )

        assert result_2025.add_ons_total == 2000
        assert result_2026.add_ons_total == 3000  # Price increase in 2026


class TestMultiMeetingPricing:
    """Test multi-meeting package pricing"""

    def test_multi_meeting_aggregation(self):
        """Test pricing aggregation across multiple events"""
        from config.events import Event

        events_configs = [
            {
                "event": Event(
                    meeting_name="Event 1",
                    meeting_date_long="June 1, 2025",
                    venue="Venue 1",
                    city_state="City 1",
                    default_tier="standard_1d"
                ),
                "booth_tier": "standard_1d",
                "add_on_keys": []
            },
            {
                "event": Event(
                    meeting_name="Event 2",
                    meeting_date_long="July 1, 2025",
                    venue="Venue 2",
                    city_state="City 2",
                    default_tier="standard_1d"
                ),
                "booth_tier": "standard_2d",
                "add_on_keys": ["program_ad_full"]
            }
        ]

        result = PricingEngine.calculate_multi_meeting_pricing(events_configs)

        assert result["total_booth_cost"] == 12500  # 5000 + 7500
        assert result["total_addon_cost"] == 2000  # 0 + 2000
        assert result["final_total"] == 14500


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
