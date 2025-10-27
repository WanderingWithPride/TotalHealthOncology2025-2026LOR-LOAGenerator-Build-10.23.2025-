"""
Unit Tests - Event Matcher
Tests for event matching algorithm
"""
import pytest
from services.event_matcher import EventMatcher
from config.events import Event


class TestEventMatcher:
    """Test event matching functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.matcher = EventMatcher()

    def test_exact_match(self):
        """Test exact event name match"""
        result = self.matcher.match_event("2026 ASCO Direct Denver")
        assert result is not None
        assert "Denver" in result.meeting_name

    def test_partial_match(self):
        """Test partial name matching"""
        result = self.matcher.match_event("ASCO Direct Denver")
        assert result is not None
        assert "Denver" in result.meeting_name

    def test_best_of_asco_normalization(self):
        """Test ASCO naming variation handling"""
        # The system has "ASCO Direct" but search uses "Best of ASCO"
        result = self.matcher.match_event("2026 Best of ASCO Denver")
        assert result is not None  # Should match despite different naming

    def test_keyword_matching(self):
        """Test keyword-based matching (3+ common words)"""
        result = self.matcher.match_event("2026 Denver June ASCO")
        assert result is not None
        assert "Denver" in result.meeting_name

    def test_no_match(self):
        """Test no match scenario"""
        result = self.matcher.match_event("NonExistent Event 2099")
        assert result is None

    def test_empty_input(self):
        """Test empty input handling"""
        result = self.matcher.match_event("")
        assert result is None

    def test_confidence_levels(self):
        """Test confidence level reporting"""
        # Exact match
        event, confidence = self.matcher.match_with_confidence("2026 ASCO Direct Denver")
        assert confidence in ["exact", "normalized", "keyword"]

        # No match
        event, confidence = self.matcher.match_with_confidence("NonExistent Event")
        assert confidence == "none"

    def test_similarity_scoring(self):
        """Test similarity scoring for fuzzy matching"""
        similar = self.matcher.find_similar_events("ASCO Denver 2026", limit=3)
        assert len(similar) <= 3
        assert all(isinstance(score, float) for _, score in similar)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
