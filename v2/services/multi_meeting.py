"""
Multi-Meeting Package Service - Total Health Conferencing
Handles multi-meeting sponsorship packages
"""
from typing import List, Dict
from io import BytesIO
from core.models import MultiMeetingPackage, DocumentPayload
from core.pricing_calc import PricingEngine
from generators.lor_generator import LORGenerator
from generators.loa_generator import LOAGenerator
from config.events import Event
from config.pricing import currency


class MultiMeetingService:
    """
    Service for creating multi-meeting sponsorship packages

    Combines multiple events into a single sponsorship opportunity
    with comprehensive pricing and document generation
    """

    @staticmethod
    def create_package(
        company_name: str,
        events_configs: List[Dict],
        document_type: str = "LOR",
        additional_info: str = "",
        company_address: str = ""
    ) -> MultiMeetingPackage:
        """
        Create multi-meeting package from event configurations

        Args:
            company_name: Sponsor company name
            events_configs: List of event configurations, each containing:
                - event: Event object
                - booth_tier: Selected booth tier
                - add_on_keys: List of selected add-on keys
            document_type: "LOR" or "LOA"
            additional_info: Additional requirements text
            company_address: Company address (for LOA)

        Returns:
            MultiMeetingPackage object
        """
        package = MultiMeetingPackage(
            company_name=company_name,
            document_type=document_type,
            additional_info=additional_info,
            company_address=company_address
        )

        # Calculate pricing for each event and add to package
        for config in events_configs:
            event = config["event"]
            booth_tier = config.get("booth_tier", "(no booth)")
            add_on_keys = config.get("add_on_keys", [])

            # Calculate pricing for this event
            pricing = PricingEngine.calculate_pricing(
                booth_tier=booth_tier,
                add_on_keys=add_on_keys,
                event_year=event.get_year(),
                discount_key="none"  # No discounts in multi-meeting
            )

            # Add event to package
            package.add_event(
                event=event.to_dict(),
                booth_price=pricing.booth_price,
                addon_cost=pricing.add_ons_total
            )

        return package

    @staticmethod
    def generate_package_documents(
        package: MultiMeetingPackage
    ) -> tuple:
        """
        Generate documents for multi-meeting package

        Args:
            package: MultiMeetingPackage object

        Returns:
            Tuple of (docx_buffer, pdf_buffer)
        """
        # Create payload for document generation
        payload = MultiMeetingService._create_package_payload(package)

        # Generate documents based on type
        if package.document_type == "LOA":
            generator = LOAGenerator(payload)
        else:
            generator = LORGenerator(payload)

        docx_buffer = generator.generate_docx()
        pdf_buffer = generator.generate_pdf()

        return docx_buffer, pdf_buffer

    @staticmethod
    def _create_package_payload(package: MultiMeetingPackage) -> Dict:
        """
        Create document payload from multi-meeting package

        Args:
            package: MultiMeetingPackage object

        Returns:
            Dictionary payload for document generation
        """
        # Build event list summary
        event_list = []
        for event in package.events:
            event_list.append(f"• {event['meeting_name']} - {event['meeting_date_long']}")

        # Create payload
        payload = {
            "company_name": package.company_name,
            "company_address": package.company_address,
            "meeting_name": f"Multi-Meeting Package ({len(package.events)} Events)",
            "meeting_date_long": "Various Dates (2025-2026)",
            "venue": "Multiple Venues",
            "city_state": "Various Locations",
            "booth_selected": package.total_booth_cost > 0,
            "booth_tier": "Multi-Meeting Package",
            "booth_price": package.total_booth_cost,
            "add_on_keys": [],  # Add-ons are event-specific
            "add_ons_total": package.total_addon_cost,
            "subtotal": package.final_total,
            "discount_applied": 0.0,
            "final_total": package.final_total,
            "amount_currency": currency(package.final_total),
            "additional_info": package.additional_info or self._generate_event_list_text(package.events),
            "document_type": package.document_type,
            "event_year": 2025,  # Default year
        }

        return payload

    @staticmethod
    def _generate_event_list_text(events: List[Dict]) -> str:
        """
        Generate formatted event list text for documents

        Args:
            events: List of event dictionaries

        Returns:
            Formatted event list string
        """
        lines = ["This multi-meeting package includes the following events:"]
        lines.append("")

        for event in events:
            meeting_name = event.get("meeting_name", "")
            meeting_date = event.get("meeting_date_long", "")
            city_state = event.get("city_state", "")

            lines.append(f"• {meeting_name}")
            lines.append(f"  Date: {meeting_date}")
            lines.append(f"  Location: {city_state}")

            # Add costs if available
            booth_price = event.get("booth_price", 0)
            addon_cost = event.get("addon_cost", 0)

            if booth_price > 0:
                lines.append(f"  Booth: {currency(booth_price)}")

            if addon_cost > 0:
                lines.append(f"  Add-ons: {currency(addon_cost)}")

            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def calculate_package_summary(package: MultiMeetingPackage) -> Dict:
        """
        Calculate package summary statistics

        Args:
            package: MultiMeetingPackage object

        Returns:
            Dictionary with summary statistics
        """
        return {
            "event_count": len(package.events),
            "total_booth_cost": package.total_booth_cost,
            "total_addon_cost": package.total_addon_cost,
            "final_total": package.final_total,
            "average_per_event": package.final_total / len(package.events) if package.events else 0,
            "total_booth_cost_formatted": currency(package.total_booth_cost),
            "total_addon_cost_formatted": currency(package.total_addon_cost),
            "final_total_formatted": currency(package.final_total),
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_multi_meeting_package(
    company_name: str,
    events_configs: List[Dict],
    document_type: str = "LOR",
    additional_info: str = "",
    company_address: str = ""
) -> MultiMeetingPackage:
    """
    Convenience function to create multi-meeting package

    Args:
        company_name: Sponsor company name
        events_configs: List of event configurations
        document_type: "LOR" or "LOA"
        additional_info: Additional requirements
        company_address: Company address

    Returns:
        MultiMeetingPackage object
    """
    return MultiMeetingService.create_package(
        company_name=company_name,
        events_configs=events_configs,
        document_type=document_type,
        additional_info=additional_info,
        company_address=company_address
    )


def generate_multi_meeting_documents(package: MultiMeetingPackage) -> tuple:
    """
    Convenience function to generate multi-meeting package documents

    Args:
        package: MultiMeetingPackage object

    Returns:
        Tuple of (docx_buffer, pdf_buffer)
    """
    return MultiMeetingService.generate_package_documents(package)
