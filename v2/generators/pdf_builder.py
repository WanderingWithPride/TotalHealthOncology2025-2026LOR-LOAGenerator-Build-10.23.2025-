"""
PDF Document Builder - Total Health Conferencing
Creates professionally formatted PDF documents using ReportLab
"""
from io import BytesIO
from typing import List, Optional
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    Table, TableStyle
)
from reportlab.lib import colors
from PIL import Image
from generators.base import DocumentBuilder
from config.settings import DOCUMENT_SETTINGS


class PDFBuilder(DocumentBuilder):
    """
    Builds PDF documents with Total Health branding

    Uses ReportLab for professional PDF generation
    """

    def __init__(self):
        """Initialize PDF builder"""
        self.story = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Set up custom paragraph styles"""
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontName='Times-Roman',
            fontSize=11,
            leading=14,
            spaceAfter=10,
        ))

        # Bold style
        self.styles.add(ParagraphStyle(
            name='CustomBold',
            parent=self.styles['CustomBody'],
            fontName='Times-Bold',
        ))

        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontName='Times-Bold',
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=12,
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontName='Times-Bold',
            fontSize=12,
            spaceAfter=8,
            spaceBefore=12,
        ))

        # Bullet style
        self.styles.add(ParagraphStyle(
            name='Bullet',
            parent=self.styles['CustomBody'],
            leftIndent=20,
            bulletIndent=10,
        ))

    def add_logo(self, logo_bytes: Optional[bytes]):
        """
        Add logo to PDF (centered, max 2.5 inches)

        Args:
            logo_bytes: Logo image as bytes
        """
        if logo_bytes:
            try:
                # Load image to get dimensions
                img = Image.open(BytesIO(logo_bytes))
                width, height = img.size

                # Calculate scaled dimensions
                max_width = DOCUMENT_SETTINGS["logo_width_inches"] * inch
                ratio = max_width / width
                scaled_height = height * ratio

                # Create ReportLab image
                rl_img = RLImage(BytesIO(logo_bytes), width=max_width, height=scaled_height)

                # Center the image using a table
                table = Table([[rl_img]], colWidths=[6.5 * inch])
                table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))

                self.story.append(table)
                self.story.append(Spacer(1, 12))

            except Exception as e:
                print(f"Warning: Could not add logo to PDF: {e}")

    def add_title(self, title: str, bold: bool = True, centered: bool = True):
        """
        Add title to PDF

        Args:
            title: Title text
            bold: Make title bold (used in style selection)
            centered: Center align title
        """
        style = 'CustomTitle' if centered else 'SectionHeader'
        para = Paragraph(title, self.styles[style])
        self.story.append(para)
        self.story.append(Spacer(1, 6))

    def add_paragraph(self, text: str, spacing_after: int = 10):
        """
        Add paragraph to PDF

        Args:
            text: Paragraph text
            spacing_after: Spacing after paragraph (in points)
        """
        para = Paragraph(text, self.styles['CustomBody'])
        self.story.append(para)

        if spacing_after > 0:
            self.story.append(Spacer(1, spacing_after))

    def add_section_header(self, header: str, bold: bool = True):
        """
        Add section header to PDF

        Args:
            header: Header text
            bold: Make header bold
        """
        style = 'SectionHeader' if bold else 'CustomBody'
        para = Paragraph(header, self.styles[style])
        self.story.append(para)

    def add_bullet_list(self, items: List[str], indent: float = 0.25):
        """
        Add bullet list to PDF using table for proper formatting

        Args:
            items: List of bullet point texts
            indent: Indentation (not used in table-based approach)
        """
        for item in items:
            # Create 2-column table: bullet + text
            bullet_char = "•"

            table_data = [[bullet_char, item]]
            table = Table(table_data, colWidths=[0.3 * inch, 6 * inch])

            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (0, -1), 0),
                ('LEFTPADDING', (1, 0), (1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))

            self.story.append(table)

    def add_signature(self, signature_bytes: Optional[bytes]):
        """
        Add signature image to PDF (2.0 inches width)

        Args:
            signature_bytes: Signature image as bytes
        """
        if signature_bytes:
            try:
                # Load image to get dimensions
                img = Image.open(BytesIO(signature_bytes))
                width, height = img.size

                # Calculate scaled dimensions
                max_width = DOCUMENT_SETTINGS["signature_width_inches"] * inch
                ratio = max_width / width
                scaled_height = height * ratio

                # Create ReportLab image
                rl_img = RLImage(BytesIO(signature_bytes), width=max_width, height=scaled_height)

                self.story.append(Spacer(1, 12))
                self.story.append(rl_img)
                self.story.append(Spacer(1, 6))

            except Exception as e:
                print(f"Warning: Could not add signature to PDF: {e}")

    def add_contact_info(self, lines: List[str]):
        """
        Add contact information to PDF

        Args:
            lines: List of contact info lines
        """
        for line in lines:
            para = Paragraph(line, self.styles['CustomBody'])
            self.story.append(para)

    def add_blank_line(self):
        """Add blank line (spacer)"""
        self.story.append(Spacer(1, 12))

    def get_buffer(self) -> BytesIO:
        """
        Get PDF as BytesIO buffer

        Returns:
            BytesIO buffer containing PDF file
        """
        buffer = BytesIO()

        # Create PDF document with margins
        margin = DOCUMENT_SETTINGS["pdf_margins_inches"] * inch

        doc = SimpleDocTemplate(
            buffer,
            pagesize=LETTER,
            leftMargin=margin,
            rightMargin=margin,
            topMargin=margin,
            bottomMargin=margin,
        )

        # Build PDF
        doc.build(self.story)
        buffer.seek(0)

        return buffer


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_pdf_from_paragraphs(
    paragraphs: List[str],
    logo_bytes: Optional[bytes] = None,
    signature_bytes: Optional[bytes] = None,
    contact_lines: Optional[List[str]] = None,
    title: Optional[str] = None
) -> BytesIO:
    """
    Create simple PDF from paragraphs (for basic documents)

    Args:
        paragraphs: List of paragraph texts
        logo_bytes: Optional logo image
        signature_bytes: Optional signature image
        contact_lines: Optional contact information
        title: Optional document title

    Returns:
        BytesIO buffer containing PDF file
    """
    builder = PDFBuilder()

    # Add logo
    if logo_bytes:
        builder.add_logo(logo_bytes)

    # Add title
    if title:
        builder.add_title(title)
        builder.add_blank_line()

    # Add paragraphs
    for para in paragraphs:
        builder.add_paragraph(para)

    # Add signature
    if signature_bytes:
        builder.add_signature(signature_bytes)

    # Add contact info
    if contact_lines:
        builder.add_contact_info(contact_lines)

    return builder.get_buffer()
