"""
Core Data Models - Total Health Conferencing
Data structures for document generation and business logic
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class DocumentPayload:
    """
    Complete data payload for document generation

    Contains all information needed to generate an LOR or LOA
    """
    # Company information
    company_name: str
    company_address: Optional[str] = None

    # Event information
    meeting_name: str
    meeting_date_long: str
    venue: str
    city_state: str

    # Booth and pricing
    booth_selected: bool = False
    booth_tier: Optional[str] = None
    booth_price: Optional[float] = None

    # Add-ons
    add_on_keys: List[str] = field(default_factory=list)
    add_ons_total: float = 0.0

    # Totals and discounts
    subtotal: float = 0.0
    discount_applied: float = 0.0
    final_total: float = 0.0
    amount_currency: str = "$0.00"

    # Additional information
    additional_info: Optional[str] = None
    additional_info_lead_in: Optional[str] = None
    additional_info_bullets: List[str] = field(default_factory=list)

    # Attendance
    attendance_expected: Optional[int] = None
    audience_list: str = "physicians, nurses, pharmacists, advanced practitioners and patient advocates"

    # LOA-specific fields
    agreement_date: Optional[str] = None
    signature_person: str = "Sarah Louden - Founder and Executive Director, Total Health Conferencing"

    # Document metadata
    document_type: str = "LOR"  # "LOR" or "LOA"
    event_year: int = 2025

    def to_dict(self) -> Dict:
        """Convert payload to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'DocumentPayload':
        """Create payload from dictionary"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class MultiMeetingPackage:
    """
    Represents a multi-meeting sponsorship package

    Combines multiple events into a single sponsorship opportunity
    """
    company_name: str
    events: List[Dict] = field(default_factory=list)
    total_booth_cost: float = 0.0
    total_addon_cost: float = 0.0
    final_total: float = 0.0
    document_type: str = "LOR"
    additional_info: Optional[str] = None
    company_address: Optional[str] = None

    def add_event(self, event: Dict, booth_price: float = 0.0, addon_cost: float = 0.0):
        """Add an event to the package"""
        self.events.append({
            **event,
            "booth_price": booth_price,
            "addon_cost": addon_cost,
        })
        self.total_booth_cost += booth_price
        self.total_addon_cost += addon_cost
        self.final_total = self.total_booth_cost + self.total_addon_cost

    def get_event_count(self) -> int:
        """Get number of events in package"""
        return len(self.events)

    def to_payload(self) -> DocumentPayload:
        """Convert package to document payload"""
        return DocumentPayload(
            company_name=self.company_name,
            company_address=self.company_address,
            meeting_name=f"Multi-Meeting Package ({len(self.events)} events)",
            meeting_date_long="Various dates",
            venue="Multiple venues",
            city_state="Various locations",
            final_total=self.final_total,
            amount_currency=f"${self.final_total:,.2f}",
            document_type=self.document_type,
            additional_info=self.additional_info,
        )

    def to_dict(self) -> Dict:
        """Convert package to dictionary"""
        return asdict(self)


@dataclass
class ExcelRow:
    """
    Represents a row from Excel bulk import

    Maps Excel columns to internal data structure
    """
    exhibitor_invite: str
    event_name: str
    total: str

    # Optional fields
    company_name: Optional[str] = None
    expected_attendance: Optional[int] = None
    date: Optional[str] = None
    city: Optional[str] = None
    venue: Optional[str] = None
    official_address: Optional[str] = None
    amount: Optional[str] = None
    discount: Optional[str] = None

    row_number: int = 0
    matched_event: Optional[Dict] = None
    errors: List[str] = field(default_factory=list)

    def has_errors(self) -> bool:
        """Check if row has validation errors"""
        return len(self.errors) > 0

    def add_error(self, error: str):
        """Add validation error"""
        self.errors.append(error)

    def get_total_amount(self) -> float:
        """Extract numeric total from total string"""
        try:
            # Remove currency symbols and commas
            clean = self.total.replace('$', '').replace(',', '').strip()
            return float(clean)
        except (ValueError, AttributeError):
            return 0.0


@dataclass
class LetterGenerationLog:
    """
    Log entry for letter generation tracking
    """
    timestamp: str
    company_name: str
    meeting_name: str
    document_type: str
    booth_selected: Optional[str]
    add_ons: List[str]
    total_cost: float
    additional_info: str
    user_role: str
    session_id: str

    def to_dict(self) -> Dict:
        """Convert log entry to dictionary"""
        return asdict(self)

    @classmethod
    def create(
        cls,
        company_name: str,
        meeting_name: str,
        document_type: str,
        booth_selected: Optional[str],
        add_ons: List[str],
        total_cost: float,
        additional_info: str = "",
        user_role: str = "Unknown",
        session_id: str = "unknown",
    ) -> 'LetterGenerationLog':
        """Create new log entry with current timestamp"""
        return cls(
            timestamp=datetime.now().isoformat(),
            company_name=company_name,
            meeting_name=meeting_name,
            document_type=document_type,
            booth_selected=booth_selected,
            add_ons=add_ons,
            total_cost=total_cost,
            additional_info=additional_info,
            user_role=user_role,
            session_id=session_id,
        )


@dataclass
class PricingCalculation:
    """
    Result of pricing calculation

    Tracks booth costs, add-ons, discounts, and final total
    """
    booth_tier: str
    booth_price: float
    add_on_keys: List[str]
    add_ons_total: float
    subtotal: float
    discount_key: str
    discount_multiplier: float
    discount_amount: float
    final_total: float
    rounded_total: float

    def get_summary(self) -> Dict[str, float]:
        """Get pricing summary as dictionary"""
        return {
            "booth_price": self.booth_price,
            "add_ons_total": self.add_ons_total,
            "subtotal": self.subtotal,
            "discount_amount": self.discount_amount,
            "final_total": self.final_total,
            "rounded_total": self.rounded_total,
        }

    def to_currency_summary(self) -> Dict[str, str]:
        """Get pricing summary formatted as currency"""
        return {
            "booth_price": f"${self.booth_price:,.2f}",
            "add_ons_total": f"${self.add_ons_total:,.2f}",
            "subtotal": f"${self.subtotal:,.2f}",
            "discount_amount": f"-${self.discount_amount:,.2f}",
            "final_total": f"${self.final_total:,.2f}",
            "rounded_total": f"${self.rounded_total:,.2f}",
        }
