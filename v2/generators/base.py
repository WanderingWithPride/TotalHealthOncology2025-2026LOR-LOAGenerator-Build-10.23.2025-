"""
Base Document Generator - Total Health Conferencing
Abstract base classes for document generation
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from io import BytesIO
from pathlib import Path
from config.settings import ASSETS_DIR, LOGO_PATHS, SIGNATURE_PATHS


class BaseDocumentGenerator(ABC):
    """
    Abstract base class for document generators

    Subclasses must implement:
    - generate_paragraphs()
    - generate_docx()
    - generate_pdf()
    """

    def __init__(self, payload: Dict):
        """
        Initialize generator with document payload

        Args:
            payload: Dictionary containing all document data
        """
        self.payload = payload

    @abstractmethod
    def generate_paragraphs(self) -> List[str]:
        """
        Generate document paragraphs

        Returns:
            List of paragraph strings
        """
        pass

    @abstractmethod
    def generate_docx(self) -> BytesIO:
        """
        Generate DOCX document

        Returns:
            BytesIO buffer containing DOCX file
        """
        pass

    @abstractmethod
    def generate_pdf(self) -> BytesIO:
        """
        Generate PDF document

        Returns:
            BytesIO buffer containing PDF file
        """
        pass

    # ========================================================================
    # ASSET LOADING HELPERS
    # ========================================================================

    def get_logo_bytes(self) -> Optional[bytes]:
        """
        Get logo image as bytes

        Returns:
            Logo image bytes or None if not found
        """
        return self._read_first_existing(LOGO_PATHS)

    def get_signature_bytes(self) -> Optional[bytes]:
        """
        Get signature image as bytes

        Returns:
            Signature image bytes or None if not found
        """
        return self._read_first_existing(SIGNATURE_PATHS)

    @staticmethod
    def _read_first_existing(paths: List[Path]) -> Optional[bytes]:
        """
        Read first existing file from list of paths

        Args:
            paths: List of file paths to try

        Returns:
            File contents as bytes or None if no file found
        """
        for path in paths:
            if path.exists() and path.is_file():
                return path.read_bytes()
        return None


class DocumentBuilder(ABC):
    """
    Abstract base class for format-specific builders (DOCX, PDF)

    Handles the actual document formatting and creation
    """

    @abstractmethod
    def add_logo(self, logo_bytes: Optional[bytes]):
        """Add logo to document"""
        pass

    @abstractmethod
    def add_title(self, title: str):
        """Add title to document"""
        pass

    @abstractmethod
    def add_paragraph(self, text: str):
        """Add paragraph to document"""
        pass

    @abstractmethod
    def add_bullet_list(self, items: List[str]):
        """Add bullet list to document"""
        pass

    @abstractmethod
    def add_section_header(self, header: str):
        """Add section header to document"""
        pass

    @abstractmethod
    def add_signature(self, signature_bytes: Optional[bytes]):
        """Add signature to document"""
        pass

    @abstractmethod
    def get_buffer(self) -> BytesIO:
        """Get document as BytesIO buffer"""
        pass


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def parse_additional_info(text: str) -> tuple:
    """
    Parse additional information text into lead-in and bullets

    Args:
        text: Multi-line additional information text

    Returns:
        Tuple of (lead_in: str, bullets: List[str])
    """
    if not text:
        return None, []

    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]  # Remove empty lines

    if not lines:
        return None, []

    # First line is the lead-in
    lead_in = lines[0]

    # Subsequent lines are bullets
    cleaned_bullets = []
    for bullet in lines[1:]:
        # Remove bullet characters
        s = bullet.lstrip("-•*").strip()

        # Remove numbered list formatting (1. or 1))
        if len(s) > 2 and s[0].isdigit() and s[1] in (".", ")"):
            s = s[2:].strip()

        if s:
            cleaned_bullets.append(s)

    return lead_in, cleaned_bullets


def format_currency(amount: float) -> str:
    """Format amount as USD currency"""
    return f"${amount:,.2f}"


def safe_get(data: dict, key: str, default: str = "") -> str:
    """
    Safely get value from dictionary

    Args:
        data: Dictionary to query
        key: Key to retrieve
        default: Default value if key not found

    Returns:
        Value from dictionary or default
    """
    value = data.get(key, default)
    return value if value is not None else default
