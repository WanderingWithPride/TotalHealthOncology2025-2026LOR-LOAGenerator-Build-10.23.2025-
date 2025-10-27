"""
LOR/LOA Generator - Total Health Conferencing
Professional healthcare document generation system

Version 2.0 - Complete Rebuild
Production-ready, modular, and maintainable
"""
import streamlit as st

# Configure page
st.set_page_config(
    page_title="LOR/LOA Generator - Total Health",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Security - require authentication
from core.security import require_authentication
require_authentication()

# Import modules
from config.events import get_all_events, search_events
from config.pricing import (
    get_booth_prices, BOOTH_TIER_LABELS, get_add_ons_pricing,
    ADD_ON_CATEGORIES, DISCOUNT_OPTIONS, currency
)
from config.settings import SARAH_INFO, COMPLIANCE_TEMPLATES
from core.models import DocumentPayload
from core.pricing_calc import PricingEngine
from core.logger import log_generation, get_recent_activity, get_activity_stats
from generators.lor_generator import generate_lor
from generators.loa_generator import generate_loa
from services.multi_meeting import create_multi_meeting_package, generate_multi_meeting_documents
import datetime as dt


# ============================================================================
# PAGE HEADER
# ============================================================================

st.title("📄 LOR/LOA Generator")
st.markdown("**Total Health Conferencing** - Professional Document Generation System")
st.markdown("---")


# ============================================================================
# SIDEBAR - MODE SELECTION
# ============================================================================

with st.sidebar:
    st.header("🎯 Generation Mode")

    mode = st.radio(
        "Select Mode:",
        options=["Single Event", "Multi-Meeting Package", "Excel Bulk"],
        help="Choose how you want to generate documents"
    )

    st.markdown("---")

    # Document type selection
    doc_type = st.radio(
        "Document Type:",
        options=["LOR", "LOA"],
        help="LOR = Letter of Request, LOA = Letter of Agreement"
    )

    st.markdown("---")
    st.caption(f"👤 Logged in as: {st.session_state.get('user_role', 'User')}")


# ============================================================================
# MODE 1: SINGLE EVENT
# ============================================================================

if mode == "Single Event":
    st.header("📝 Single Event Generator")

    # Event selection
    st.subheader("1️⃣ Select Event")

    search_query = st.text_input("🔍 Search Events", placeholder="Type to search...", key="search")

    # Get and filter events
    all_events = get_all_events()

    if search_query:
        events = search_events(search_query)
        st.info(f"Found {len(events)} events matching '{search_query}'")
    else:
        events = all_events

    # Event dropdown
    event_names = [f"{e.meeting_name} - {e.meeting_date_long}" for e in events]

    if not events:
        st.warning("No events found. Try a different search term.")
        st.stop()

    selected_event_idx = st.selectbox(
        "Choose Event:",
        options=range(len(events)),
        format_func=lambda i: event_names[i],
        key="event_select"
    )

    selected_event = events[selected_event_idx]

    # Company information
    st.subheader("2️⃣ Company Information")

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("Company Name*", key="company")

    with col2:
        attendance = st.number_input(
            "Expected Attendance (optional)",
            min_value=0,
            value=selected_event.expected_attendance or 0,
            key="attendance"
        )

    if doc_type == "LOA":
        company_address = st.text_area("Company Address*", key="address")

    # Booth selection
    st.subheader("3️⃣ Booth Selection")

    booth_prices = get_booth_prices()
    booth_options = ["(no booth)"] + list(booth_prices.keys())
    booth_labels = {k: f"{BOOTH_TIER_LABELS.get(k, k)} - {currency(booth_prices.get(k, 0))}" for k in booth_prices.keys()}
    booth_labels["(no booth)"] = "(No Booth - Add-ons Only)"

    booth_tier = st.selectbox(
        "Booth Tier:",
        options=booth_options,
        format_func=lambda x: booth_labels.get(x, x),
        index=booth_options.index(selected_event.default_tier) if selected_event.default_tier in booth_options else 0,
        key="booth"
    )

    # Add-ons selection
    st.subheader("4️⃣ Add-ons (Optional)")

    event_year = selected_event.get_year()
    add_ons_pricing = get_add_ons_pricing(event_year)
    selected_addons = []

    for category, addon_keys in ADD_ON_CATEGORIES.items():
        with st.expander(category):
            for key in addon_keys:
                if key in add_ons_pricing:
                    addon = add_ons_pricing[key]
                    if st.checkbox(
                        f"{addon['label']} - {currency(addon['price'])}",
                        key=f"addon_{key}"
                    ):
                        selected_addons.append(key)

    # Pricing
    st.subheader("5️⃣ Pricing")

    discount_key = st.selectbox(
        "Discount:",
        options=list(DISCOUNT_OPTIONS.keys()),
        format_func=lambda k: DISCOUNT_OPTIONS[k]["label"],
        key="discount"
    )

    custom_total = None
    if discount_key == "custom":
        custom_total = st.number_input("Custom Total Amount:", min_value=0.0, step=50.0, key="custom_total")

    # Calculate pricing
    pricing = PricingEngine.calculate_pricing(
        booth_tier=booth_tier,
        add_on_keys=selected_addons,
        event_year=event_year,
        discount_key=discount_key,
        custom_total=custom_total
    )

    # Display pricing
    st.markdown("**Pricing Summary:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Booth", currency(pricing.booth_price))
    with col2:
        st.metric("Add-ons", currency(pricing.add_ons_total))
    with col3:
        st.metric("**TOTAL**", currency(pricing.rounded_total))

    # Additional info
    st.subheader("6️⃣ Additional Information (Optional)")

    with st.expander("📋 Use Compliance Template"):
        for key, template in COMPLIANCE_TEMPLATES.items():
            if st.button(template["name"], key=f"template_{key}"):
                st.session_state.additional_info = template["text"]

    additional_info = st.text_area(
        "Additional Requirements:",
        value=st.session_state.get("additional_info", ""),
        height=150,
        key="additional_info"
    )

    # Generate button
    st.markdown("---")

    if st.button("🚀 Generate Documents", type="primary", use_container_width=True):
        if not company_name:
            st.error("Please enter a company name")
        elif doc_type == "LOA" and not company_address:
            st.error("Please enter a company address for LOA")
        else:
            with st.spinner("Generating documents..."):
                # Create payload
                payload = DocumentPayload(
                    company_name=company_name,
                    company_address=company_address if doc_type == "LOA" else None,
                    meeting_name=selected_event.meeting_name,
                    meeting_date_long=selected_event.meeting_date_long,
                    venue=selected_event.venue,
                    city_state=selected_event.city_state,
                    booth_selected=booth_tier != "(no booth)",
                    booth_tier=booth_tier,
                    booth_price=pricing.booth_price,
                    add_on_keys=selected_addons,
                    add_ons_total=pricing.add_ons_total,
                    subtotal=pricing.subtotal,
                    discount_applied=pricing.discount_amount,
                    final_total=pricing.rounded_total,
                    amount_currency=currency(pricing.rounded_total),
                    additional_info=additional_info,
                    attendance_expected=attendance if attendance > 0 else None,
                    document_type=doc_type,
                    event_year=event_year,
                    agreement_date=dt.date.today().strftime("%B %d, %Y") if doc_type == "LOA" else None
                )

                # Generate documents
                if doc_type == "LOR":
                    docx_buffer, pdf_buffer = generate_lor(payload.to_dict())
                else:
                    docx_buffer, pdf_buffer = generate_loa(payload.to_dict())

                # Log generation
                log_generation(
                    company_name=company_name,
                    meeting_name=selected_event.meeting_name,
                    document_type=doc_type,
                    booth_selected=booth_tier,
                    add_ons=selected_addons,
                    total_cost=pricing.rounded_total,
                    mode="single-event"
                )

                st.success("✅ Documents generated successfully!")

                # Download buttons
                col1, col2 = st.columns(2)

                with col1:
                    st.download_button(
                        "📄 Download DOCX",
                        data=docx_buffer,
                        file_name=f"{doc_type}_{company_name.replace(' ', '_')}_{selected_event.meeting_name[:30].replace(' ', '_')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )

                with col2:
                    st.download_button(
                        "📄 Download PDF",
                        data=pdf_buffer,
                        file_name=f"{doc_type}_{company_name.replace(' ', '_')}_{selected_event.meeting_name[:30].replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )


# ============================================================================
# MODE 2: MULTI-MEETING PACKAGE
# ============================================================================

elif mode == "Multi-Meeting Package":
    st.header("📦 Multi-Meeting Package Generator")
    st.info("💡 Select multiple events to create a comprehensive sponsorship package")

    # Company information
    st.subheader("1️⃣ Company Information")

    company_name = st.text_input("Company Name*", key="mm_company")

    if doc_type == "LOA":
        company_address = st.text_area("Company Address*", key="mm_address")

    # Event selection
    st.subheader("2️⃣ Select Events")

    all_events = get_all_events()

    # Initialize session state for multi-meeting
    if 'mm_selected_events' not in st.session_state:
        st.session_state.mm_selected_events = []

    if 'mm_configs' not in st.session_state:
        st.session_state.mm_configs = {}

    # Event checkboxes
    for event in all_events[:20]:  # Limit to first 20 for UI performance
        event_key = f"mm_event_{event.meeting_name}"

        if st.checkbox(
            f"{event.meeting_name} - {event.meeting_date_long} ({event.city_state})",
            key=event_key
        ):
            if event not in st.session_state.mm_selected_events:
                st.session_state.mm_selected_events.append(event)
        elif event in st.session_state.mm_selected_events:
            st.session_state.mm_selected_events.remove(event)

    if st.session_state.mm_selected_events:
        st.success(f"✅ {len(st.session_state.mm_selected_events)} events selected")

        # Configure each event
        st.subheader("3️⃣ Configure Each Event")

        events_configs = []

        for event in st.session_state.mm_selected_events:
            with st.expander(f"⚙️ {event.meeting_name}"):
                col1, col2 = st.columns(2)

                with col1:
                    booth_tier = st.selectbox(
                        "Booth:",
                        options=["(no booth)"] + list(get_booth_prices().keys()),
                        key=f"mm_booth_{event.meeting_name}"
                    )

                with col2:
                    event_year = event.get_year()
                    add_ons_pricing = get_add_ons_pricing(event_year)
                    selected_addons = st.multiselect(
                        "Add-ons:",
                        options=list(add_ons_pricing.keys()),
                        format_func=lambda k: add_ons_pricing[k]["label"],
                        key=f"mm_addons_{event.meeting_name}"
                    )

                events_configs.append({
                    "event": event,
                    "booth_tier": booth_tier,
                    "add_on_keys": selected_addons
                })

        # Generate button
        st.markdown("---")

        if st.button("🚀 Generate Multi-Meeting Package", type="primary", use_container_width=True):
            if not company_name:
                st.error("Please enter a company name")
            else:
                with st.spinner("Generating package..."):
                    # Create package
                    package = create_multi_meeting_package(
                        company_name=company_name,
                        events_configs=events_configs,
                        document_type=doc_type,
                        company_address=company_address if doc_type == "LOA" else ""
                    )

                    # Generate documents
                    docx_buffer, pdf_buffer = generate_multi_meeting_documents(package)

                    # Log generation
                    log_generation(
                        company_name=company_name,
                        meeting_name=f"Multi-Meeting Package ({len(events_configs)} events)",
                        document_type=doc_type,
                        booth_selected="Multi-Meeting",
                        add_ons=[],
                        total_cost=package.final_total,
                        mode="multi-meeting"
                    )

                    st.success(f"✅ Package generated! Total: {currency(package.final_total)}")

                    # Download buttons
                    col1, col2 = st.columns(2)

                    with col1:
                        st.download_button(
                            "📄 Download DOCX",
                            data=docx_buffer,
                            file_name=f"MM_{doc_type}_{company_name.replace(' ', '_')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )

                    with col2:
                        st.download_button(
                            "📄 Download PDF",
                            data=pdf_buffer,
                            file_name=f"MM_{doc_type}_{company_name.replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

    else:
        st.warning("Please select at least one event")


# ============================================================================
# MODE 3: EXCEL BULK (Simplified - show instructions)
# ============================================================================

else:  # Excel Bulk
    st.header("📊 Excel Bulk Generator")
    st.info("⚠️ Excel Bulk Mode is available in the full version. For now, use Single Event or Multi-Meeting mode.")

    st.markdown("""
    ### Coming Soon

    The Excel Bulk mode allows you to:
    - Upload an Excel spreadsheet with multiple events
    - Auto-match event names to system events
    - Generate hundreds of letters in seconds
    - Download as organized ZIP file

    **For now, please use:**
    - **Single Event** for individual letters
    - **Multi-Meeting Package** for multi-event sponsorships
    """)


# ============================================================================
# ACTIVITY LOG (Bottom of page)
# ============================================================================

st.markdown("---")
st.header("📊 Recent Activity")

with st.expander("View Recent Letter Generation"):
    recent = get_recent_activity(limit=10)

    if recent:
        for log in recent:
            st.markdown(f"""
            **{log.get('company_name')}** - {log.get('meeting_name')}
            - Type: {log.get('document_type')} | Total: ${log.get('total_cost'):,.2f}
            - Generated: {log.get('timestamp')} by {log.get('user_role')}
            """)
            st.markdown("---")
    else:
        st.info("No recent activity")

    # Statistics
    stats = get_activity_stats()
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Letters", stats["total_letters"])
    with col2:
        st.metric("LORs", stats["lor_count"])
    with col3:
        st.metric("LOAs", stats["loa_count"])
    with col4:
        st.metric("Total Revenue", f"${stats['total_revenue']:,.2f}")
