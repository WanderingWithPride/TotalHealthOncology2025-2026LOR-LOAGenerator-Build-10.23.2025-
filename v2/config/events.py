"""
Events Database - Total Health Conferencing
Contains all 2025-2026 conference events with complete metadata
"""
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Event:
    """
    Represents a single conference event

    Attributes:
        meeting_name: Full event name
        meeting_date_long: Human-readable date (e.g., "June 27-28, 2026")
        venue: Venue name
        city_state: City and state (e.g., "Denver, CO")
        default_tier: Default booth tier for this event
        expected_attendance: Expected number of attendees (optional)
    """
    meeting_name: str
    meeting_date_long: str
    venue: str
    city_state: str
    default_tier: str
    expected_attendance: Optional[int] = None

    def to_dict(self) -> Dict:
        """Convert event to dictionary"""
        return asdict(self)

    def get_year(self) -> int:
        """Extract year from meeting name or date"""
        if "2026" in self.meeting_name:
            return 2026
        elif "2025" in self.meeting_name:
            return 2025
        return 2025  # Default


# ============================================================================
# 2025 EVENTS
# ============================================================================

EVENTS_2025 = [
    Event(
        meeting_name="2025 Astera Cancer Care Annual Retreat",
        meeting_date_long="September 27, 2025",
        venue="Ocean Place Resort and Spa",
        city_state="Long Branch, NJ",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2025 Cancer Updates GU and Lung, Memphis, TN",
        meeting_date_long="September 30, 2025",
        venue="Hilton Memphis",
        city_state="Memphis, TN",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2025 West Oncology APP Dinner",
        meeting_date_long="October 9, 2025",
        venue="Hilton Memphis",
        city_state="Memphis, TN",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2025 Empower (Patient Meeting)",
        meeting_date_long="October 11, 2025",
        venue="Farmer's Table",
        city_state="Boca Raton, FL",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2025 Northwell Health Second Annual Liver Cancer Symposium",
        meeting_date_long="October 17, 2025",
        venue="The Garden City Hotel",
        city_state="Garden City, NY",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2025 Cancer Updates GI and Breast, Boston, MA",
        meeting_date_long="October 30, 2025",
        venue="Battery Wharf Hotel Boston Waterfront",
        city_state="Boston, MA",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2025 ESMO USA West",
        meeting_date_long="November 1–2, 2025",
        venue="The Antlers",
        city_state="Colorado Springs, CO",
        default_tier="standard_2d"
    ),
    Event(
        meeting_name="2025 ESMO USA East",
        meeting_date_long="November 1–2, 2025",
        venue="The Ritz-Carlton Orlando",
        city_state="Orlando, FL",
        default_tier="standard_2d"
    ),
    Event(
        meeting_name="2025 Northwell Health Multidisciplinary Head and Neck Cancer Symposium",
        meeting_date_long="November 1, 2025",
        venue="The Garden City Hotel",
        city_state="Garden City, NY",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2025 Cancer Updates Heme and GU, Denver, CO",
        meeting_date_long="December 4, 2025",
        venue="Denver Marriott Westminster",
        city_state="Denver, CO",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2025 Northwell Best of Practice Impacting Science",
        meeting_date_long="December 5, 2025",
        venue="The Garden City Hotel",
        city_state="Garden City, NY",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2025 Oncology Update Conference presented by High Plains Oncology Professionals-HPOP",
        meeting_date_long="December 6, 2025",
        venue="Fort Collins Marriott",
        city_state="Fort Collins, CO",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2025 (Northwell) 2nd Annual New York Pancreatic Cancer Consortium",
        meeting_date_long="December 12, 2025",
        venue="Martinique New York on Broadway",
        city_state="Manhattan, NY",
        default_tier="platinum"
    ),
]


# ============================================================================
# 2026 EVENTS
# ============================================================================

EVENTS_2026 = [
    Event(
        meeting_name="2026 Best of Breast Conference",
        meeting_date_long="January 17-18, 2026",
        venue="Beach House Ft. Lauderdale",
        city_state="Fort Lauderdale, FL",
        default_tier="best_of",
        expected_attendance=50
    ),
    Event(
        meeting_name="2026 Cancer Updates GI and Breast, Princeton, NJ",
        meeting_date_long="January 22, 2026",
        venue="Princeton Marriott at Forrestal",
        city_state="Princeton, NJ",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 Northwell Cancer Institute Frontiers in Cancer Scientific Symposium",
        meeting_date_long="January 28, 2026",
        venue="Carnegie Hall",
        city_state="Manhattan, NYC",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2026 West Oncology Conference",
        meeting_date_long="January 31-February 1, 2026",
        venue="Hilton Memphis",
        city_state="Memphis, TN",
        default_tier="standard_2d",
        expected_attendance=50
    ),
    Event(
        meeting_name="2026 Best of Hematology Conference",
        meeting_date_long="February 7-8, 2026",
        venue="The Hythe",
        city_state="Vail, CO",
        default_tier="best_of",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 ASCO Direct GI",
        meeting_date_long="February 7-8, 2026",
        venue="The Rittenhouse",
        city_state="Philadelphia, PA",
        default_tier="standard_2d",
        expected_attendance=40
    ),
    Event(
        meeting_name="2026 University of Kansas Cancer Center Breast Cancer Year in Review",
        meeting_date_long="February 21, 2026",
        venue="Sheraton Overland Park Hotel at the Convention Center",
        city_state="Kansas City, MO",
        default_tier="standard_1d",
        expected_attendance=75
    ),
    Event(
        meeting_name="2026 Cancer Updates GI and Breast, Dallas, TX",
        meeting_date_long="February 26, 2026",
        venue="The Highland Dallas",
        city_state="Dallas, TX",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 Cancer Updates GI and Breast, Nashville, TN",
        meeting_date_long="March 5, 2026",
        venue="Loews Vanderbilt Hotel",
        city_state="Nashville, TN",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 Cancer Updates GI and Lung, Denver, CO",
        meeting_date_long="March 12, 2026",
        venue="Denver Marriott Westminster",
        city_state="Denver, CO",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 ASCO Direct GU",
        meeting_date_long="March 14-15, 2026",
        venue="The Hyatt",
        city_state="Boston, MA",
        default_tier="standard_2d",
        expected_attendance=40
    ),
    Event(
        meeting_name="2026 Cancer Updates GI and Breast, Houston",
        meeting_date_long="April 9, 2026",
        venue="The Blossom Hotel Houston",
        city_state="Houston, TX",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 Oncology Clinical Updates - Review and Renew Sedona",
        meeting_date_long="April 11-12, 2026",
        venue="Hilton Sedona Resort at Bell Rock",
        city_state="Sedona, AZ",
        default_tier="standard_2d",
        expected_attendance=30
    ),
    Event(
        meeting_name="ESMO USA in Focus 2026: Lung Cancer and Sarcomas - With John Trent and Ravi Salgia",
        meeting_date_long="April 25, 2026",
        venue="Minneapolis Marriott City Center",
        city_state="Minneapolis, MN",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 Cancer Updates Breast and Lung, Kansas City",
        meeting_date_long="May 14, 2026",
        venue="Crossroads Hotel Kansas City",
        city_state="Kansas City, MO",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="ESMO in Focus 2026: Breast - EAST - With Reshma Mahtani and Kevin Kalinsky",
        meeting_date_long="May 16, 2026",
        venue="Baltimore, MD",
        city_state="Baltimore, MD",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="ESMO in Focus 2026: Breast - WEST - With Hope Rugo and Sarah Tolaney",
        meeting_date_long="May 16, 2026",
        venue="Salt Lake City, UT",
        city_state="Salt Lake City, UT",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2026 ASCO Direct Puerto Rico",
        meeting_date_long="June 13-14, 2026",
        venue="Hyatt Regency Grand Reserve",
        city_state="San Juan, PR",
        default_tier="standard_2d",
        expected_attendance=60
    ),
    Event(
        meeting_name="2026 ASCO Direct Austin",
        meeting_date_long="June 13-14, 2026",
        venue="W Austin",
        city_state="Austin, TX",
        default_tier="standard_2d",
        expected_attendance=60
    ),
    Event(
        meeting_name="2026 ASCO Direct Los Angeles",
        meeting_date_long="June 13-14, 2026",
        venue="Le Meridien",
        city_state="Los Angeles, CA",
        default_tier="standard_2d",
        expected_attendance=50
    ),
    Event(
        meeting_name="2026 ASCO Direct Hawaii",
        meeting_date_long="June 27-28, 2026",
        venue="Sheraton Waikiki Beach Resort",
        city_state="Honolulu, HI",
        default_tier="standard_2d",
        expected_attendance=100
    ),
    Event(
        meeting_name="2026 ASCO Direct Washington DC",
        meeting_date_long="June 27-28, 2026",
        venue="Four Seasons Hotel Washington",
        city_state="Washington DC",
        default_tier="standard_2d",
        expected_attendance=60
    ),
    Event(
        meeting_name="2026 ASCO Direct Denver",
        meeting_date_long="June 27-28, 2026",
        venue="Denver Marriott Westminster",
        city_state="Denver, CO",
        default_tier="standard_2d",
        expected_attendance=60
    ),
    Event(
        meeting_name="2026 Cancer Updates Heme and Breast, Michigan",
        meeting_date_long="July 9, 2026",
        venue="The Vanguard Ann Arbor, Autograph Collection",
        city_state="Ann Arbor, MI",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 ASCO Direct New Orleans",
        meeting_date_long="July 10-11, 2026",
        venue="Hyatt Regency NOLA",
        city_state="New Orleans, LA",
        default_tier="standard_2d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 ASCO Direct Charlotte",
        meeting_date_long="July 18-19, 2026",
        venue="Grand Bohemian",
        city_state="Charlotte, NC",
        default_tier="standard_2d",
        expected_attendance=60
    ),
    Event(
        meeting_name="2026 ASCO Direct Philadelphia",
        meeting_date_long="July 18-19, 2026",
        venue="Rittenhouse",
        city_state="Philadelphia, PA",
        default_tier="standard_2d",
        expected_attendance=60
    ),
    Event(
        meeting_name="2026 ASCO Direct Anchorage",
        meeting_date_long="July 18-19, 2026",
        venue="Anchorage Marriott Downtown",
        city_state="Anchorage, AK",
        default_tier="standard_2d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 ASCO Direct Las Vegas",
        meeting_date_long="July 25-26, 2026",
        venue="Westin Lake Las Vegas",
        city_state="Henderson/Las Vegas, NV",
        default_tier="standard_2d",
        expected_attendance=60
    ),
    Event(
        meeting_name="2026 ASCO Direct Indianapolis",
        meeting_date_long="July 25-26, 2026",
        venue="Indianapolis Marriott Downtown",
        city_state="Indianapolis, IN",
        default_tier="standard_2d",
        expected_attendance=50
    ),
    Event(
        meeting_name="2026 ASCO Direct Minneapolis",
        meeting_date_long="August 1-2, 2026",
        venue="Four Seasons Minneapolis",
        city_state="Minneapolis, MN",
        default_tier="standard_2d",
        expected_attendance=50
    ),
    Event(
        meeting_name="2026 ASCO Direct Maine",
        meeting_date_long="August 1-2, 2026",
        venue="TBD",
        city_state="Portland, ME",
        default_tier="standard_2d",
        expected_attendance=50
    ),
    Event(
        meeting_name="2026 ASCO Direct Boston",
        meeting_date_long="August 8-9, 2026",
        venue="Ritz Carlton Boston",
        city_state="Boston, MA",
        default_tier="standard_2d",
        expected_attendance=50
    ),
    Event(
        meeting_name="2026 ASCO Direct Seattle",
        meeting_date_long="August 8-9, 2026",
        venue="Hilton Motif Seattle",
        city_state="Seattle, WA",
        default_tier="standard_2d",
        expected_attendance=50
    ),
    Event(
        meeting_name="2026 ASCO Direct Memphis",
        meeting_date_long="August 8-9, 2026",
        venue="Hilton Memphis",
        city_state="Memphis, TN",
        default_tier="standard_2d",
        expected_attendance=60
    ),
    Event(
        meeting_name="2026 Cancer Update GU and Lung, Princeton, NJ",
        meeting_date_long="August 13, 2026",
        venue="Princeton Marriott at Forrestal",
        city_state="Princeton, NJ",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 Oncology Clinical Updates - Review and Renew Martha's Vineyard",
        meeting_date_long="August 15-16, 2026",
        venue="Martha's Vineyard, MA",
        city_state="Martha's Vineyard, MA",
        default_tier="standard_2d"
    ),
    Event(
        meeting_name="2026 Cancer Updates GU and Heme, Houston, TX",
        meeting_date_long="September 10, 2026",
        venue="The Blossom Hotel Houston",
        city_state="Houston, TX",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 MDONS Conference",
        meeting_date_long="September 18, 2026",
        venue="The Westin Westminster",
        city_state="Denver, CO",
        default_tier="standard_1d",
        expected_attendance=200
    ),
    Event(
        meeting_name="2026 Cancer Updates Lung and Breast, Dallas, TX",
        meeting_date_long="September 24, 2026",
        venue="The Beeman Hotel",
        city_state="Dallas, TX",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 Cancer Updates GU and Lung, Philadelphia, PA",
        meeting_date_long="September 24, 2026",
        venue="Hilton Penn's Landing",
        city_state="Philadelphia, PA",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 Astera Cancer Care Annual Retreat",
        meeting_date_long="September 26, 2026",
        venue="Ocean Place Resort and Spa",
        city_state="Long Branch, NJ",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2026 Pathways Conference",
        meeting_date_long="September 25-26, 2026",
        venue="Hotel Zaza Houston",
        city_state="Houston, TX",
        default_tier="standard_2d"
    ),
    Event(
        meeting_name="2026 Cancer Updates GI and Breast, Boston, MA",
        meeting_date_long="October 1, 2026",
        venue="Battery Wharf Hotel Boston Waterfront",
        city_state="Boston, MA",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 West Oncology APP Dinner",
        meeting_date_long="October 8, 2026",
        venue="Hilton Memphis",
        city_state="Memphis, TN",
        default_tier="standard_1d",
        expected_attendance=30
    ),
    Event(
        meeting_name="2026 Virtual West Oncology APP",
        meeting_date_long="October 9, 2026",
        venue="Virtual",
        city_state="Virtual",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2026 Empower (Patient Meeting)",
        meeting_date_long="October 10, 2026",
        venue="Boca Raton, FL",
        city_state="Boca Raton, FL",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2026 Empower GI Conference",
        meeting_date_long="November 7, 2026",
        venue="Washington DC",
        city_state="Washington DC",
        default_tier="standard_1d"
    ),
    Event(
        meeting_name="2026 ESMO USA West",
        meeting_date_long="November 14-15, 2026",
        venue="Colorado Springs, CO",
        city_state="Colorado Springs, CO",
        default_tier="standard_2d"
    ),
    Event(
        meeting_name="2026 ESMO USA East",
        meeting_date_long="November 14-15, 2026",
        venue="Orlando, FL",
        city_state="Orlando, FL",
        default_tier="standard_2d"
    ),
    Event(
        meeting_name="2026 Multidisciplinary Head and Neck Cancer Symposium",
        meeting_date_long="November 14, 2026",
        venue="Garden City, NY",
        city_state="Garden City, NY",
        default_tier="standard_1d"
    ),
]


# ============================================================================
# ALL EVENTS COMBINED
# ============================================================================

ALL_EVENTS = EVENTS_2025 + EVENTS_2026


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_all_events() -> List[Event]:
    """Get all events (2025 + 2026)"""
    return ALL_EVENTS


def get_events_by_year(year: int) -> List[Event]:
    """Get events for a specific year"""
    return [event for event in ALL_EVENTS if event.get_year() == year]


def find_event_by_name(name: str) -> Optional[Event]:
    """Find event by exact name match"""
    for event in ALL_EVENTS:
        if event.meeting_name == name:
            return event
    return None


def search_events(query: str) -> List[Event]:
    """Search events by name, city, state, or venue (case-insensitive)"""
    query_lower = query.lower()
    results = []

    for event in ALL_EVENTS:
        searchable = (
            event.meeting_name.lower() + " " +
            event.city_state.lower() + " " +
            event.venue.lower()
        )

        if query_lower in searchable:
            results.append(event)

    return results
