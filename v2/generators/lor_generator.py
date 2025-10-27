"""
LOR Generator - Total Health Conferencing
Generates Letters of Request for conference sponsorship
"""
import datetime as dt
from typing import List, Dict
from io import BytesIO
from generators.base import BaseDocumentGenerator, parse_additional_info
from generators.docx_builder import DOCXBuilder
from generators.pdf_builder import PDFBuilder
from config.pricing import get_booth_benefits, ADD_ON_BULLETS
from config.settings import SARAH_INFO, DEFAULT_AUDIENCE


class LORGenerator(BaseDocumentGenerator):
    """
    Generates Letter of Request (LOR) documents

    LOR structure:
    1. Logo
    2. "Letter of Request" title
    3. Date
    4. "Dear Exhibitor" salutation
    5. Opening paragraph (company + event details)
    6. Attendance information
    7. Clinical presentation description
    8. Support amount and benefits lead-in
    9. Booth benefits (if selected)
    10. Add-on benefits (if selected)
    11. Additional compliance information (if provided)
    12. Closing
    13. Signature
    14. Contact information
    """

    def generate_paragraphs(self) -> List[str]:
        """
        Generate LOR paragraphs from payload

        Returns:
            List of paragraph strings
        """
        payload = self.payload
        today_long = dt.date.today().strftime("%B %d, %Y")

        # Get audience and attendance
        audience = payload.get("audience_list", DEFAULT_AUDIENCE)
        attendance_expected = payload.get("attendance_expected")

        paras = []

        # Title
        paras.append("Letter of Request")

        # Date
        paras.append(today_long)

        # Salutation
        paras.append("Dear Exhibitor,")

        # Opening paragraph
        paras.append(
            f"Total Health Conferencing is proud to submit this request to {payload['company_name']} "
            f"for support of {payload['meeting_name']}. "
            f"The meeting will take place on {payload['meeting_date_long']} at {payload['venue']}, {payload['city_state']}."
        )

        # Attendance information
        if attendance_expected:
            paras.append(
                f"We expect {attendance_expected} total attendees, including {audience}. "
                "Attendance numbers are expected, but not guaranteed."
            )
        else:
            paras.append(
                f"We expect a strong mix of {audience}. "
                "Attendance numbers are expected, but not guaranteed."
            )

        # Clinical presentation description
        paras.append(
            f"{payload['meeting_name']} will showcase clinical presentations, allowing attendees to "
            "engage in presentation, discussion, analysis, and participation."
        )

        # Support amount and benefits lead-in
        paras.append(
            f"Your support in the amount of {payload['amount_currency']} will provide you with an "
            "opportunity to support high-quality education. Total Health Conferencing will provide "
            "you with the following benefits:"
        )

        return paras

    def generate_docx(self) -> BytesIO:
        """
        Generate LOR as DOCX document

        Returns:
            BytesIO buffer containing DOCX file
        """
        builder = DOCXBuilder()

        # Add logo
        logo_bytes = self.get_logo_bytes()
        builder.add_logo(logo_bytes)

        # Generate paragraphs
        paragraphs = self.generate_paragraphs()

        # Add title
        builder.add_title(paragraphs[0])
        builder.add_blank_line()

        # Add date and salutation
        builder.add_paragraph(paragraphs[1], spacing_after=10)
        builder.add_paragraph(paragraphs[2], spacing_after=10)

        # Add body paragraphs
        for para in paragraphs[3:]:
            builder.add_paragraph(para, spacing_after=10)

        # Add booth benefits if selected
        if self.payload.get("booth_selected"):
            builder.add_blank_line()
            builder.add_section_header("In-Person Exhibit Booth:")
            builder.add_bullet_list(get_booth_benefits())

        # Add add-ons if selected
        add_on_keys = self.payload.get("add_on_keys", [])
        if add_on_keys:
            for addon_key in add_on_keys:
                if addon_key in ADD_ON_BULLETS:
                    # Get add-on label from payload or config
                    builder.add_blank_line()
                    builder.add_section_header(f"{addon_key.replace('_', ' ').title()}:")
                    builder.add_bullet_list(ADD_ON_BULLETS[addon_key])

        # Add additional information if provided
        additional_info = self.payload.get("additional_info")
        if additional_info:
            lead_in, bullets = parse_additional_info(additional_info)

            if lead_in:
                builder.add_blank_line()
                builder.add_section_header("Additional Requirements:")
                builder.add_paragraph(lead_in, spacing_after=8)

            if bullets:
                builder.add_bullet_list(bullets)

        # Add closing
        builder.add_blank_line()
        builder.add_paragraph(
            "We are grateful for your support and look forward to working with you.",
            spacing_after=12
        )

        # Add signature
        signature_bytes = self.get_signature_bytes()
        builder.add_signature(signature_bytes)

        # Add contact information
        contact_lines = [
            SARAH_INFO["name"],
            SARAH_INFO["title"],
            SARAH_INFO["email"],
            SARAH_INFO["phone"],
        ]
        builder.add_contact_info(contact_lines)

        return builder.get_buffer()

    def generate_pdf(self) -> BytesIO:
        """
        Generate LOR as PDF document

        Returns:
            BytesIO buffer containing PDF file
        """
        builder = PDFBuilder()

        # Add logo
        logo_bytes = self.get_logo_bytes()
        builder.add_logo(logo_bytes)

        # Generate paragraphs
        paragraphs = self.generate_paragraphs()

        # Add title
        builder.add_title(paragraphs[0])
        builder.add_blank_line()

        # Add date and salutation
        builder.add_paragraph(paragraphs[1], spacing_after=10)
        builder.add_paragraph(paragraphs[2], spacing_after=10)

        # Add body paragraphs
        for para in paragraphs[3:]:
            builder.add_paragraph(para, spacing_after=10)

        # Add booth benefits if selected
        if self.payload.get("booth_selected"):
            builder.add_blank_line()
            builder.add_section_header("In-Person Exhibit Booth:")
            builder.add_bullet_list(get_booth_benefits())

        # Add add-ons if selected
        add_on_keys = self.payload.get("add_on_keys", [])
        if add_on_keys:
            for addon_key in add_on_keys:
                if addon_key in ADD_ON_BULLETS:
                    builder.add_blank_line()
                    builder.add_section_header(f"{addon_key.replace('_', ' ').title()}:")
                    builder.add_bullet_list(ADD_ON_BULLETS[addon_key])

        # Add additional information if provided
        additional_info = self.payload.get("additional_info")
        if additional_info:
            lead_in, bullets = parse_additional_info(additional_info)

            if lead_in:
                builder.add_blank_line()
                builder.add_section_header("Additional Requirements:")
                builder.add_paragraph(lead_in, spacing_after=8)

            if bullets:
                builder.add_bullet_list(bullets)

        # Add closing
        builder.add_blank_line()
        builder.add_paragraph(
            "We are grateful for your support and look forward to working with you.",
            spacing_after=12
        )

        # Add signature
        signature_bytes = self.get_signature_bytes()
        builder.add_signature(signature_bytes)

        # Add contact information
        contact_lines = [
            SARAH_INFO["name"],
            SARAH_INFO["title"],
            SARAH_INFO["email"],
            SARAH_INFO["phone"],
        ]
        builder.add_contact_info(contact_lines)

        return builder.get_buffer()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def generate_lor(payload: Dict) -> tuple:
    """
    Generate LOR documents (DOCX and PDF)

    Args:
        payload: Document payload dictionary

    Returns:
        Tuple of (docx_buffer, pdf_buffer)
    """
    generator = LORGenerator(payload)
    docx_buffer = generator.generate_docx()
    pdf_buffer = generator.generate_pdf()
    return docx_buffer, pdf_buffer
