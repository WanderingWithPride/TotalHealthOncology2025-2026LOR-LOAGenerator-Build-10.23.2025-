"""
LOA Generator - Total Health Conferencing
Generates Letters of Agreement for conference sponsorship
"""
import datetime as dt
from typing import List, Dict
from io import BytesIO
from generators.base import BaseDocumentGenerator, parse_additional_info
from generators.docx_builder import DOCXBuilder
from generators.pdf_builder import PDFBuilder
from config.pricing import ADD_ON_BULLETS, currency
from config.settings import COMPANY_INFO


class LOAGenerator(BaseDocumentGenerator):
    """
    Generates Letter of Agreement (LOA) documents

    LOA structure:
    1. Logo
    2. "LETTER OF AGREEMENT (LOA)" title
    3. Agreement parties and legal text
    4. 15 numbered sections with terms and conditions
    5. Signature sections (NO signature image - manual signing)
    """

    def generate_paragraphs(self) -> List[str]:
        """
        Generate LOA paragraphs from payload

        Returns:
            List of paragraph strings organized by section
        """
        payload = self.payload

        # Extract key information
        agreement_date = payload.get("agreement_date", dt.date.today().strftime("%B %d, %Y"))
        company_name = payload.get("company_name", "[Company]")
        company_address = payload.get("company_address", "[Address]")
        meeting_name = payload.get("meeting_name", "[Meeting]")
        meeting_date = payload.get("meeting_date_long", "[Date]")
        venue = payload.get("venue", "[Venue]")
        city_state = payload.get("city_state", "[City, State]")
        amount = payload.get("amount_currency", "[Amount]")

        # Smart venue display
        if venue == city_state or venue in city_state:
            location = city_state
        else:
            location = f"{venue}, {city_state}"

        paras = []

        # Title
        paras.append("LETTER OF AGREEMENT (LOA)")
        paras.append("")

        # Parties paragraph
        paras.append(
            f"This Letter of Agreement (the \"Agreement\") is made as of {agreement_date} by and between "
            f"{COMPANY_INFO['name']} (\"Total Health\"), with its principal place of business at "
            f"{COMPANY_INFO['address']}, and {company_name} (\"Sponsor\"), with its principal place of "
            f"business at {company_address}. The individual signing this Agreement represents that they have "
            f"the authority to legally bind the Sponsor to this Agreement."
        )
        paras.append("")

        # Section 1: Purpose
        paras.append("1. Purpose")
        paras.append("")
        paras.append(
            "The purpose of this Agreement is to outline the terms under which the Sponsor agrees to participate "
            "in Total Health's educational events by securing exhibit tables, product theaters, and other "
            "sponsorship-related opportunities, as defined in the attached Scope of Work (SOW)."
        )
        paras.append("")

        # Section 2: Scope of Work
        paras.append("2. Scope of Work (SOW)")
        paras.append("")
        paras.append("The SOW, attached as Exhibit A, details the services Total Health will provide educational related services.")
        paras.append("")
        paras.append(
            "Each sponsorship opportunity including name and date of meeting, city, and specific sponsor items will be "
            "specified in the SOW. This Agreement applies to all events listed within the specified dates and covers "
            "all agreed-upon sponsorship activities."
        )
        paras.append("")

        # Event details
        paras.append("**SPECIFIC EVENT DETAILS:**")
        paras.append(f"• Event: {meeting_name}")
        paras.append(f"• Date: {meeting_date}")
        paras.append(f"• Location: {location}")
        paras.append(f"• Total Sponsorship Amount: {amount}")
        paras.append("")

        return paras

    def _generate_full_loa_text(self) -> List[str]:
        """Generate complete LOA text with all 15 sections"""
        paras = self.generate_paragraphs()

        # Add detailed SOW section
        paras.append("**DETAILED SCOPE OF WORK:**")
        paras.append("")

        # Booth details if selected
        if self.payload.get("booth_selected"):
            booth_tier = self.payload.get("booth_tier", "Standard")
            booth_price = self.payload.get("booth_price", 0)

            paras.append("**EXHIBIT BOOTH SPONSORSHIP:**")
            paras.append(f"• Booth Tier: {booth_tier}")
            paras.append(f"• Booth Cost: {currency(booth_price)}")
            paras.append("• Booth Benefits:")
            paras.append("  - Designated exhibit space at the event")
            paras.append("  - Company name and logo in event materials")
            paras.append("  - Access to attendee networking opportunities")
            paras.append("  - Inclusion in event directory and program")
            paras.append("")

        # Add-ons details
        add_on_keys = self.payload.get("add_on_keys", [])
        if add_on_keys:
            paras.append("**ADDITIONAL SPONSORSHIP COMPONENTS:**")

            # We need pricing info - get from payload or reconstruct
            for key in add_on_keys:
                if key in ADD_ON_BULLETS:
                    # Get label and price from payload or config
                    label = key.replace('_', ' ').title()
                    paras.append(f"• {label}")

                    # Add benefits
                    for bullet in ADD_ON_BULLETS[key]:
                        paras.append(f"  - {bullet}")

            paras.append("")

        # Additional information if provided
        if self.payload.get("additional_info"):
            paras.append("**ADDITIONAL SPONSORSHIP REQUIREMENTS:**")
            paras.append(self.payload["additional_info"])
            paras.append("")

        # Section 3: Payment and Financial Terms
        paras.append("3. Payment and Financial Terms")
        paras.append("")
        paras.append(
            "Full payment is due within 60 days of receiving the invoice, regardless of the Sponsor's attendance "
            "or participation. No refunds shall be issued under any circumstances, except those agreed upon in writing."
        )
        paras.append("")
        paras.append(
            "Any notice of cancellation for participation in an event must be submitted in writing at least sixty (60) days "
            "prior to the event. Cancellations made within this period will receive a 50% credit of all fees paid toward a "
            "future program, at Total Health's discretion. Cancellations after this period will not be entitled to any credit. "
            "In cases where Total Health is unable to produce a scheduled meeting, a credit may be issued at Total Health's "
            "toward future programs."
        )
        paras.append("")

        # Sections 4-15 (standard legal text)
        self._add_standard_loa_sections(paras)

        # Signature section
        paras.append("15. Signatures")
        paras.append("")
        paras.append("By signing below, the parties agree to the terms and conditions outlined in this Agreement.")
        paras.append("")

        return paras

    def _add_standard_loa_sections(self, paras: List[str]):
        """Add standard legal sections 4-14 to LOA"""

        # Section 4
        paras.append("4. Right to Refuse Exhibit")
        paras.append("")
        paras.append(
            "Total Health reserves the right to decline, prohibit, or expel any exhibit it deems inappropriate or out of "
            "character with the event, or if the exhibit violates the terms of this Agreement or applicable laws and regulations. "
            "No refunds or credits will be issued if an exhibit is refused or expelled under these conditions."
        )
        paras.append("")

        # Section 5
        paras.append("5. Compliance with Laws and Facility Rules")
        paras.append("")
        paras.append(
            "The Sponsor shall comply with all applicable laws, codes, and regulations, as well as the rules of the venue "
            "where the event is held. The Sponsor assumes all liability for any non-compliance and agrees to indemnify Total "
            "Health against any claims arising from such violations."
        )
        paras.append("")

        # Section 6
        paras.append("6. Advertising and Solicitation")
        paras.append("")
        paras.append(
            "Distribution of advertising materials and solicitation is restricted to the Sponsor's designated booth area only. "
            "Any unauthorized promotion outside the assigned space may result in the removal of the Sponsor from the event, "
            "without refund or credit."
        )
        paras.append("")

        # Section 7
        paras.append("7. Occupancy of Exhibit Space")
        paras.append("")
        paras.append(
            "Sponsor's use of exhibit space is mandatory. Should the Sponsor fail to occupy the space, Total Health reserves "
            "the right to repurpose the space as it sees fit, without offering any rebate or credit."
        )
        paras.append("")

        # Section 8
        paras.append("8. Installation and Dismantling of Exhibits")
        paras.append("")
        paras.append(
            "The Sponsor is responsible for adhering to the installation and dismantling schedules provided by Total Health. "
            "Any deviations or delays in setup or breakdown may result in penalties or additional charges. It is the Sponsor's "
            "responsibility to coordinate with their team and notify any third parties involved about these schedules."
        )
        paras.append("")

        # Section 9
        paras.append("9. Liability and Insurance")
        paras.append("")
        paras.append(
            "Total Health and the venue assume no responsibility for the protection or safety of the Sponsor's representatives, "
            "agents, or property. Total Health recommends that small and easily portable items be secured or removed outside of "
            "exhibit hours."
        )
        paras.append("")
        paras.append(
            "Indemnification: The Sponsor agrees to indemnify, defend, and hold harmless Total Health, its officers, employees, "
            "and agents from any claims, damages, or liabilities arising from the Sponsor's participation, exhibit, or actions "
            "at the event."
        )
        paras.append("")

        # Section 11 (note: skipping 10 to match original)
        paras.append("11. Force Majeure")
        paras.append("")
        paras.append(
            "Total Health shall not be liable for any failure to perform its obligations under this Agreement due to circumstances "
            "beyond its reasonable control, including, but not limited to, acts of God, natural disasters, pandemics, government "
            "restrictions, or any other unforeseen event (\"Force Majeure\"). In such cases, Total Health may reschedule the event "
            "or offer a credit at its discretion, without liability for any resulting damages or costs incurred by the Sponsor."
        )
        paras.append("")

        # Section 12
        paras.append("12. Confidentiality")
        paras.append("")
        paras.append(
            "The terms of this Agreement, including the SOW and all proprietary information exchanged between Total Health and "
            "the Sponsor, shall be considered confidential and shall not be disclosed to third parties without the prior written "
            "consent of both parties, except as required by law."
        )
        paras.append("")

        # Section 13
        paras.append("13. Entire Agreement")
        paras.append("")
        paras.append(
            "This Agreement, together with the attached SOW, represents the complete understanding between Total Health and the "
            "Sponsor, superseding any prior discussions or agreements. Any amendments must be in writing and signed by both parties "
            "to be valid."
        )
        paras.append("")

        # Section 14
        paras.append("14. Governing Law and Dispute Resolution")
        paras.append("")
        paras.append(
            "This Agreement shall be governed by the laws of the State of Florida. Any disputes arising out of or relating to this "
            "Agreement shall be resolved through binding arbitration in West Palm Beach, FL, with each party bearing its own legal "
            "fees and costs."
        )
        paras.append("")

    def generate_docx(self) -> BytesIO:
        """
        Generate LOA as DOCX document

        Returns:
            BytesIO buffer containing DOCX file
        """
        builder = DOCXBuilder()

        # Add logo
        logo_bytes = self.get_logo_bytes()
        builder.add_logo(logo_bytes)

        # Generate full LOA text
        all_paras = self._generate_full_loa_text()

        # Add title (first paragraph)
        builder.add_title(all_paras[0], bold=True, centered=True)

        # Add all paragraphs
        for para in all_paras[1:]:
            if para == "":
                builder.add_blank_line()
            elif para.startswith("**") and para.endswith(":**"):
                # Section header
                header = para.strip("*").rstrip(":")
                builder.add_section_header(header, bold=True)
            elif para.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "11.", "12.", "13.", "14.", "15.")):
                # Numbered section
                builder.add_section_header(para, bold=True)
            elif para.startswith("•"):
                # Bullet point (add as simple paragraph with indent)
                builder.add_paragraph(para, spacing_after=4)
            else:
                builder.add_paragraph(para, spacing_after=10)

        # Add signature fields
        builder.add_blank_line()
        builder.add_loa_field("Total Health")
        builder.add_blank_line()
        builder.add_loa_field("By", underline_length=50)

        # Add signatory info from payload
        signature_person = self.payload.get("signature_person", "Sarah Louden - Founder and Executive Director, Total Health Conferencing")

        if " - " in signature_person:
            name, title = signature_person.split(" - ", 1)
            builder.add_loa_field("Name", name)
            builder.add_loa_field("Title", title)
        else:
            builder.add_loa_field("Name", signature_person)
            builder.add_loa_field("Title", underline_length=50)

        builder.add_loa_field("Date", dt.date.today().strftime("%B %d, %Y"))

        # Sponsor signature section
        builder.add_blank_line()
        builder.add_blank_line()
        builder.add_loa_field("Sponsor")
        builder.add_blank_line()
        builder.add_loa_field("By", underline_length=50)
        builder.add_loa_field("Name", underline_length=50)
        builder.add_loa_field("Title", underline_length=50)
        builder.add_loa_field("Date", underline_length=30)

        return builder.get_buffer()

    def generate_pdf(self) -> BytesIO:
        """
        Generate LOA as PDF document

        Returns:
            BytesIO buffer containing PDF file
        """
        builder = PDFBuilder()

        # Add logo
        logo_bytes = self.get_logo_bytes()
        builder.add_logo(logo_bytes)

        # Generate full LOA text
        all_paras = self._generate_full_loa_text()

        # Add title
        builder.add_title(all_paras[0], centered=True)

        # Add all paragraphs
        for para in all_paras[1:]:
            if para == "":
                builder.add_blank_line()
            elif para.startswith("**") and para.endswith(":**"):
                # Section header
                header = para.strip("*").rstrip(":")
                builder.add_section_header(header, bold=True)
            elif para.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "11.", "12.", "13.", "14.", "15.")):
                # Numbered section
                builder.add_section_header(para, bold=True)
            elif para.startswith("•"):
                # Bullet point
                builder.add_paragraph(para, spacing_after=4)
            else:
                builder.add_paragraph(para, spacing_after=10)

        # Add signature fields (as text in PDF)
        builder.add_blank_line()
        builder.add_paragraph("Total Health", spacing_after=6)
        builder.add_paragraph("By: ____________________________", spacing_after=4)

        # Add signatory info
        signature_person = self.payload.get("signature_person", "Sarah Louden - Founder and Executive Director, Total Health Conferencing")

        if " - " in signature_person:
            name, title = signature_person.split(" - ", 1)
            builder.add_paragraph(f"Name: {name}", spacing_after=4)
            builder.add_paragraph(f"Title: {title}", spacing_after=4)
        else:
            builder.add_paragraph(f"Name: {signature_person}", spacing_after=4)
            builder.add_paragraph("Title: ____________________________", spacing_after=4)

        builder.add_paragraph(f"Date: {dt.date.today().strftime('%B %d, %Y')}", spacing_after=12)

        # Sponsor signature section
        builder.add_blank_line()
        builder.add_paragraph("Sponsor", spacing_after=6)
        builder.add_paragraph("By: ____________________________", spacing_after=4)
        builder.add_paragraph("Name: ____________________________", spacing_after=4)
        builder.add_paragraph("Title: ____________________________", spacing_after=4)
        builder.add_paragraph("Date: ____________________________", spacing_after=4)

        return builder.get_buffer()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def generate_loa(payload: Dict) -> tuple:
    """
    Generate LOA documents (DOCX and PDF)

    Args:
        payload: Document payload dictionary

    Returns:
        Tuple of (docx_buffer, pdf_buffer)
    """
    generator = LOAGenerator(payload)
    docx_buffer = generator.generate_docx()
    pdf_buffer = generator.generate_pdf()
    return docx_buffer, pdf_buffer
