"""
Audit Trail Logger - Total Health Conferencing
Tracks all letter generation activity for compliance and analytics
"""
import json
import os
from typing import List, Optional
from pathlib import Path
from core.models import LetterGenerationLog
from core.security import sanitize_input, get_current_user_context
from config.settings import LOGGING_CONFIG


class AuditLogger:
    """
    Manages audit trail for letter generation

    Features:
    - Secure logging with input sanitization
    - Automatic log rotation (max entries)
    - File size limits
    - Search and filtering
    """

    def __init__(self, log_file: str = None):
        """
        Initialize audit logger

        Args:
            log_file: Path to log file (default from config)
        """
        if log_file is None:
            log_file = LOGGING_CONFIG["log_file"]

        self.log_file = Path(log_file)
        self.max_file_size_mb = LOGGING_CONFIG["max_file_size_mb"]
        self.max_entries = LOGGING_CONFIG["max_entries"]

    def log_letter_generation(
        self,
        company_name: str,
        meeting_name: str,
        document_type: str,
        booth_selected: Optional[str],
        add_ons: List[str],
        total_cost: float,
        additional_info: str = "",
        mode: str = "single"
    ) -> bool:
        """
        Log a letter generation event

        Args:
            company_name: Company name
            meeting_name: Meeting/event name
            document_type: "LOR" or "LOA"
            booth_selected: Booth tier selected
            add_ons: List of add-on keys
            total_cost: Final total cost
            additional_info: Additional details
            mode: Generation mode ("single", "multi-meeting", "excel-bulk")

        Returns:
            True if logged successfully, False otherwise
        """
        try:
            # Check file size before writing
            if not self._check_file_size():
                return False

            # Sanitize inputs
            company_name = sanitize_input(company_name)
            meeting_name = sanitize_input(meeting_name)
            document_type = sanitize_input(document_type)
            additional_info = sanitize_input(additional_info)

            # Get user context
            user_context = get_current_user_context()

            # Create log entry
            log_entry = LetterGenerationLog.create(
                company_name=company_name,
                meeting_name=meeting_name,
                document_type=document_type,
                booth_selected=booth_selected,
                add_ons=add_ons,
                total_cost=total_cost,
                additional_info=f"[{mode}] {additional_info}",
                user_role=user_context["user_role"],
                session_id=user_context["session_id"],
            )

            # Load existing log
            log_data = self._load_log()

            # Add new entry
            log_data["letters"].append(log_entry.to_dict())

            # Rotate log if needed
            if len(log_data["letters"]) > self.max_entries:
                log_data["letters"] = log_data["letters"][-self.max_entries:]

            # Save updated log
            self._save_log(log_data)

            return True

        except Exception as e:
            # Don't crash the app if logging fails
            print(f"Warning: Failed to log letter generation: {e}")
            return False

    def get_all_logs(self) -> List[dict]:
        """Get all log entries"""
        log_data = self._load_log()
        return log_data.get("letters", [])

    def get_recent_logs(self, limit: int = 50) -> List[dict]:
        """
        Get most recent log entries

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of log entries in reverse chronological order
        """
        all_logs = self.get_all_logs()
        return list(reversed(all_logs[-limit:]))

    def search_logs(
        self,
        company_name: Optional[str] = None,
        meeting_name: Optional[str] = None,
        document_type: Optional[str] = None,
        user_role: Optional[str] = None,
    ) -> List[dict]:
        """
        Search log entries with filters

        Args:
            company_name: Filter by company name (partial match)
            meeting_name: Filter by meeting name (partial match)
            document_type: Filter by document type (exact match)
            user_role: Filter by user role (exact match)

        Returns:
            List of matching log entries
        """
        all_logs = self.get_all_logs()
        filtered = []

        for log in all_logs:
            # Check filters
            if company_name and company_name.lower() not in log.get("company_name", "").lower():
                continue

            if meeting_name and meeting_name.lower() not in log.get("meeting_name", "").lower():
                continue

            if document_type and document_type != log.get("document_type"):
                continue

            if user_role and user_role != log.get("user_role"):
                continue

            filtered.append(log)

        return filtered

    def get_statistics(self) -> dict:
        """
        Get summary statistics from logs

        Returns:
            Dictionary with:
            - total_letters: Total count
            - lor_count: LOR count
            - loa_count: LOA count
            - total_revenue: Sum of all costs
            - unique_companies: Number of unique companies
        """
        all_logs = self.get_all_logs()

        lor_count = sum(1 for log in all_logs if log.get("document_type") == "LOR")
        loa_count = sum(1 for log in all_logs if log.get("document_type") == "LOA")
        total_revenue = sum(log.get("total_cost", 0) for log in all_logs)

        unique_companies = set(log.get("company_name") for log in all_logs if log.get("company_name"))

        return {
            "total_letters": len(all_logs),
            "lor_count": lor_count,
            "loa_count": loa_count,
            "total_revenue": total_revenue,
            "unique_companies": len(unique_companies),
        }

    def clear_logs(self) -> bool:
        """
        Clear all log entries (USE WITH CAUTION)

        Returns:
            True if successful
        """
        try:
            empty_log = {"letters": []}
            self._save_log(empty_log)
            return True
        except Exception as e:
            print(f"Error clearing logs: {e}")
            return False

    # ========================================================================
    # PRIVATE HELPER METHODS
    # ========================================================================

    def _load_log(self) -> dict:
        """Load log data from file"""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r') as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # Return empty log structure
        return {"letters": []}

    def _save_log(self, log_data: dict):
        """Save log data to file"""
        with open(self.log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

    def _check_file_size(self) -> bool:
        """Check if log file is within size limits"""
        try:
            if self.log_file.exists():
                file_size_mb = self.log_file.stat().st_size / (1024 * 1024)
                if file_size_mb > self.max_file_size_mb:
                    print(f"Warning: Log file too large ({file_size_mb:.1f}MB)")
                    return False
        except Exception:
            pass

        return True


# ============================================================================
# GLOBAL LOGGER INSTANCE
# ============================================================================

# Create global logger instance for easy access
audit_logger = AuditLogger()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def log_generation(
    company_name: str,
    meeting_name: str,
    document_type: str,
    booth_selected: Optional[str],
    add_ons: List[str],
    total_cost: float,
    additional_info: str = "",
    mode: str = "single"
) -> bool:
    """
    Convenience function to log letter generation

    Uses global audit_logger instance
    """
    return audit_logger.log_letter_generation(
        company_name=company_name,
        meeting_name=meeting_name,
        document_type=document_type,
        booth_selected=booth_selected,
        add_ons=add_ons,
        total_cost=total_cost,
        additional_info=additional_info,
        mode=mode
    )


def get_recent_activity(limit: int = 50) -> List[dict]:
    """Get recent letter generation activity"""
    return audit_logger.get_recent_logs(limit=limit)


def get_activity_stats() -> dict:
    """Get activity statistics"""
    return audit_logger.get_statistics()
