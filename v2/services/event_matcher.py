"""
Event Matcher Service - Total Health Conferencing
Matches event names from Excel spreadsheets to system events
"""
from typing import Optional, List, Tuple
from config.events import Event, get_all_events


class EventMatcher:
    """
    Matches event names from external sources to system events

    Uses 3-stage matching algorithm:
    1. Exact partial match
    2. Normalized matching (handles ASCO naming variations)
    3. Keyword matching (year + location - minimum 3 common words)
    """

    def __init__(self):
        """Initialize event matcher with all system events"""
        self.events = get_all_events()

    def match_event(self, event_name: str) -> Optional[Event]:
        """
        Match event name to system event

        Args:
            event_name: Event name from external source (e.g., Excel)

        Returns:
            Matched Event object or None if no match found
        """
        if not event_name or not event_name.strip():
            return None

        # Stage 1: Exact partial match
        matched = self._exact_partial_match(event_name)
        if matched:
            return matched

        # Stage 2: Normalized matching
        matched = self._normalized_match(event_name)
        if matched:
            return matched

        # Stage 3: Keyword matching
        matched = self._keyword_match(event_name)
        if matched:
            return matched

        return None

    def match_with_confidence(self, event_name: str) -> Tuple[Optional[Event], str]:
        """
        Match event with confidence level

        Args:
            event_name: Event name to match

        Returns:
            Tuple of (matched_event, confidence) where confidence is "exact", "normalized", "keyword", or "none"
        """
        if not event_name or not event_name.strip():
            return None, "none"

        # Stage 1
        matched = self._exact_partial_match(event_name)
        if matched:
            return matched, "exact"

        # Stage 2
        matched = self._normalized_match(event_name)
        if matched:
            return matched, "normalized"

        # Stage 3
        matched = self._keyword_match(event_name)
        if matched:
            return matched, "keyword"

        return None, "none"

    def find_similar_events(self, event_name: str, limit: int = 5) -> List[Tuple[Event, float]]:
        """
        Find similar events with similarity scores

        Args:
            event_name: Event name to match
            limit: Maximum number of results

        Returns:
            List of (Event, similarity_score) tuples, sorted by score descending
        """
        results = []

        for event in self.events:
            score = self._calculate_similarity(event_name, event.meeting_name)
            if score > 0:
                results.append((event, score))

        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:limit]

    # ========================================================================
    # MATCHING STRATEGIES
    # ========================================================================

    def _exact_partial_match(self, event_name: str) -> Optional[Event]:
        """
        Stage 1: Exact partial match (case-insensitive)

        Checks if event_name contains system event name or vice versa
        """
        event_name_lower = event_name.lower()

        for event in self.events:
            system_name_lower = event.meeting_name.lower()

            if event_name_lower in system_name_lower or system_name_lower in event_name_lower:
                return event

        return None

    def _normalized_match(self, event_name: str) -> Optional[Event]:
        """
        Stage 2: Normalized matching

        Handles variations like:
        - "Best of ASCO" vs "ASCO Direct"
        - Different dash characters (–, —, -)
        - Extra whitespace
        """
        normalized_input = self._normalize_name(event_name)

        for event in self.events:
            normalized_system = self._normalize_name(event.meeting_name)

            if normalized_input in normalized_system or normalized_system in normalized_input:
                return event

        return None

    def _keyword_match(self, event_name: str) -> Optional[Event]:
        """
        Stage 3: Keyword matching

        Matches based on common keywords (minimum 3 words)
        Useful for matching by year + location
        """
        input_words = set(event_name.lower().split())

        best_match = None
        max_common = 0

        for event in self.events:
            system_words = set(event.meeting_name.lower().split())

            common = input_words & system_words
            common_count = len(common)

            if common_count >= 3 and common_count > max_common:
                max_common = common_count
                best_match = event

        return best_match

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    @staticmethod
    def _normalize_name(name: str) -> str:
        """
        Normalize event name for comparison

        Handles:
        - Lowercase conversion
        - Dash normalization (–, —, -)
        - ASCO naming variations
        - Whitespace normalization
        """
        name = name.lower()

        # Normalize dashes
        name = name.replace('–', '-').replace('—', '-')

        # Handle ASCO naming variations
        name = name.replace('best of asco', 'asco direct')
        name = name.replace('best of', '').replace('best', '')

        # Normalize whitespace
        name = ' '.join(name.split())

        return name

    @staticmethod
    def _calculate_similarity(str1: str, str2: str) -> float:
        """
        Calculate similarity score between two strings

        Simple word-based similarity:
        score = (common_words / total_unique_words)

        Returns:
            Float between 0.0 and 1.0
        """
        words1 = set(str1.lower().split())
        words2 = set(str2.lower().split())

        if not words1 or not words2:
            return 0.0

        common = words1 & words2
        total = words1 | words2

        return len(common) / len(total) if total else 0.0


# ============================================================================
# GLOBAL MATCHER INSTANCE
# ============================================================================

# Create global matcher instance for easy access
event_matcher = EventMatcher()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def match_event_name(event_name: str) -> Optional[Event]:
    """
    Convenience function to match event name

    Args:
        event_name: Event name to match

    Returns:
        Matched Event object or None
    """
    return event_matcher.match_event(event_name)


def match_event_with_confidence(event_name: str) -> Tuple[Optional[Event], str]:
    """
    Convenience function to match event with confidence level

    Args:
        event_name: Event name to match

    Returns:
        Tuple of (matched_event, confidence_level)
    """
    return event_matcher.match_with_confidence(event_name)
